---
title: API Reference
description: Catalogue of RomM's REST API. Authoritative interactive docs live on each instance.
---

# API Reference

RomM's REST API is documented via **OpenAPI 3.0**. The spec is the source of truth. This page catalogues what's there, but every running RomM instance serves its own interactive browser with live "try it out" functionality.

## Interactive docs

Every RomM instance hosts two renderings of its own spec:

- **Swagger UI** at `{romm_url}/api/docs`: explore + try endpoints inline.
- **ReDoc** at `{romm_url}/api/redoc`: cleaner reading layout.

The raw spec:

```text
{romm_url}/openapi.json
```

For code generation, Postman imports, and schema-validation libraries, see [Consuming OpenAPI](openapi.md).

## Base URL

```text
{romm_url}/api
```

## Auth

Every write endpoint (and most read endpoints) requires a credential. Five modes supported:

- **Session cookie:** from the web UI.
- **HTTP Basic:** username + password header.
- **OAuth2 Bearer:** JWT access token.
- **Client API Token:** long-lived `rmm_...` bearer token.
- **OIDC session:** after IdP callback, same as a regular session.

Full walkthrough in [API Authentication](api-authentication.md).

## Endpoint groups

Every endpoint belongs to a group. Summaries below. The interactive docs at `/api/docs` have full request/response schemas.

### Auth & users

- `POST /api/auth/login`, `/api/auth/logout`: session login/logout.
- `POST /api/token`: OAuth2 token endpoint (password + refresh grants).
- `GET /api/auth/openid`, `/api/oauth/openid`: OIDC flow.
- `POST /api/auth/forgot-password`, `/api/auth/reset-password`: password reset.
- `GET/POST/PUT/DELETE /api/users`: user management. See [Users & Roles](../administration/users-and-roles.md).
- `POST /api/users/register`: claim an invite link.
- `POST /api/users/invite-link`: generate one.

### ROMs

- `GET /api/roms`: list with filters, pagination, search.
- `GET /api/roms/{id}`: single ROM details.
- `POST /api/roms/upload/{start,chunk,complete,cancel}`: chunked upload.
- `PUT /api/roms/{id}`: update metadata.
- `PUT /api/roms/{id}/props`: update per-user data (rating, status).
- `POST /api/roms/delete`: bulk delete.
- `GET /api/roms/{id}/content/{filename}`: download.
- `GET /api/roms/download?ids=...`: bulk zip download.
- `GET /api/roms/by-hash`, `/api/roms/by-metadata-provider`: lookup helpers.

### ROM notes, files, manuals

- `GET/POST/PUT/DELETE /api/roms/{id}/notes`: per-ROM notes (optional public).
- `GET /api/roms/{id}/files/content/{filename}`: individual file in a multi-file ROM.
- `POST/DELETE /api/roms/{id}/manuals`: PDF manual management.

### Platforms

- `GET /api/platforms`: list.
- `GET /api/platforms/supported`: everything RomM recognises (same data as [Supported Platforms](../platforms/supported-platforms.md)).
- `PUT/DELETE /api/platforms/{id}`: edit or delete.

### Collections

- `GET/POST/PUT/DELETE /api/collections`: standard collections.
- `POST/DELETE /api/collections/{id}/roms`: add/remove ROMs.
- `GET/POST/PUT/DELETE /api/collections/smart`: [Smart Collections](../using/smart-collections.md).
- `GET /api/collections/virtual`: read-only [Virtual Collections](../using/virtual-collections.md).

### Assets: saves, states, screenshots

- `GET/POST/PUT /api/saves`: save files. See [Saves & States](../using/saves-and-states.md).
- `POST /api/saves/delete`: bulk delete.
- `GET/POST/PUT /api/states`: emulator states.
- `POST /api/screenshots`: screenshot upload.

### Firmware

- `GET/POST/DELETE /api/firmware`: firmware management. See [Firmware Management](../administration/firmware-management.md).
- `GET /api/firmware/{id}/content/{filename}`: download.

### Devices & sync

