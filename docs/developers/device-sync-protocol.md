---
title: Device Sync Protocol
description: Wire-level reference for RomM's save/state/play-session sync, for companion-app developers.
---

# Device Sync Protocol

Wire-level reference for the protocol RomM uses for bidirectional sync with companion apps. End-user view in [Saves & States](../using/saves-and-states.md). Operator-side SSH transport in [SSH Sync](../ecosystem/ssh-sync.md).

## Primitives

- **Device**: a registered endpoint, bound to a [Client API Token](../ecosystem/client-api-tokens.md).
- **Sync session**: one atomic bidirectional run (pull, push, conflict reconcile, play-session ingest).
- **Play session**: per-ROM playtime record. Posted standalone or batched at sync end.

## Authentication

Every call: `Authorization: Bearer rmm_...`. Required scopes:

| Endpoint family              | Scope                                                         |
| ---------------------------- | ------------------------------------------------------------- |
| `/devices/*`                 | `devices.read`, `devices.write`                               |
| `/sync/*`                    | `assets.read`, `assets.write`, `devices.write`                |
| `/play-sessions/*`           | `me.read`, `me.write` (read own), `users.read` (read others') |
| `/assets/*` (save/state I/O) | `assets.read`, `assets.write`                                 |

## Registering a device

After [pairing](../ecosystem/client-api-tokens.md#device-pairing):

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
  "paths": { "roms": "/roms", "saves": "/saves", "states": "/saves/states" }
}
```

Response includes `id`, which the device caches for subsequent calls.

`sync_mode`: `pull_only` (server → device), `push_only` (device → server), `push_pull` (bidirectional, default).

## Sync negotiation

Device sends what it has. RomM returns what to do.

```http
POST /api/sync/negotiate
{
  "device_id": 17,
  "roms": [
    {
      "rom_id": 1234,
      "saves": [
        { "file": "mario.srm",   "mtime": "2026-04-18T09:42:01Z", "sha1": "abc..." },
        { "file": "mario.state", "mtime": "2026-04-18T09:45:00Z", "sha1": "def..." }
      ]
    }
  ]
}
```

Response is a list of operations:

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "operations": [
    { "type": "upload",   "rom_id": 1234, "file": "mario.srm",   "destination": "/api/saves" },
    { "type": "download", "rom_id": 5678, "file": "zelda.srm",   "source": "/api/saves/42/content", "dest_path": "/saves/zelda.srm" },
    { "type": "conflict", "rom_id": 9999, "file": "tetris.srm",  "resolution": "keep_both" },
    { "type": "noop",     "rom_id": 1111, "file": "goldeneye.srm" }
  ]
}
```

| Op         | Meaning                                                                                                           |
| ---------- | ----------------------------------------------------------------------------------------------------------------- |
| `upload`   | Device `POST`s the file to `destination`.                                                                         |
| `download` | Device `GET`s `source` and writes to `dest_path`.                                                                 |
| `conflict` | Both sides newer. `resolution` ∈ `keep_both` (default), `server_wins`, `device_wins`.                             |
| `noop`     | Hashes match, nothing to do.                                                                                      |

Upload (`POST /api/saves`, multipart) and download (`GET /api/saves/{id}/content`) both require the bearer token.

## Completing a session

```http
POST /api/sync/sessions/{session_id}/complete
{
  "operations_completed": 15,
  "operations_failed": 1,
  "play_sessions": [
    { "rom_id": 1234, "start": "2026-04-18T09:00:00Z", "end": "2026-04-18T09:45:00Z", "duration_seconds": 2700 }
  ]
}
```

Closes the session and ingests batched play sessions in one call.

## Play sessions (standalone)

Without a full sync run:

```http
POST /api/play-sessions
[
  { "rom_id": 1234, "start": "...", "end": "...", "device_id": 17 }
]
```

Up to 100 per request.

## Rate limits and polling

No strict limits in 5.0. Sync once per session, not per save. Don't poll `/api/sync/negotiate` tightly: Grout defaults to every 15 minutes on Wi-Fi. No push channel yet, so polling is the only model.

## See also

- [Client API Tokens](../ecosystem/client-api-tokens.md): auth and pairing
- [API Authentication](api-authentication.md): general auth primer
- [API Reference](api-reference.md): full endpoint catalogue
- [SSH Sync](../ecosystem/ssh-sync.md): alternative transport
- [Argosy](../ecosystem/first-party-apps.md#argosy-launcher), [Grout](../ecosystem/first-party-apps.md#grout): reference client implementations
