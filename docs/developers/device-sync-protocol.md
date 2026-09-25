---
title: Device Sync Protocol
description: Wire-level reference for save/state/play-session sync
---

# Device Sync Protocol

This is a reference for the protocol RomM uses for bidirectional sync with companion apps. End-user view in [Saves & States](../using/saves-and-states.md), with operator-side SSH transport in [SSH Sync](ssh-sync.md).

## Primitives

- **Device**: a registered endpoint owned by a user, identified by a string UUID.
- **Sync session**: one negotiate/complete run, identified by an integer ID.
- **Operation**: one action the server asks the device to take for a save (`upload`, `download`, `conflict`, `no_op`).
- **Play session**: per-ROM playtime record, posted standalone or batched at sync end.

## Authentication

The sync endpoints accept either:

- a [Client API Token](client-api-tokens.md): `Authorization: Bearer rmm_...`
- a normal web session: the session cookie plus the CSRF header, as described in [API Authentication](api-authentication.md).

Required scopes:

| Endpoint                                                | Scope                          |
| ------------------------------------------------------- | ------------------------------ |
| `POST /api/devices`                                     | `devices.write`                |
| `POST /api/sync/negotiate`                              | `assets.read` + `devices.read` |
| `POST /api/sync/sessions/{id}/complete`                 | `devices.write`                |
| `GET /api/sync/sessions`, `GET /api/sync/sessions/{id}` | `devices.read`                 |
| `POST /api/saves`, `PUT /api/saves/{id}`                | `assets.write`                 |
| `GET /api/saves/{id}/content`                           | `assets.read`                  |
| `POST /api/saves/{id}/downloaded`                       | `devices.write`                |
| `POST /api/play-sessions`                               | `roms.user.write`              |

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

| Field             | Notes                                                                                        |
| ----------------- | -------------------------------------------------------------------------------------------- |
| `name`            | Display name.                                                                                |
| `platform`        | Device platform or OS.                                                                       |
| `client`          | Short slug for the app (for example `grout`). The activity feed shows it as the device type. |
| `client_version`  | App version.                                                                                 |
| `ip_address`      | Device IP address.                                                                           |
| `mac_address`     | Used to match an existing device.                                                            |
| `hostname`        | Used to match an existing device.                                                            |
| `sync_mode`       | `api`, `file_transfer` or `push_pull`.                                                       |
| `sync_config`     | Mode-specific settings.                                                                      |
| `allow_existing`  | Default `true`. Return a matching existing device instead of creating one.                   |
| `allow_duplicate` | Default `false`. `true` always creates a new device and turns off `allow_existing`.          |
| `reset_syncs`     | Default `false`.                                                                             |

Registration is idempotent. The server matches an existing device for the user on (`mac_address`, `hostname`, `platform`) and returns it instead of creating a second one, unless `allow_duplicate` is set.

Response:

```json
{
    "device_id": "3f1c2b9e-8a4d-4c7e-9f21-6d0b5a7e1c34",
    "name": "RG35XX - Living Room",
    "created_at": "2026-04-18T09:00:00Z"
}
```

`device_id` is a string (a UUID). Cache it for subsequent calls.

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
  "rom_ids": [1234]
}
```

- `device_id` is optional when the token is bound to a device, since the server works it out from the token. Otherwise leaving it out returns `400`.
- An unknown device returns `404`. A device with sync turned off returns `400`.
- `content_hash` is an MD5 hex digest of the file.
- `rom_ids` is an optional, read-only scope. Downloads are offered only for these ROMs, plus any ROM a save was sent for. Leaving a ROM out never deletes anything. The number of IDs per request is capped.
- Saves are paired on **(`rom_id`, `slot`)**. Send a stable slot such as `autosave`. A `null` slot marks an archival or manual save: it is never paired, so it always comes back as `upload`.
- A new negotiate cancels any session still active for that device.

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
    "total_no_op": 0
}
```

| Action     | Meaning                                                                                        |
| ---------- | ---------------------------------------------------------------------------------------------- |
| `upload`   | The server doesn't have this version. `save_id` is `null` and `slot` echoes the device's slot. |
| `download` | The server has a newer save. Fetch it using `save_id`. `slot` is the server save's slot.       |
| `conflict` | Both sides changed. `save_id` and `slot` refer to the server save.                             |
| `no_op`    | Hashes match, nothing to do.                                                                   |

Operations carry no URLs or local paths: the client builds the request from `save_id` (see [Moving bytes](#moving-bytes)) and decides where the file goes on disk.

A conflict carries no resolution, so the client decides what to do. One safe option is to keep both: upload the local copy as a `null`-slot (archival) save instead of overwriting the slot.

## Moving bytes

### Upload

```http
POST /api/saves?rom_id=1234&slot=autosave&device_id=<uuid>&session_id=42&overwrite=false&autocleanup=true&autocleanup_limit=10
Content-Type: multipart/form-data

saveFile=<file>
screenshotFile=<file, optional>
```

- With `overwrite=false`, the server returns `409` if the slot has moved on since this device last synced it, instead of overwriting another device's progress.
- `autocleanup=true` limits how many versions a slot keeps (`autocleanup_limit`, default 10).
- The response is the stored save, including its `id`.

To replace a version the client itself created, use `PUT /api/saves/{id}?device_id=<uuid>` with the same multipart body. There is no conflict guard on this call, so only use it on your own saves.

### Download

```http
GET /api/saves/{save_id}/content?device_id=<uuid>&session_id=42&optimistic=true
```

With `optimistic=true` (the default), the device is marked as synced for the save as soon as the file is served. With `optimistic=false`, it isn't marked until the client confirms:

```http
POST /api/saves/{save_id}/downloaded
Content-Type: application/json

{ "device_id": "3f1c2b9e-8a4d-4c7e-9f21-6d0b5a7e1c34" }
```

This records the device's sync baseline for the save.

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
- Completing a session that isn't pending or in progress returns `400`.

## Other endpoints

- `GET /api/sync/sessions` and `GET /api/sync/sessions/{id}`: list and inspect sync sessions.
- `POST /api/sync/devices/{device_id}/push-pull`: push/pull sync for a device.

See the [API Reference](api-reference.md) for their full schemas.

## Rate limits and polling

- Sync once per session, not per save
- Don't poll `/api/sync/negotiate` tightly
- No push channel yet, so polling is the only model

## See also

- [Client API Tokens](client-api-tokens.md): auth and pairing
- [API Authentication](api-authentication.md): general auth primer
- [API Reference](api-reference.md): full endpoint catalogue
- [SSH Sync](ssh-sync.md): alternative transport
- [Argosy](../ecosystem/first-party-apps.md#argosy-launcher), [Grout](../ecosystem/first-party-apps.md#grout): reference client implementations
