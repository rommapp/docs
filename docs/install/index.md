---
title: Install & Deploy
description: Pick a deployment path: Docker Compose, Unraid, Synology, TrueNAS, or Kubernetes.
---

# Install & Deploy

RomM is distributed as a Docker image. Every supported deployment runs the same container; the differences are in who manages it.

## Pick your path

| If you're on… | Start here |
| --- | --- |
| A Linux server / NAS with Docker | **[Docker Compose](docker-compose.md)**: the canonical reference setup. |
| **Unraid** | [Unraid](unraid.md): two supported paths (Community Apps template, Docker Compose Manager). |
| **Synology** | [Synology](synology.md): Container Manager + DSM-specific notes. |
| **TrueNAS SCALE** | [TrueNAS](truenas.md): App Catalog or YAML install. |
| **Kubernetes** | [Kubernetes](kubernetes.md): manifest examples, required quirks. |

If none of those match, start with [Docker Compose](docker-compose.md) and adapt.

## Foundational pieces

Regardless of host platform, you'll make the same handful of decisions:

- **[Image variant](image-variants.md)**: `full` (default, includes in-browser emulators) or `slim` (headless, smaller footprint).
- **[Database](databases.md)**: MariaDB (default), MySQL, PostgreSQL, or SQLite (dev-only).
- **[Redis / Valkey](redis-or-valkey.md)**: required for sessions + task queue. Embedded or external.
- **[Reverse proxy](reverse-proxy.md)**: Caddy, nginx, Traefik, or NPM. HTTPS required for OIDC and PWA install.
- **[Backup & restore](backup-and-restore.md)**: don't skip. Test the restore before you need it.

## Minimum reading before going live

1. [Quick Start](../getting-started/quick-start.md): 15-minute happy-path walkthrough.
2. [Docker Compose](docker-compose.md): production-oriented reference compose.
3. [Reverse Proxy](reverse-proxy.md): pick a TLS-terminating proxy.
4. [Backup & Restore](backup-and-restore.md): nightly backup + restore drill.

Then come back here when you're ready to pick a platform-specific guide, or read [Administration](../administration/index.md) to set up your first users, metadata, and scheduled tasks.

## After you're up and running

- **Populate the library**: [Your First Scan](../getting-started/first-scan.md).
- **Add users**: [Invitations & Registration](../administration/invitations-and-registration.md).
- **Configure metadata providers**: [Metadata Providers](../administration/metadata-providers.md).
- **Upgrading from 4.x?** [Upgrading to 5.0](../releases/upgrading-to-5.0.md).
