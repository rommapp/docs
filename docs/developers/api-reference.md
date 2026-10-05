---
title: API Reference
description: Catalogue of the API. Authoritative interactive docs live on each instance.
---

## Interactive docs

Every RomM instance hosts two renderings of its own spec:

- **Swagger UI** at `{romm_url}/api/docs`: explore + try endpoints inline
- **ReDoc** at `{romm_url}/api/redoc`: cleaner reading layout

The raw spec:

```text
{romm_url}/openapi.json
```

For code generation, see [Consuming OpenAPI](openapi.md).

## Starting a scan

Clients that authenticate with a token rather than a session cookie can queue a library scan with `POST /api/tasks/scan`, which needs the `tasks.run` scope and takes the same `ScanPayload` body as the `scan` socket event (see [WebSockets → Scans](websockets.md#scans)). Leave the body out for a quick scan of the whole library:

```bash
curl -X POST https://demo.romm.app/api/tasks/scan \
     -H "Authorization: Bearer rmm_..." \
     -H "Content-Type: application/json" \
     -d '{"type": "unmatched", "platforms": [12], "apis": ["igdb", "ss"]}'
```

| Status | Meaning                                                                                     |
| ------ | ------------------------------------------------------------------------------------------- |
| `202`  | Queued. The response's `task_id` can be followed on `GET /api/tasks/{task_id}`              |
| `409`  | A library scan is already queued or running. A scan limited to `roms_ids` is still accepted |
| `422`  | The body has an unknown key or an invalid value                                             |
| `503`  | No scan worker is running, so the scan can't be queued                                      |

`POST /api/tasks/run/{task_name}` likewise returns `409` when a task that only runs one at a time, such as Convert library, is already queued or running. `GET /api/tasks` flags destructive tasks such as Convert library, which replaces the original files, with `destructive: true`, so a client can ask for confirmation before running one.

## WebSockets

Alongside REST, two socket.io endpoints cover live-update and coordination use cases (see [WebSockets](websockets.md)).

## Versioning

The API follows SemVer along with the rest of RomM:

- **Breaking changes only in major versions.** Endpoint removal, required-parameter changes, incompatible response-schema shifts
- **Minor versions add** endpoints, optional parameters, optional response fields.
- **Patch versions fix** bugs without schema changes.

## See also

- [API Authentication](api-authentication.md): auth modes in detail
- [Consuming OpenAPI](openapi.md): codegen + schema validation
- [WebSockets](websockets.md): socket.io endpoints
- [Client API Tokens](client-api-tokens.md): recommended companion-app auth
- [Device Sync Protocol](device-sync-protocol.md): sync endpoints in depth
