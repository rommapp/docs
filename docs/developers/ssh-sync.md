---
title: SSH Sync
description: Configure SSH key-based push/pull sync
---

# SSH Sync

<!-- prettier-ignore -->
!!! warning "Coming soon"
    SSH-based push/pull sync is a work in progress. The env var surface, key layout, and device-registration flow are still being finalised. This page will be filled in once the feature stabilises.

The plan is for the Push-Pull Device Sync task to push saves/states to registered devices and pull them back after a session, over SSH, using keys that RomM holds. Until that lands, sync via HTTPS + [Client API Tokens](client-api-tokens.md), which is what Argosy, Playnite, and most companion apps already use.

For the wire-level protocol, see [Device Sync Protocol](device-sync-protocol.md).
