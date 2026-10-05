---
title: Device Sync Protocol
description: Wire-level reference for save/state/play-session sync
---

# Device Sync Protocol

This page documents the protocol RomM uses for bidirectional sync with companion apps. The end-user view is in [Saves & States](../using/saves-and-states.md), and the operator-side SSH transport is in [SSH Sync](ssh-sync.md).

## Primitives

- **Device**: a registered endpoint owned by a user, identified by a string UUID.
- **Sync session**: one negotiate/complete run, identified by an integer ID.
- **Operation**: one action the server asks the device to take for a save (`upload`, `download`, `conflict`, `delete`, `no_op`).
- **Play session**: per-ROM playtime record, posted standalone or batched at sync end.

## Authentication

The sync endpoints accept either:

- a [Client API Token](client-api-tokens.md): `Authorization: Bearer rmm_...`
- a normal web session (see [API Authentication](api-authentication.md#session-login-browsers)): the `romm_session` cookie. Requests that change state also need the `romm_csrftoken` cookie, with its value repeated in an `X-CSRFToken` header. Bearer-token requests skip this check.

Required scopes:

| Endpoint                                                | Scope                                                  |
| ------------------------------------------------------- | ------------------------------------------------------ |
| `POST /api/devices`                                     | `devices.write`                                        |
| `POST /api/sync/negotiate`                              | `assets.read` + `devices.read`                         |
| `POST /api/sync/sessions/{id}/complete`                 | `devices.write`                                        |
| `GET /api/sync/sessions`, `GET /api/sync/sessions/{id}` | `devices.read`                                         |
| `POST /api/saves`, `PUT /api/saves/{id}`                | `assets.write`                                         |
| `GET /api/saves/{id}/content`                           | `assets.read`                                          |
| `POST /api/saves/{id}/downloaded`                       | `devices.write`                                        |
| `POST /api/play-sessions`                               | `roms.user.write`                                      |
| `GET /api/play-sessions`                                | `roms.user.read` (see [Play sessions](#play-sessions)) |
| `POST /api/sync/devices/{device_id}/push-pull`          | `devices.write`                                        |
| `PUT /api/devices/{device_id}`                          | `devices.write`                                        |
| `POST /api/devices/{device_id}/installs/claim`          | `devices.write` + `roms.read`, device-bound token      |
| `PUT /api/devices/{device_id}/installs/{request_id}`    | `devices.write`, device-bound token                    |

Passing `device_id` to the save endpoints also needs `devices.write` on upload and update, and `devices.read` on download. Without it the call returns `403`.

## Registering a device

After [pairing](client-api-tokens.md#device-pairing):

```http
POST /api/devices
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "RG35XX - Living Room",
  "platform": "muos",
  "client": "grout",
  "client_version": "1.4.0",
  "hostname": "rg35xx-livingroom.local",
  "mac_address": "aa:bb:cc:dd:ee:ff",
  "sync_mode": "api"
}
```

| Field             | Notes                                                                                                                           |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `name`            | Display name.                                                                                                                   |
| `platform`        | Device platform or OS.                                                                                                          |
| `client`          | Short slug for the app (for example `grout`). The activity feed shows it as the device type.                                    |
| `client_version`  | App version.                                                                                                                    |
| `ip_address`      | Device IP address.                                                                                                              |
| `mac_address`     | Used to match an existing device.                                                                                               |
| `hostname`        | Used to match an existing device.                                                                                               |
| `sync_mode`       | `api`, `file_transfer` or `push_pull`.                                                                                          |
| `sync_config`     | Mode-specific settings.                                                                                                         |
| `capabilities`    | Boolean flags the device reports about itself, for example `{ "remote_install": true }`. At most 32 keys of 1 to 64 characters. |
| `allow_existing`  | Default `true`. Return a matching existing device. `false` returns `409` if one exists.                                         |
| `allow_duplicate` | Default `false`. `true` always creates a new device and turns off `allow_existing`.                                             |
| `reset_syncs`     | Default `false`.                                                                                                                |

Registration is idempotent. The server looks for one of the user's devices with the same `mac_address`, or failing that the same `hostname` and `platform`, and returns it (`200`) instead of creating a second one (`201`), unless `allow_duplicate` is set. With `allow_existing: false`, a match returns `409` with `error: "device_exists"` and the existing `device_id`. Sending `capabilities` for an existing device updates them.

Response:

```json
{
    "device_id": "3f1c2b9e-8a4d-4c7e-9f21-6d0b5a7e1c34",
    "name": "RG35XX - Living Room",
    "created_at": "2026-04-18T09:00:00Z"
}
```

`device_id` is a string (a UUID). Cache it for subsequent calls.

`PUT /api/devices/{device_id}` updates a device with the same fields, plus `sync_enabled`. A device with `sync_enabled: false` gets `400` from negotiate until it's turned back on, which users can do from their [devices list](../using/devices.md). `DELETE /api/devices/{device_id}` removes a device, closes the sockets its tokens opened and drops its queued installs, but keeps the saves it uploaded.

## Sync negotiation

The device sends the saves it has and RomM returns what to do:

```http
POST /api/sync/negotiate
Content-Type: application/json

{
  "device_id": "3f1c2b9e-8a4d-4c7e-9f21-6d0b5a7e1c34",
  "saves": [
    {
      "rom_id": 1234,
      "file_name": "mario.srm",
      "slot": "autosave",
      "emulator": null,
      "content_hash": "9e107d9d372bb6826bd81d3542a419d6",
      "updated_at": "2026-04-18T09:42:01Z",
      "file_size_bytes": 8192
    }
  ],
  "rom_ids": [1234],
  "restore_unlisted": false,
  "emulators": null
}
```

- `device_id` is optional when the token is bound to a device, since the server works it out from the token. Otherwise leaving it out returns `400`.
- An unknown device returns `404`. A device with sync turned off returns `400`.
- `content_hash` is an MD5 hex digest of the file.
- `rom_ids` is an optional, read-only scope. Downloads are offered only for these ROMs, plus any ROM a save was sent for. Leaving a ROM out never deletes anything. The number of IDs per request is capped.
- `restore_unlisted` (default `false`) offers every current server save the device didn't list as a `download`, even one it already synced. Normally a save the device synced before and no longer lists is taken as deleted there and left alone. Set it for a client that never deletes saves itself, such as a browser whose storage can be evicted, so a missing save reads as lost and comes back.
- `emulators` (default `null`) limits pairing to server saves written by one of these emulators, so a save another emulator wrote into the same slot is neither paired nor offered. RomM's browser players send their own emulator here.
- Saves are paired on **(`rom_id`, `slot`)**. Send a stable slot such as `autosave`. A `null` slot marks an archival or manual save: it is never paired, so it always comes back as `upload`.
- Every negotiate opens a new session that lasts one launch, so one device can have several open at once (for example, two games running). A session nobody completes is marked failed by the scheduled sync session cleanup (`ENABLE_SCHEDULED_CLEANUP_SYNC_SESSIONS`, hourly at `23 * * * *` by default, set by `SCHEDULED_CLEANUP_SYNC_SESSIONS_CRON`) once it's 24 hours old.

Response:

```json
{
    "session_id": 42,
    "operations": [
        {
            "action": "download",
            "rom_id": 1234,
            "save_id": 99,
            "file_name": "mario.srm",
            "slot": "autosave",
            "emulator": null,
            "reason": "server save is newer",
            "server_updated_at": "2026-04-18T10:00:00Z",
            "server_content_hash": "e4d909c290d0fb1ca068ffaddf22cbd0"
        }
    ],
    "total_upload": 0,
    "total_download": 1,
    "total_conflict": 0,
    "total_no_op": 0,
    "total_delete": 0
}
```

| Action     | Meaning                                                                                                                              |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `upload`   | The server doesn't have this version. `save_id` is `null` and `slot` echoes the device's slot.                                       |
| `download` | The server has a newer save, or the device holds a version removed here. Fetch it using `save_id`. `slot` is the server save's slot. |
| `conflict` | Both sides changed. `save_id` and `slot` refer to the server save.                                                                   |
| `delete`   | The slot was emptied on the server. Remove the local copy. `save_id` is `null` and `slot` echoes the device's slot.                  |
| `no_op`    | Hashes match, nothing to do.                                                                                                         |

A `delete` keeps a device from uploading a save that was deleted on the server back to it.

Operations carry no URLs or local paths: the client builds the request from `save_id` (see [Moving bytes](#moving-bytes)) and decides where the file goes on disk.

A conflict carries no resolution, so the client decides what to do. One safe option is to keep both: upload the local copy as a `null`-slot (archival) save instead of overwriting the slot.

## Moving bytes

### Upload

```http
POST /api/saves?rom_id=1234&slot=autosave&device_id=<uuid>&session_id=42&content_hash=<md5>&overwrite=false&autocleanup=true&autocleanup_limit=10
Content-Type: multipart/form-data

saveFile=<file>
screenshotFile=<file, optional>
```

- With `overwrite=false` and a `device_id`, an upload to a slot that already holds a save returns `409` unless this device has synced the slot's latest save and nothing has changed since. That includes the device's first upload to a slot another device filled, so negotiate and download or resolve first. Without a `slot`, `409` only comes back when a save with the same file name changed since this device last synced it.
- `autocleanup=true` limits how many versions a slot keeps (`autocleanup_limit`, default 10).
- `content_hash` is the device's MD5 of the file it sent, the same value it sends to negotiate. The server stores it as the device's baseline for the save, so the next negotiate can tell that the device's copy hasn't changed.
- The response is the stored save, including its `id`.

To replace a version the client itself created, use `PUT /api/saves/{id}?device_id=<uuid>&content_hash=<md5>` with the same multipart body. There is no conflict guard on this call, so only use it on your own saves.

### Download

```http
GET /api/saves/{save_id}/content?device_id=<uuid>&session_id=42&optimistic=true
```

With `optimistic=true` (the default), the device is marked as synced for the save as soon as the file is served. With `optimistic=false`, it isn't marked until the client confirms:

```http
POST /api/saves/{save_id}/downloaded
Content-Type: application/json

{
  "device_id": "3f1c2b9e-8a4d-4c7e-9f21-6d0b5a7e1c34",
  "content_hash": "e4d909c290d0fb1ca068ffaddf22cbd0"
}
```

This records the device's sync baseline for the save. `content_hash` is optional: send the MD5 of the file as written. The server keeps it when an optimistic download already recorded which version it served, or when it matches the save's current hash. Otherwise it drops it.

## Completing a session

```http
POST /api/sync/sessions/{session_id}/complete
Content-Type: application/json

{
  "operations_completed": 15,
  "operations_failed": 1,
  "play_sessions": [
    {
      "rom_id": 1234,
      "save_slot": "autosave",
      "start_time": "2026-04-18T09:00:00Z",
      "end_time": "2026-04-18T09:45:00Z",
      "duration_ms": 2700000
    }
  ]
}
```

- `play_sessions` is optional. `save_slot` is optional. `end_time` must be after `start_time`, and both are truncated to whole seconds.
- Playtime can also be sent on its own to `POST /api/play-sessions`. Sending it there (with retries) means playtime is still recorded when a sync fails.
- The response is `{ session, play_session_ingest }`.
- An unknown session returns `404`. A session that was cancelled or failed on purpose returns `400`. One that the cleanup expired can still be completed, so its counts and playtime aren't lost.

## Play sessions

`GET /api/play-sessions` lists the caller's sessions, filtered by `rom_id`, `device_id`, `start_after` and `end_before`. Reading another device's sessions, or every device's at once, needs `devices.read`. A device-bound token without that scope can still read its own device's sessions by passing its own `device_id`. The server never fills in `device_id` from the token, so leaving it out lists every device and needs `devices.read`.

Play session responses have no `sync_session_id` field.

## Paging

`GET /api/play-sessions` and `GET /api/sync/sessions` share these page parameters:

| Parameter | Default | Range       |
| --------- | ------- | ----------- |
| `limit`   | `50`    | 1 to 10000  |
| `offset`  | `0`     | 0 and above |

On play sessions, `limit` is ignored when `start_after` or `end_before` is set, so a time window always comes back whole.

## Other endpoints

- `GET /api/sync/sessions` (filtered by `device_id`) and `GET /api/sync/sessions/{id}`: list and inspect sync sessions.
- `POST /api/sync/devices/{device_id}/push-pull`: push/pull sync for a device.

See the [API Reference](api-reference.md) for their full schemas.

## Installs on devices

Users can send a game to one of their devices from the web UI (see [Devices](../using/devices.md#install-on-device)), and the device downloads it the next time it's online. A device opts in by registering with the `remote_install` capability:

```json
{ "capabilities": { "remote_install": true } }
```

Only devices with that flag are offered as install targets. Every install endpoint answers `404` when the server sets `DEVICE_INSTALL_ENABLED=false`, and `GET /api/heartbeat` reports it under `DEVICE_INSTALL` (`ENABLED` and `EXCLUDED_PLATFORM_SLUGS`).

### Request lifecycle

An install request is a JSON object:

```json
{
    "id": "b6f1d3c2-6a0e-4d55-9f3e-7f6b1c2d9e10",
    "user_id": 1,
    "device_id": "3f1c2b9e-8a4d-4c7e-9f21-6d0b5a7e1c34",
    "rom_id": 1234,
    "file_ids": [5678, 5679],
    "status": "pending",
    "reason": null,
    "created_at": "2026-10-05T09:00:00Z",
    "updated_at": "2026-10-05T09:00:00Z"
}
```

`file_ids` lists the ROM's game, update and DLC files on disk, which is what the device should download, for example with `GET /api/roms/{rom_id}/content/{file_name}?file_ids=5678,5679`.

| Status              | Meaning                                                   |
| ------------------- | --------------------------------------------------------- |
| `pending`           | Queued, waiting for the device to claim it                |
| `taken`             | Claimed by the device, which is downloading it            |
| `done`              | The device installed it                                   |
| `already_installed` | The device already had it                                 |
| `failed`            | The device couldn't install it, with an optional `reason` |
| `cancelled`         | The user cancelled it before it finished                  |

`done`, `already_installed`, `failed` and `cancelled` end a request, and an ended request is gone from every list. A request nobody touches expires `DEVICE_INSTALL_REQUEST_TTL_DAYS` days (2 by default) after its last change.

### Endpoints

| Method and path                                         | Called by | Description                                                                                            |
| ------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------ |
| `POST /api/devices/{device_id}/installs`                | Web UI    | Queue `{ "rom_id": 1234 }`. `201` with a new request, or `200` with the live one for the same pair     |
| `GET /api/devices/{device_id}/installs`                 | Either    | The device's `pending` and `taken` requests, oldest first                                              |
| `POST /api/devices/{device_id}/installs/claim`          | Device    | Take every `pending` request and return all the device holds `taken`, oldest first                     |
| `PUT /api/devices/{device_id}/installs/{request_id}`    | Device    | Report `{ "status": "done" \| "already_installed" \| "failed", "reason": "..." }` on a `taken` request |
| `DELETE /api/devices/{device_id}/installs/{request_id}` | Either    | Cancel a `pending` or `taken` request                                                                  |
| `GET /api/devices/online`                               | Web UI    | IDs of the caller's devices with an open `/devices` socket                                             |
| `GET /api/roms/{id}/installs`                           | Web UI    | The caller's open requests for a ROM, across devices                                                   |

Queueing needs `devices.write` and `roms.read`. A ROM the user can't see returns `404`, and a device without the `remote_install` capability, a ROM on a platform in `DEVICE_INSTALL_EXCLUDED_PLATFORM_SLUGS` or a ROM with no installable file returns `400`. Claiming and reporting need a token bound to that same device (see [Client API Tokens](client-api-tokens.md#device-bound-tokens)), and any other caller gets `403`. A report or cancel on a request in the wrong status returns `409`, and `reason` is capped at 500 characters. Each report also sends the user a notification.

### The `/devices` socket

A device learns about requests over this Socket.IO namespace. Connect with a device-bound client token holding `devices.read`, passed either in the handshake's `auth` payload as `{ "token": "rmm_..." }` or as an `Authorization: Bearer` header. Any other credential is refused, and so is every connection while installs are disabled.

The server sends two events, each with a payload of `{ "id": "<request id>", "rom_id": 1234 }`:

| Event               | Meaning                                                               |
| ------------------- | --------------------------------------------------------------------- |
| `install:queued`    | A request is waiting. Claim it with `POST .../installs/claim`         |
| `install:cancelled` | The user cancelled a request. Stop downloading it if it's in progress |

The open socket also marks the device as online until the server drops it, which happens when the token expires or is revoked, or when the device is deleted. Events sent while the device is offline aren't replayed, so claim on every connect to pick up whatever queued in the meantime.

## Rate limits and polling

- Sync once per session, not per save
- Don't poll `/api/sync/negotiate` tightly
- Nothing tells a device to start a sync. The [`/devices` Socket.IO namespace](#the-devices-socket) only carries install requests, so the device decides when to negotiate

## See also

- [Client API Tokens](client-api-tokens.md): auth and pairing
- [API Authentication](api-authentication.md): general auth primer
- [API Reference](api-reference.md): full endpoint catalogue
- [SSH Sync](ssh-sync.md): alternative transport
- [Argosy](../ecosystem/first-party-apps.md#argosy-launcher), [Grout](../ecosystem/first-party-apps.md#grout): reference client implementations
