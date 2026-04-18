---
title: Consuming OpenAPI
description: Use RomM's OpenAPI spec for code generation, Postman imports, and API exploration.
---

# Consuming OpenAPI

RomM ships its entire REST API as an OpenAPI 3.0 specification. That's the source of truth: every endpoint, every request/response schema, every parameter. Use it to generate clients, drive test suites, or import into tools.

## Where to find the spec

Every RomM instance serves:

```text
{romm_url}/openapi.json
```

No authentication required: the spec itself is public, though calling most of the endpoints it describes requires auth.

Human-readable versions:

- **Swagger UI** at `{romm_url}/api/docs`
- **ReDoc** at `{romm_url}/api/redoc`

Both are auto-generated from the same `openapi.json`. Swagger UI has a "Try it out" feature for live testing; ReDoc has a cleaner reading layout.

## Versioning

The spec is versioned alongside RomM. Every release tag includes a matching `openapi.json` in the release artifacts on GitHub. Snapshot the spec at a specific version if your client needs reproducible builds:

```sh
curl https://romm.example.com/openapi.json > openapi-5.0.0.json
```

## Rendered API reference

RomM's docs site embeds a rendered version of the spec at [API Reference](api-reference.md). It's built at docs-publish time from a pinned `openapi-v5.json` snapshot. If the live docs are behind the latest API, check the [API Reference](api-reference.md) page for the version it was built against.

## Generating client libraries

[`openapi-generator-cli`](https://openapi-generator.tech/) generates clients in 30+ languages. Example for a Python client:

```sh
npx @openapitools/openapi-generator-cli generate \
  -i https://romm.example.com/openapi.json \
  -g python \
  -o ./romm-client-python
```

For TypeScript:

```sh
npx @openapitools/openapi-generator-cli generate \
  -i https://romm.example.com/openapi.json \
  -g typescript-axios \
  -o ./romm-client-ts
```

Generated clients handle auth, request shaping, and response parsing. Drop in, import, call. Quality varies by generator target; Python and TypeScript are the best-tested.

### Tips

- **Pin the spec**, don't fetch live. Builds should be reproducible.
- **Regenerate on new RomM releases.** Breaking changes are rare but possible.
- **Patch if needed.** Generated clients sometimes need tweaks (upstream generator bugs, our spec's rough edges, etc.). Keep a patch file.

## Postman / Insomnia / Bruno

All three import OpenAPI directly:

- **Postman:** File → Import → paste `openapi.json` URL.
- **Insomnia:** Create → Import From → URL.
- **Bruno:** Import Collection → OpenAPI.

Useful for manual API exploration during development.

## Validating requests

If you're building something that calls RomM, consider validating requests against the spec before sending. Schema-driven validation catches bugs early:

- **Python:** [`openapi-core`](https://github.com/python-openapi/openapi-core).
- **Node.js:** [`openapi-backend`](https://github.com/anttiviljami/openapi-backend) or `ajv`-based approaches.
- **Go:** [`kin-openapi`](https://github.com/getkin/kin-openapi).

## Spec quirks

A few known quirks to work around:

- **Some `additionalProperties` are loose.** RomM's spec lets some responses include fields not in the schema (debug hooks, feature-flag-gated fields). Don't treat the spec as an exact response guarantee; treat it as "everything here is always present; more may follow".
- **Socket.IO isn't in the OpenAPI spec.** WebSocket endpoints are documented separately in [WebSockets](websockets.md).
- **Pagination defaults vary per endpoint.** Some paginate, some don't. Check the spec per endpoint.

## Webhooks & events

Not currently in the spec. Event-driven integration is via [WebSockets](websockets.md) only.

## See also

- [API Reference](api-reference.md): the pre-rendered version of the spec for browsing.
- [API Authentication](api-authentication.md): required auth for most endpoints.
- [OpenAPI Initiative](https://www.openapis.org/): upstream specification.
