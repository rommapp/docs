---
title: WebSockets
description: Endpoints for live updates
---

# WebSockets

RomM uses socket.io for real-time communication over two endpoints:

| Endpoint             | Purpose                                                                                                                |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `/ws/socket.io`      | Live updates (scans, notifications, sync, activity, installs, streaming, log streaming), plus the `/devices` namespace |
| `/netplay/socket.io` | Netplay session coordination (room discovery, join/leave, WebRTC signalling)                                           |

## Authentication

The default namespace on `/ws/socket.io` and the netplay endpoint authenticate with the browser's session cookie. The handshake reads the `romm_session` cookie and binds the socket to that login session. A socket without a valid session still connects, but it joins no per-user room, so it never receives events addressed to a user, and the events that act on a user's behalf (`scan`, `activity:*`) are rejected or ignored.

Signing out, or revoking a session, disconnects every socket that session opened, on both endpoints and on every worker. The client has to sign in again before it reconnects.

### The `/devices` namespace

Companion apps that hold a [device-bound Client API Token](client-api-tokens.md) connect to the `/devices` namespace instead. The token goes in the handshake's `auth` payload, or in an `Authorization: Bearer` header:

```javascript
const socket = io("https://demo.romm.app/devices", {
    path: "/ws/socket.io",
    transports: ["websocket"],
    auth: { token: "rmm_..." },
});
```

The handshake is refused with `unauthorized` unless the token is live, bound to a device, and holds `devices.read` (as does its owner). It's refused with `disabled` when `DEVICE_INSTALL_ENABLED=false`. While connected, the device counts as online for `GET /api/devices/online`. The socket is closed when the token expires or is revoked, and when the device is deleted.

## Events

### Scans

Client to server, both requiring the `tasks.run` scope:

| Event       | Payload                                                            |
| ----------- | ------------------------------------------------------------------ |
| `scan`      | A `ScanPayload` object, the same body `POST /api/tasks/scan` takes |
| `scan:stop` | None. Cancels queued scans and stops the running one               |

`ScanPayload` rejects unknown keys, so a misspelt option fails instead of silently scanning the whole library. Every field is optional:

```json
{
    "type": "quick",
    "platforms": [12, 34],
    "platform_fs_slugs": [],
    "roms_ids": [],
    "apis": ["igdb", "ss", "hasheous"],
    "launchbox_remote_enabled": true
}
```

