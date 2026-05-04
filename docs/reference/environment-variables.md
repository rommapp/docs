---
title: Environment Variables
description: Every environment variable grouped by category
---

# Environment Variables

Everything RomM does that's not in [`config.yml`](configuration-file.md) is driven by env vars. Set them on the `romm` service in your compose file, as Unraid/Synology/TrueNAS container env vars, or on your Kubernetes deployment.

This page is the **authoritative lookup**! The table is generated directly from [`rommapp/romm`'s `env.template`][src] at the SHA pinned in [`scripts/sources.toml`](https://github.com/rommapp/docs/blob/main/scripts/sources.toml). When RomM adds an env var, the next docs bump re-runs the generator and this page updates.

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

- A `.env` that's `.gitignore`d
- Docker secrets (`ROMM_AUTH_SECRET_KEY_FILE` reads from a [mounted file](https://docs.docker.com/compose/how-to/use-secrets/))
- Your orchestrator's secret store (K8s Secrets, HashiCorp Vault, AWS Secrets Manager)

## Essential variables

You'll always set these:

| Variable                                     | Purpose                                                                                         |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `ROMM_AUTH_SECRET_KEY`                       | JWT signing key generated with `openssl rand -hex 32`                                           |
| `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWD` | Database connection                                                                             |
| `ROMM_DB_DRIVER`                             | One of `mariadb` (default), `mysql`, or `postgresql` (see [Databases](../install/databases.md)) |

For metadata providers (IGDB, ScreenScraper, etc.) see [Metadata Providers](../getting-started/metadata-providers.md), and for OIDC, see [OIDC Setup](../administration/oidc/index.md).

## Full reference

--8<-- "env-vars.md"

## See also

- [Configuration File](configuration-file.md): everything that lives in `config.yml` rather than env vars
