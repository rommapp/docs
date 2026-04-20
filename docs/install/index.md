---
title: Install & Deploy
description: On Docker Compose, Unraid, Synology, TrueNAS, or Kubernetes.
---

# Install & Deploy

RomM is distributed as a Docker image. Every supported deployment runs the same container, and the differences are in who manages it.

## Pick your path

| If you're on…          | Start here                                            |
| ---------------------- | ----------------------------------------------------- |
| **Linux server / NAS** | [The canonical reference setup](docker-compose.md)    |
| **Unraid**             | [Community Apps template or DCM](unraid.md)           |
| **Synology**           | [Container Manager + DSM-specific notes](synology.md) |
| **TrueNAS**            | [App Catalog or YAML install](truenas.md)             |
| **Kubernetes**         | [Manifest examples](kubernetes.md)                    |

If none of those match, start with [Docker Compose](docker-compose.md) and adapt.

## Foundational pieces

Regardless of host platform, you'll make the same handful of decisions:

- **[Image variant](image-variants.md)**: `full` (default, includes in-browser emulators) or `slim` (headless, smaller memory footprint)
- **[Database](databases.md)**: MariaDB (default), MySQL or PostgreSQL
- **[In-memory store](redis-or-valkey.md)**: required for sessions + task queue, embedded or external
- **[Reverse proxy](reverse-proxy.md)**: Caddy, nginx, Traefik, or NPM. HTTPS is required for OIDC and PWA install.
- **[Backup & restore](backup-and-restore.md)**: Test it before you need it!

## After you're up and running

- **Configure metadata providers**: [Metadata Providers](../administration/metadata-providers.md)
- **Populate the library**: [Your First Scan](../getting-started/first-scan.md)
- **Add users**: [Invitations & Registration](../administration/invitations-and-registration.md)
