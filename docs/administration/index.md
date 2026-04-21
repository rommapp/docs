---
title: Administration
description: Running RomM for yourself and others.
---

# Administration

Administration is everything you do **as the operator** of a RomM instance: managing accounts, controlling access, configuring metadata sources, scheduling scans, watching the library for changes, monitoring the server, and keeping data safe.

The end-user equivalent (how to actually play the games, build collections, upload saves) lives in [Using RomM](../using/index.md).

## Where things live

### Users & access

- **[Users & Roles](users-and-roles.md)**: roles, the scope model, how permissions add up
- **[Invitations & Registration](invitations-and-registration.md)**: invite links, public signup, first-user setup
- **[Authentication](authentication.md)**: session config, password reset, Client API Tokens for devices
- **[OIDC Setup](oidc/index.md)**: Authelia, Authentik, Keycloak, PocketID, Zitadel, SSO + role mapping

### Content & library

- **[Metadata Providers](metadata-providers.md)**: all providers, credentials, priority ordering
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
