---
title: Administration
description: Running RomM for yourself and others: users, auth, metadata, scans, tasks, backups.
---

# Administration

Administration is everything you do **as the operator** of a RomM instance: managing accounts, controlling access, configuring metadata sources, scheduling scans, watching the library for changes, monitoring the server, and keeping data safe.

The end-user equivalent (how to actually play the games, build collections, upload saves) lives in [Using RomM](../using/index.md).

## Where things live

### Users & access

- **[Users & Roles](users-and-roles.md)**: roles, the 19-scope model, how permissions add up
- **[Invitations & Registration](invitations-and-registration.md)**: invite links, public signup, first-user setup
- **[Authentication](authentication.md)**: session config, password reset, Client API Tokens for devices
- **[OIDC Setup](oidc/index.md)**: Authelia, Authentik, Keycloak, PocketID, Zitadel, SSO + role mapping

### Content & library

- **[Metadata Providers](metadata-providers.md)**: all 13 providers, credentials, priority ordering
- **[Scanning & Watcher](scanning-and-watcher.md)**: how scans work, scan modes, filesystem watcher
- **[Firmware Management](firmware-management.md)**: BIOS/firmware uploads for emulation

### Operations

- **[Scheduled Tasks](scheduled-tasks.md)**: what runs in the background and how to tune it
- **[Server Stats](server-stats.md)**: the stats page and what its numbers mean
- **[Observability](observability.md)**: logs, Sentry, OpenTelemetry, `/heartbeat`
- **[SSH Sync](ssh-sync.md)**: push/pull sync to handhelds and other devices
- **[Administration Page](administration-page.md)**: the in-app admin UI tour

### Configuration

- **[Environment Variables](../reference/environment-variables.md)**: every env var, grouped by area
- **[Configuration File](../reference/configuration-file.md)**: the `config.yml` schema

### Keeping data safe

- **[Backup & Restore](../install/backup-and-restore.md)**: routine backups, restore drill, host migration

## The role model in thirty seconds

Three built-in roles, all backed by the same scope system:

| Role       | Summary                                                                                     |
| ---------- | ------------------------------------------------------------------------------------------- |
| **Admin**  | Full control. User management, task execution, every scope. First user always gets this.    |
| **Editor** | Curate the library: edit ROMs, platforms, collections, upload firmware. No user management. |
| **Viewer** | Play games, manage own saves/states/profile. Read-only everywhere else.                     |

Full scope matrix in [Users & Roles](users-and-roles.md).

## The operator checklist

First time running RomM for someone else? Do these, in this order:

1. **Set `ROMM_AUTH_SECRET_KEY`** (via `openssl rand -hex 32`) and keep it forever. Changing it invalidates every session and invite link.
2. **Put it behind HTTPS.** See [Reverse Proxy](../install/reverse-proxy.md). Set `ROMM_BASE_URL` to the public URL.
3. **Set up at least one metadata provider** before the first scan. See [Metadata Providers](metadata-providers.md).
4. **Run the first scan** from the Scan page. See [Scanning & Watcher](scanning-and-watcher.md).
5. **Decide on invitations vs open registration.** See [Invitations & Registration](invitations-and-registration.md).
6. **Wire up OIDC** if you run an IdP. See [OIDC Setup](oidc/index.md).
7. **Configure backups.** See [Backup & Restore](../install/backup-and-restore.md). Test the restore before you need it.
8. **Pin the image tag** (`rommapp/romm:5.0.0`, not `:latest`) and read release notes before each upgrade.
