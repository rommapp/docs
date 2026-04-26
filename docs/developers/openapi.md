---
title: Consuming OpenAPI
description: Use RomM's OpenAPI spec for code generation, Postman imports, and validation
---

# Consuming OpenAPI

RomM ships its entire API as an OpenAPI 3.0 spec. That's the source of truth: every endpoint, every request and response schema, every parameter. Use it to generate clients, drive test suites, or import into tools.

## Where the spec lives

Every RomM instance serves it:

```text
{romm_url}/openapi.json
```

No authentication required. The spec itself is public, though calling most of the endpoints it describes requires auth (see [API Authentication](api-authentication.md)).

Human-readable renderings:

- **Swagger UI** at `{romm_url}/api/docs` with a "Try it out" button for live testing
- **ReDoc** at `{romm_url}/api/redoc` with a cleaner reading layout

Both are auto-generated from the same `openapi.json`.

## Versioning

The spec is versioned alongside RomM itself. Every release tag includes a matching `openapi.json` in the GitHub release artifacts. Snapshot the spec at a specific version when your client needs reproducible builds:

```sh
curl https://demo.romm.app/openapi.json > openapi-5.0.0.json
```

The docs site embeds a rendered version of the spec at [API Reference](api-reference.md), built at docs-publish time from a pinned snapshot. If the rendered docs lag behind the live API, fetch the live spec from your instance directly.

## Generating client libraries

[`openapi-generator-cli`](https://openapi-generator.tech/) generates clients in 30+ languages.

Python:

```sh
npx @openapitools/openapi-generator-cli generate \
  -i https://demo.romm.app/openapi.json \
  -g python \
  -o ./romm-client-python
```

TypeScript:

```sh
npx @openapitools/openapi-generator-cli generate \
  -i https://demo.romm.app/openapi.json \
  -g typescript-axios \
  -o ./romm-client-ts
```

Generated clients handle auth, request shaping, and response parsing for you. Quality varies by generator target, but Python and TypeScript are the best-tested in practice since that's what RomM itself uses internally.

Three rules for staying sane:

- **Pin the spec, don't fetch live.** Builds should be reproducible.
- **Regenerate on every RomM release** that bumps the major or minor version. Patch releases are spec-stable.
- **Keep a patch file** if your generator output needs tweaks. Generators have rough edges, and so does the spec.

## Postman, Insomnia, Bruno

All three import OpenAPI directly:

- **Postman**: File → Import → paste the `openapi.json` URL
- **Insomnia**: Create → Import From → URL
- **Bruno**: Import Collection → OpenAPI

Useful for manual API exploration during development.

## Validating requests against the spec

If you're building something that calls RomM, schema-driven validation catches bugs before they hit the wire:

- **Python**: [`openapi-core`](https://github.com/python-openapi/openapi-core)
- **Node.js**: [`openapi-backend`](https://github.com/anttiviljami/openapi-backend) or any `ajv`-based approach
- **Go**: [`kin-openapi`](https://github.com/getkin/kin-openapi)

## Spec quirks

A few known rough edges to be aware of:

- **Some `additionalProperties` are loose.** Certain responses include fields that aren't declared in the schema (debug hooks, feature-flag-gated fields), so treat the spec as "everything here is always present, more may follow" rather than an exact response guarantee.
- **Socket.IO isn't in the spec.** WebSocket endpoints are documented separately in [WebSockets](websockets.md).
- **Pagination defaults vary per endpoint.** Some endpoints paginate by default and some don't, so check the spec for each one before assuming.

## Webhooks & events

Not currently in the spec. Event-driven integration is via Socket.IO only. See [WebSockets](websockets.md).
