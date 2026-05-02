---
title: Consuming OpenAPI
description: Use the OpenAPI spec for code generation
---

# Consuming OpenAPI

RomM ships its entire API as an OpenAPI 3.0 spec, which includes every endpoint, every request and response schema, and every parameter.

## Where the spec lives

Every instance serves it at `{romm_url}/openapi.json`. It's public and doesn't require auth, so you can fetch it from any running instance, including `https://demo.romm.app/openapi.json`.

For human-readable renderings, see [API Reference](api-reference.md).

## Versioning

The spec is versioned alongside the app, so you can snapshot the spec at a specific version when your client needs reproducible builds:

```sh
curl https://demo.romm.app/openapi.json > openapi-5.0.0.json
```

The docs site embeds a rendered version of the spec at [API Reference](api-reference.md), built at docs-publish time from a pinned snapshot. If the rendered docs lag behind the live API, fetch the live spec from your instance directly.

## Importing into tools

- **Postman**: File → Import → paste the `openapi.json` URL
- **Insomnia**: Create → Import From → URL
- **Bruno**: Import Collection → OpenAPI

## Spec quirks

A few known rough edges to be aware of:

- **Some `additionalProperties` are loose.** Certain responses include fields that aren't declared in the schema, so treat the spec as "everything here is always present, more may follow" rather than an exact response guarantee.
- **socket.io isn't in the spec.** WebSocket endpoints are documented separately in [WebSockets](websockets.md).
- **Pagination defaults vary per endpoint.** Some endpoints paginate by default and some don't, so check the spec for each one before assuming.
