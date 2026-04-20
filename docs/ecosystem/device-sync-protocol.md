---
title: Device Sync Protocol
description: Wire-level reference for RomM's save/state/play-session sync protocol, for companion-app developers.
---

# Device Sync Protocol

This page documents the **wire-level protocol** RomM uses for bidirectional sync between itself and companion apps. If you're building a companion app, this is your reference.

End users: this is under the hood. You don't need to read it. See [Saves & States](../using/saves-and-states.md) and [SSH Sync](../administration/ssh-sync.md) for operator/user views.

## The three primitives

1. **Devices**: registered endpoints. Each device has a name, hostname, and links to a specific user's [Client API Token](client-api-tokens.md).
2. **Sync sessions**: an atomic bidirectional sync run. One session handles "pull anything new from server" + "push anything new from device" + "reconcile conflicts" + "ingest play sessions".
3. **Play sessions**: per-session records of ROM playtime. Independent of sync but commonly posted in batch at the end of a sync run.

## Authentication

Every API call requires a valid token:

```http
Authorization: Bearer rmm_...
```

Required scopes:

| Endpoint family              | Scope                                                         |
| ---------------------------- | ------------------------------------------------------------- |
| `/devices/*`                 | `devices.read`, `devices.write`                               |
| `/sync/*`                    | `assets.read`, `assets.write`, `devices.write`                |
| `/play-sessions/*`           | `me.read`, `me.write` (read own), `users.read` (read others') |
| `/assets/*` (save/state I/O) | `assets.read`, `assets.write`                                 |

## Registering a device

After [pairing](client-api-tokens.md#device-pairing), the device registers itself:

```http
POST /api/devices
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "RG35XX - Living Room",
  "platform": "muos",
  "hostname": "rg35xx-livingroom.local",
  "mac": "aa:bb:cc:dd:ee:ff",
  "sync_mode": "push_pull",
  "paths": {
    "roms":   "/roms",
    "saves":  "/saves",
    "states": "/saves/states"
  }
}
```

Response:

```json
{
  "id": 17,
  "name": "RG35XX - Living Room",
  ...
}
```

The device remembers `id` for all subsequent calls.

### Sync modes

| Mode        | Behaviour                                                   |
| ----------- | ----------------------------------------------------------- |
| `pull_only` | Server only pushes, and device-side changes are ignored.    |
| `push_only` | Device pushes saves up, and server changes never flow down. |
| `push_pull` | Bidirectional (most common).                                |

## Sync negotiation

The core of the protocol. A device asks RomM: "here's what I have, tell me what to do."

### Request

```http
POST /api/sync/negotiate
Authorization: Bearer <token>
Content-Type: application/json

{
  "device_id": 17,
  "roms": [
    {
      "rom_id": 1234,
      "saves": [
        { "file": "mario.srm",  "mtime": "2026-04-18T09:42:01Z", "sha1": "abc..." },
        { "file": "mario.state", "mtime": "2026-04-18T09:45:00Z", "sha1": "def..." }
      ]
    },
    ...
  ]
}
```

The device reports every save/state it knows about for each ROM: filename, last-modified time, and hash.

### Response

RomM returns a set of **operations** the device should execute:

```json
{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "operations": [
        {
            "type": "upload",
            "rom_id": 1234,
            "file": "mario.srm",
            "destination": "/api/saves",
            "reason": "server_newer"
        },
        {
            "type": "download",
            "rom_id": 5678,
            "file": "zelda.srm",
            "source": "/api/saves/42/content",
            "dest_path": "/saves/zelda.srm"
        },
        {
            "type": "conflict",
            "rom_id": 9999,
            "file": "tetris.srm",
            "server_mtime": "...",
            "device_mtime": "...",
            "resolution": "keep_both"
        },
        {
            "type": "noop",
            "rom_id": 1111,
            "file": "goldeneye.srm",
            "reason": "already_synced"
        }
    ]
}
```

### Operation types

- **`upload`**: device pushes the file to the server.
- **`download`**: device pulls the file from the server.
- **`conflict`**: both sides have newer versions. Resolution strategy:
    - `keep_both`: rename and keep both copies.
    - `server_wins` / `device_wins`: overwrite the other.
    - Default is `keep_both`.
- **`noop`**: nothing to do because hashes match

### Execution

For each operation the device runs the appropriate HTTP call. For an `upload`:

```http
POST /api/saves
Authorization: Bearer <token>
Content-Type: multipart/form-data

[file upload]
```

For a `download`:

```http
GET /api/saves/{id}/content
Authorization: Bearer <token>
```

## Completing a sync session

Once the device has executed every operation:

```http
POST /api/sync/sessions/{session_id}/complete
Authorization: Bearer <token>
Content-Type: application/json

{
  "operations_completed": 15,
  "operations_failed": 1,
  "play_sessions": [
    {
      "rom_id": 1234,
      "start": "2026-04-18T09:00:00Z",
      "end":   "2026-04-18T09:45:00Z",
      "duration_seconds": 2700
    },
    ...
  ]
}
```

This closes out the sync session and ingests any play sessions from the device in one call.

## Play sessions (standalone)

If you just want to report a play session without running a full sync:

```http
POST /api/play-sessions
Authorization: Bearer <token>
Content-Type: application/json

[
  {
    "rom_id": 1234,
    "start": "2026-04-18T09:00:00Z",
    "end":   "2026-04-18T09:45:00Z",
    "device_id": 17
  }
]
```

Send up to 100 per request.

## SSH-based sync (alternative)

For handhelds where the RomM server connects over SSH instead of the device polling HTTPS, see [SSH Sync](../administration/ssh-sync.md). The RomM-side push-pull task reads the device's filesystem over SSH rather than going through API calls. Same data, different transport.

Companion apps generally prefer the API model. SSH-based sync exists mostly for cases where the device can't run a TLS client reliably.

## Rate limits

Not strict in 5.0. Reasonable rule of thumb:

- Sync once per session (not every save).
- Large bursts (initial sync of a full library) are fine, and RomM handles them.
- Don't poll `/api/sync/negotiate` in a tight loop, because it's expensive server-side.

## Event notifications

Currently polling-only. Companion apps check `/api/sync/negotiate` periodically (Grout defaults to every 15 minutes on Wi-Fi). Future versions may add a push notification channel. Until then, polling.

## See also

- [Client API Tokens](client-api-tokens.md): auth + pairing
- [API Authentication](../developers/api-authentication.md): general auth primer
- [API Reference](../developers/api-reference.md): full endpoint catalogue
- [SSH Sync](../administration/ssh-sync.md): alternative transport for handhelds
- [Argosy](argosy.md), [Grout](grout.md): reference client implementations
