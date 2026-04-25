---
title: API Reference
description: Catalogue of RomM's API. Authoritative interactive docs live on each instance.
---

## Interactive docs

Every RomM instance hosts two renderings of its own spec:

- **Swagger UI** at `{romm_url}/api/docs`: explore + try endpoints inline
- **ReDoc** at `{romm_url}/api/redoc`: cleaner reading layout

The raw spec:

```text
{romm_url}/openapi.json
```

For code generation, Postman imports, and schema-validation libraries, see [Consuming OpenAPI](openapi.md).

## WebSockets

REST isn't the only surface. Two Socket.IO endpoints cover live-update and coordination use cases: [WebSockets](websockets.md).

## Versioning

RomM's API follows SemVer along with the rest of RomM:

- **Breaking changes only in major versions.** Endpoint removal, required-parameter changes, incompatible response-schema shifts
- **Minor versions add** endpoints, optional parameters, optional response fields.
- **Patch versions fix** bugs without schema changes.

## See also

- [API Authentication](api-authentication.md): auth modes in detail
- [Consuming OpenAPI](openapi.md): codegen + schema validation
- [WebSockets](websockets.md): Socket.IO endpoints
- [Client API Tokens](../ecosystem/client-api-tokens.md): recommended companion-app auth
- [Device Sync Protocol](../ecosystem/device-sync-protocol.md): sync endpoints in depth
