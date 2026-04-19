---
title: Release Notes & Migration
description: RomM release cadence, versioning policy, docs versions, and per-major migration guides.
---

# Release Notes & Migration

## Current version

RomM's current stable is [`5.0.0`](changelog.md). Read [Upgrading to 5.0](upgrading-to-5.0.md) if you're coming from 4.x.

## Versioning

RomM follows **SemVer** for breaking changes and **CalVer-ish** for cadence: major versions are planned milestones, not scheduled.

- **Patch releases** (`5.0.1`, `5.0.2`): bug fixes only. Safe to pull automatically. No migration.
- **Minor releases** (`5.1.0`, `5.2.0`): additive features. Schema may migrate automatically via Alembic, but no action required beyond reading the release notes.
- **Major releases** (`5.0.0`, `6.0.0`): breaking changes. Read the migration guide before upgrading.

## Image tags and what to pin

| Tag | What it moves to | When to use |
| --- | --- | --- |
| `rommapp/romm:latest` | Every new stable release | Dev / "I'll deal with it" setups. **Never pin production to `:latest`** because you'll ship untested upgrades. |
| `rommapp/romm:5.0.0` | Immutable, specific release | Production. Update deliberately by bumping the tag. |
| `rommapp/romm:5` | Latest in the 5.x line | Middle ground: auto-minor-upgrades within a major. |
| `rommapp/romm:develop` | Every push to `master` | Don't. |
| `rommapp/romm:5.0.0-slim` | Same as `5.0.0` but without EmulatorJS/Ruffle | Headless / API-only deployments. See [Image Variants](../install/image-variants.md). |

Registries: Docker Hub (`rommapp/romm`) and GitHub Container Registry (`ghcr.io/rommapp/romm`), same tags, same content.

## Docs versions

The docs site is versioned via [mike](https://github.com/jimporter/mike). Every major RomM release gets its own docs tree, accessible from the version switcher top-left:

- `docs.romm.app/latest/` → 5.x (this is what you're reading).
- `docs.romm.app/4.8/` → frozen 4.x docs.
- Older majors may remain accessible for a while. See the support window below.

## Support window

We support the current major and the previous major for critical bug fixes and security patches.

| Major | Status | Frozen docs |
| --- | --- | --- |
| **5.x** | **Current**, active development | `docs.romm.app/latest/` |
| **4.x** | Security + critical bugs only | `docs.romm.app/4.8/` |
| **3.x** | Unsupported, upgrade | N/A |
| **≤2.x** | Unsupported | N/A |

Older frozen docs are retained for 12 months after the major's support window ends, then removed. Plan upgrades accordingly.

## Migration guides

- **[Upgrading to 5.0](upgrading-to-5.0.md):** 4.x → 5.0. Required reading.
- **[Upgrading to 3.0](upgrading-to-3.0.md):** 2.x → 3.0. SQLite drop, auth requirement, Redis built-in, config folder mount. Historical, but kept for 2.x migrators.

## Where releases are announced

- [GitHub Releases](https://github.com/rommapp/romm/releases): authoritative changelog, tag-by-tag.
- [Discord](https://discord.gg/romm) `#announcements`: release pings.
- [Changelog](changelog.md): human-readable per-release summary.

## Upgrade protocol

Before pulling a new major:

1. Read the relevant migration guide.
2. Back up: `mysqldump` / `pg_dump` + `/romm/assets` + `/romm/config`. See [Backup & Restore](../install/backup-and-restore.md).
3. Pull the new image to your host but don't `up -d` yet.
4. In a quiet window, `docker compose down && docker compose up -d`.
5. Watch `docker logs -f romm` for any Alembic migration or startup errors.
6. Verify Server Stats, run a Quick scan, log in as a Viewer, confirm nothing is visibly broken.

If something breaks, revert the image tag and restore the backup. See the per-guide rollback sections.
