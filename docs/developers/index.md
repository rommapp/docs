---
title: API & Development
description: Build on top of RomM: API reference, WebSockets, OpenAPI, local dev, contributing.
---

# API & Development

For anyone **building something on top of or inside of RomM**: third-party apps, scripts, contributions to the core, translations.

Looking for end-user or operator content? See [Using RomM](../using/index.md) or [Administration](../administration/index.md).

## Working with the API

- **[API Reference](api-reference.md):** every API endpoint. OpenAPI-driven
- **[API Authentication](api-authentication.md):** all five auth modes (session, Basic, OAuth2, Client API Token, OIDC)
- **[Consuming OpenAPI](openapi.md):** codegen, Postman imports, schema validation
- **[WebSockets](websockets.md):** Socket.IO endpoints for live updates and Netplay

## Building companion apps

- **[Client API Tokens](../ecosystem/client-api-tokens.md):** how companion apps authenticate, including the device-pairing flow
- **[Device Sync Protocol](../ecosystem/device-sync-protocol.md):** wire-level reference for save/state/play-session sync
- **[Argosy](../ecosystem/argosy.md), [Grout](../ecosystem/grout.md):** reference implementations

## Contributing to RomM itself

- **[Development Setup](development-setup.md):** get a local environment running
- **[Architecture](architecture.md):** high-level walkthrough of the codebase
- **[Contributing](contributing.md):** process, style, AI-assistance disclosure
- **[Translations (i18n)](i18n.md):** add or improve a locale
- **[Releasing](releasing.md):** maintainer-only, how releases are cut

## Reference

- **[Environment Variables](../reference/environment-variables.md):** every env var
- **[Configuration File](../reference/configuration-file.md):** `config.yml` schema
- **[Exports](../reference/exports.md):** gamelist.xml / Pegasus export formats
- **[Feeds](../reference/feeds.md):** every URL-feed endpoint (Tinfoil, pkgj, WebRcade, etc.)
- **[Glossary](../reference/glossary.md):** canonical terminology

## Quick orientation

| I want to…                       | Start here                                                                      |
| -------------------------------- | ------------------------------------------------------------------------------- |
| Call the API from a script  | [API Authentication](api-authentication.md) + [API Reference](api-reference.md) |
| Generate a client library        | [Consuming OpenAPI](openapi.md)                                                 |
| Sync saves from a handheld       | [Device Sync Protocol](../ecosystem/device-sync-protocol.md)                    |
| Listen to scan events            | [WebSockets](websockets.md)                                                     |
| Fix a bug in RomM                | [Development Setup](development-setup.md) + [Contributing](contributing.md)     |
| Translate the app                | [Translations (i18n)](i18n.md)                                                  |
| Understand how it's put together | [Architecture](architecture.md)                                                 |
