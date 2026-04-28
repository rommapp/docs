---
title: API & Development
description: Build on top of RomM or contribute to it
---

# API & Development

Everything you need to **build on top of RomM** (third-party apps, scripts, integrations) or **contribute to it** (code, translations, docs). End-user content lives in [Using RomM](../using/index.md). Operator content lives in [Administration](../administration/index.md).

## Calling the API

- **[API Reference](api-reference.md)**: every endpoint, OpenAPI-driven
- **[API Authentication](api-authentication.md)**: all five auth modes (session, Basic, OAuth2, Client API Token, OIDC)
- **[Consuming OpenAPI](openapi.md)**: codegen, Postman imports, schema validation
- **[WebSockets](websockets.md)**: socket.io endpoints for live updates and Netplay

## Building companion apps

- **[Client API Tokens](../ecosystem/client-api-tokens.md)**: how companion apps authenticate, including the device-pairing flow
- **[Device Sync Protocol](device-sync-protocol.md)**: wire-level reference for save/state/play-session sync
- **[Argosy](../ecosystem/first-party-apps.md#argosy-launcher), [Grout](../ecosystem/first-party-apps.md#grout)**: reference implementations to crib from

## Contributing to RomM itself

- **[Development Setup](development-setup.md)**: get a local env running
- **[Architecture](architecture.md)**: high-level codebase walkthrough
- **[Contributing](contributing.md)**: process, style, AI-assistance disclosure
- **[Translations (i18n)](i18n.md)**: add or improve a locale

## Reference

- **[Environment Variables](../reference/environment-variables.md)**: every env var, grouped by area
- **[Configuration File](../reference/configuration-file.md)**: `config.yml` schema
- **[Exports](../reference/exports.md)**: gamelist.xml / Pegasus export formats
- **[Feeds](../reference/feeds.md)**: every URL-feed endpoint (Tinfoil, pkgj, WebRcade, etc.)
- **[Glossary](../reference/glossary.md)**: canonical terminology