- `GET/POST/PUT/DELETE /api/devices`: registered device management.
- `POST /api/sync/negotiate`: sync-session negotiation.
- `POST /api/sync/sessions/{id}/complete`: close a sync session with ingested play sessions.
- `POST /api/devices/{id}/push-pull`: trigger manual sync.

See [Device Sync Protocol](../ecosystem/device-sync-protocol.md) for the wire-level walkthrough.

### Play sessions

- `GET/POST/DELETE /api/play-sessions`: ingest and query play sessions (up to 100 per POST).

### Client API tokens

- `GET/POST/DELETE /api/client-tokens`: user's tokens.
- `PUT /api/client-tokens/{id}/regenerate`: regenerate the secret.
- `POST /api/client-tokens/{id}/pair`: generate a pairing code.
- `POST /api/client-tokens/exchange`: exchange a pairing code for a token.
- `GET /api/client-tokens/pair/{code}/status`: poll pairing status.
- `GET /api/client-tokens/all`, `DELETE /api/client-tokens/{id}/admin`: admin-only.

See [Client API Tokens](../ecosystem/client-api-tokens.md) for the full flow.

### Search

- `GET /api/search/roms`: search across metadata providers (IGDB, Moby, SS, Flashpoint, LaunchBox).
- `GET /api/search/cover`: alternate cover search via SteamGridDB.

### Tasks

- `GET /api/tasks`, `/api/tasks/status`: what's registered, what's running.
- `POST /api/tasks/run/{task_name}`: trigger on demand (requires `tasks.run`).

### Configuration

- `GET /api/config`: current config (parts of it public, parts require auth).
- `POST/DELETE /api/config/system/platforms`: add/remove platform bindings.
- `POST/DELETE /api/config/system/versions`: add/remove version mappings.
- `POST/DELETE /api/config/exclude`: add/remove exclusion rules.

### Stats

- `GET /api/stats`: aggregate counts + disk usage.
- `GET /api/stats?include_platform_stats=true`: per-platform breakdown.

### Feeds

- `GET /api/feeds/webrcade`: WebRcade.
- `GET /api/feeds/tinfoil`: Nintendo Switch.
- `GET /api/feeds/pkgi/{psvita|psp}/{game|dlc}`: PS Vita / PSP.
- `GET /api/feeds/fpkgi/{ps4|ps5}`: PS4 / PS5.
- `GET /api/feeds/kekatsu/{nds}`: Nintendo DS.
- `GET /api/feeds/pkgj/{psx|psvita|psp}`: legacy pkgj.

See [Feeds](../reference/feeds.md) for format details per feed.

### Exports

- `POST /api/export/gamelist-xml`: ES-DE / Batocera format.
- `POST /api/export/pegasus`: Pegasus frontend format.

See [Exports](../reference/exports.md).

### Heartbeat

- `GET /api/heartbeat`: health + config snapshot. Safe to scrape from uptime monitors.
- `GET /api/heartbeat/metadata/{provider}`: per-provider health.

### Raw

- `GET /api/raw/assets/{path}`: direct asset passthrough for advanced integrations.

### Netplay

- `GET /api/netplay/list?game_id=...`: active Netplay rooms for a game.
- WebSocket at `/netplay/socket.io`: room coordination. See [WebSockets](websockets.md).

## WebSockets

REST isn't the only surface. Two Socket.IO endpoints cover live-update and coordination use cases: [WebSockets](websockets.md).

## Versioning

RomM's API follows SemVer along with the rest of RomM:

- **Breaking changes only in major versions.** Endpoint removal, required-parameter changes, incompatible response-schema shifts.
- **Minor versions add** endpoints, optional parameters, optional response fields.
- **Patch versions fix** bugs without schema changes.

For reproducible builds, pin the OpenAPI spec version at the same RomM version you target. See [Consuming OpenAPI → Versioning](openapi.md#versioning).

## See also

- [API Authentication](api-authentication.md): auth modes in detail.
- [Consuming OpenAPI](openapi.md): codegen + schema validation.
- [WebSockets](websockets.md): Socket.IO endpoints.
- [Client API Tokens](../ecosystem/client-api-tokens.md): recommended companion-app auth.
- [Device Sync Protocol](../ecosystem/device-sync-protocol.md): sync endpoints in depth.
