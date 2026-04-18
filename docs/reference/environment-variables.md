---
title: Environment Variables
description: Every environment variable RomM reads, grouped by what it controls.
---

# Environment Variables

Everything RomM does that's not in [`config.yml`](configuration-file.md) is driven by env vars. Set them on the `romm` service in your compose file, as Unraid / Synology / TrueNAS container env vars, or on your Kubernetes deployment.

This page is the **authoritative lookup** — every var RomM reads. The table is generated directly from [`rommapp/romm`'s `env.template`][src] at the SHA pinned in [`docs/scripts/sources.toml`](https://github.com/rommapp/docs/blob/master/docs/scripts/sources.toml). When RomM adds an env var, the next docs bump re-runs the generator and this page updates.

[src]: https://github.com/rommapp/romm/blob/master/env.template

## Setting env vars

### Docker Compose

```yaml
services:
  romm:
    environment:
      - ROMM_AUTH_SECRET_KEY=abcd1234...
      - DB_PASSWD=secure-password
      # ...
```

Or from a `.env` file next to your compose:

```yaml
services:
  romm:
    env_file:
      - .env
```

### Secrets

Don't embed `ROMM_AUTH_SECRET_KEY`, DB passwords, or provider API keys directly in a committed compose file. Use:

- A `.env` that's `.gitignore`d.
- Docker secrets (`ROMM_AUTH_SECRET_KEY_FILE` reads from a [mounted file](https://docs.docker.com/compose/how-to/use-secrets/)).
- Your orchestrator's secret store (K8s Secrets, HashiCorp Vault, AWS Secrets Manager).

## Essential variables

You'll always set these:

| Variable | Purpose |
| --- | --- |
| `ROMM_AUTH_SECRET_KEY` | JWT signing key. Generate with `openssl rand -hex 32`. **Never rotate lightly** — breaks all sessions. |
| `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWD` | Database connection. |
| `ROMM_DB_DRIVER` | `mariadb` (default), `mysql`, `postgresql`, or `sqlite`. See [Databases](../install/databases.md). |

For metadata providers (IGDB, ScreenScraper, etc.) see [Metadata Providers](../administration/metadata-providers.md). For OIDC, see [OIDC Setup](../administration/oidc/index.md).

## When env vars are read

- **Startup.** Most vars are consumed once at container start. Change requires `docker compose up -d` to apply.
- **Per-request.** A handful of feature toggles (`KIOSK_MODE`, `DISABLE_USERPASS_LOGIN`) are re-checked per request — still, restart is safest to avoid partial-state caching.
- **Never at runtime.** There's no reload-config endpoint.

## Full reference

--8<-- "env-vars.md"

## See also

- [Configuration File](configuration-file.md) — everything that lives in `config.yml` rather than env vars.
- [Scheduled Tasks](scheduled-tasks.md) — cron-controlling env vars in context.
- [Authentication](../administration/authentication.md) — auth-related env vars in narrative form.
- [Metadata Providers](../administration/metadata-providers.md) — per-provider credential env vars.