| Field                      | Default                | Meaning                                                                                                                                                                                                       |
| -------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`                     | `quick`                | One of `new_platforms`, `quick`, `update`, `unmatched`, `complete`, `hashes`                                                                                                                                  |
| `platforms`                | `[]` (all)             | Platform ids to scan                                                                                                                                                                                          |
| `platform_fs_slugs`        | `[]`                   | Platform folder names to scan                                                                                                                                                                                 |
| `roms_ids`                 | `[]`                   | Scan only these ROMs. Such a scan may queue while a library scan runs, and goes ahead of any that's waiting                                                                                                   |
| `apis`                     | every enabled provider | Metadata providers to use, by source key: `igdb`, `moby`, `ss`, `ra`, `launchbox`, `hasheous`, `tgdb`, `sgdb`, `flashpoint`, `hltb`, `demozoo`, `pouet`, `csdb`, `steam`, `gamelist`, `libretro`, `playmatch` |
| `launchbox_remote_enabled` | `true`                 | Let LaunchBox use its remote API as well as the local metadata store                                                                                                                                          |

Server to client, broadcast to every connected socket:

| Event                    | Payload                                                                                                            |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| `scan:scanning_platform` | The platform being scanned                                                                                         |
| `scan:scanning_rom`      | The ROM just scanned, as a `SimpleRomSchema` without its file list, plus `is_new` (`true` when this scan added it) |
| `scan:update_stats`      | Running totals for the scan                                                                                        |
| `scan:done`              | Final stats                                                                                                        |
| `scan:done_ko`           | An error message string                                                                                            |

`scan:done_ko` also answers a `scan` event that couldn't start, sent only to the socket that asked. That happens when the caller lacks `tasks.run`, when the payload fails validation (the message lists each invalid field), when no scan worker is running, or when a library scan is already queued or running.

### Notifications

Sent to every open tab of the user they belong to (see [Notifications](../using/notifications.md)):

| Event                     | Payload                                                        |
| ------------------------- | -------------------------------------------------------------- |
| `notifications:new`       | The new notification, as `GET /api/notifications` returns it   |
| `notifications:read`      | `{"ids": [...]}`, or `{"ids": null}` when all were marked read |
| `notifications:dismissed` | `{"ids": [...]}`, or `{"ids": null}` when all were dismissed   |

### Activity

The "now playing" feed. Clients report their own sessions, and the acting user always comes from the socket's session, never from the payload:

| Event                | Direction        | Payload                                                                                 |
| -------------------- | ---------------- | --------------------------------------------------------------------------------------- |
| `activity:start`     | Client to server | `{"rom_id": 123, "device_id": "..."}`                                                   |
| `activity:heartbeat` | Client to server | Same as `activity:start`, to keep the session alive                                     |
| `activity:stop`      | Client to server | Same as `activity:start`                                                                |
| `activity:update`    | Server to client | An activity entry, sent only to users who can see the ROM                               |
| `activity:clear`     | Server to client | `{"user_id", "device_id", "rom_id"}`, sent to the same audience                         |
| `activity:refresh`   | Server to client | `{}`. Refetch `GET /api/activity`, because RomM couldn't work out who may see a session |

Before 5.4, `activity:update` went to every connected client. It now reaches only the `user:{id}` rooms of users allowed to see the ROM, which takes [hidden entities](../administration/users-and-roles.md#hidden-entities) and [age limits](../administration/parental-controls.md) into account. When that audience can't be resolved, RomM sends `activity:refresh` to everyone instead, coalesced across workers so a burst of failures produces one refresh.

### Device sync

Sent to the user's tabs while a device syncs (see [Device Sync Protocol](device-sync-protocol.md)). Every payload carries `device_id` and `session_id`:

| Event            | Extra fields                                                 |
| ---------------- | ------------------------------------------------------------ |
| `sync:started`   | `sync_mode`                                                  |
| `sync:progress`  | `operations_completed`, `operations_planned`, `current_file` |
| `sync:completed` | `operations_completed`, `operations_failed`                  |
| `sync:conflict`  | `file_name`, `rom_id`, `rom_name`, `reason`                  |
| `sync:error`     | `error`                                                      |

### Device installs

| Event               | Sent to                                    | Payload                                                                                                                      |
| ------------------- | ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| `install:updated`   | The owner's tabs, on the default namespace | The full install request: `id`, `user_id`, `device_id`, `rom_id`, `file_ids`, `status`, `reason`, `created_at`, `updated_at` |
| `install:queued`    | The device, on `/devices`                  | `{"id", "rom_id"}`. A request is waiting, so claim it with `POST /api/devices/{device_id}/installs/claim`                    |
| `install:cancelled` | The device, on `/devices`                  | `{"id", "rom_id"}`. Drop the request, even if the download already started                                                   |

`status` is one of `pending`, `taken`, `done`, `already_installed`, `failed` or `cancelled`.

### Permissions and logs

| Event                 | Sent to      | Payload                                                                        |
| --------------------- | ------------ | ------------------------------------------------------------------------------ |
| `permissions:changed` | Every socket | `{"user_id": 123}`. The named user should refetch `GET /api/permissions/me`    |
| `logs:entry`          | Admins only  | One backend log line, for the live log viewer (off with `DISABLE_LOGS_VIEWER`) |

### Emulator streaming

Sent to the user's tabs while an [emulator streaming](../using/emulator-streaming.md) session runs. Each payload names the `platform`, the `container`, and the `claimed_at` timestamp of the claim it belongs to, so a tab can ignore events meant for an older claim of the same container:

| Event                     | Extra fields                                                                                         |
| ------------------------- | ---------------------------------------------------------------------------------------------------- |
| `streaming:launch-phase`  | `phase`, the broker's extraction phase                                                               |
| `streaming:launch-ready`  | `host`, `resume`, and the RetroArch `core` and `core_tier` the session booted                        |
| `streaming:launch-failed` | `detail`, plus `refusals` and `refusals_truncated` when the broker refused an imported save or state |
| `streaming:session-ended` | `ended_by`, `reason`, `ended_at`, `rom_id`, `rom_name` and `desktop`                                 |

### Netplay

Netplay runs on `/netplay/socket.io`, on a separate channel, so a client there can never address the per-user or admin rooms of the main endpoint. RomM's player connects to it over the WebSocket transport only, because long polling breaks when gunicorn runs more than one worker.

| Event                                                              | Who may send it                                                                                              |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| `open-room`                                                        | A signed-in user with `roms.read` who can see the ROM named by `extra.game_id` (a ROM id)                    |
| `join-room`                                                        | For a room with a password, anyone who sends the right one. For a room without, the same rule as `open-room` |
| `leave-room`, `webrtc-signal`, `data-message`, `snapshot`, `input` | Players already in the room                                                                                  |

The room password travels as a top-level `password` field beside `extra`, which is where EmulatorJS sends it:

```json
{
    "extra": {
        "sessionid": "a1b2c3",
        "userid": "player-1",
        "room_name": "Friday co-op",
        "game_id": "123",
        "player_name": "alice"
    },
    "maxPlayers": 2,
    "password": "hunter2"
}
```

Both events answer through the socket.io acknowledgement with an error string, such as `Not authorized to open a room for this game` or `Incorrect password`, when they fail. Over REST, `GET /api/netplay/list?game_id=<rom id>` lists a game's open rooms. It requires `roms.read` and returns `404` for a ROM the caller can't see.

## Reverse-proxy requirements

Every reverse-proxy setup must forward the WebSocket upgrade. The recipes in [Reverse Proxy](../install/reverse-proxy.md) all keep WebSockets on by default. The main UI falls back to HTTP long polling when the upgrade fails, but netplay has no fallback and stops working outright.

Common breakages:

- Nginx without `proxy_set_header Upgrade $http_upgrade` and `Connection "upgrade"`
- Cloudflare with WebSockets disabled in Network settings
- Traefik without the default passthrough middlewares

A broken WS typically shows up as HTTP 400 on the upgrade request plus a flood of `WebSocket connection failed` errors in the browser console. [Authentication Troubleshooting → WebSockets](../troubleshooting/authentication.md#400-bad-request-on-the-websocket-endpoint) covers the diagnosis.
