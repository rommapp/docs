---
title: Ports & Endpoints
description: What listens where inside a RomM container, and how external traffic reaches it.
---

# Ports & Endpoints

Quick reference for the ports + URL paths a RomM instance exposes.

## Container ports

| Port   | Protocol | Purpose                                         | Exposed?                |
| ------ | -------- | ----------------------------------------------- | ----------------------- |
| `8080` | HTTP     | nginx: the front door. Serves everything.       | Yes, publish this.      |
| `5000` | HTTP     | gunicorn: FastAPI backend. Internal only.       | No. nginx proxies here. |
| `6379` | TCP      | Valkey. Internal only (unless you externalise). | No.                     |

Only **`8080`** should be reachable from outside the container in production. Typical compose `ports:`:

```yaml
services:
    romm:
        ports:
            - 80:8080 # bind host :80 to container :8080
            # or behind a reverse proxy:
            # - 127.0.0.1:8080:8080
```

## URL paths on `:8080`

Everything below is served by nginx on port 8080. Auth / protection depends on the path.

### Unauthenticated

| Path                                                                                          | Purpose                |
| --------------------------------------------------------------------------------------------- | ---------------------- |
| `/login`, `/register`, `/reset-password`                                                      | Auth UI pages.         |
| `/api/auth/login`, `/api/auth/logout`                                                         | Session endpoints.     |
| `/api/auth/openid`, `/api/auth/oauth/openid`                                                  | OIDC callback flow.    |
| `/api/heartbeat`                                                                              | Health check.          |
| `/openapi.json`                                                                               | OpenAPI spec.          |
| `/api/docs`, `/api/redoc`                                                                     | Rendered API browsers. |
| Static assets (`/assets/...`, EmulatorJS bundle, Ruffle, covers served from `/resources/...`) | Served by nginx.       |

### Session-authenticated (cookies)

Most of the RomM web UI: every page under `/`. Authenticated via browser cookie.

### Token-authenticated (bearer)

Every API endpoint under `/api/...` that requires a specific scope. Session cookies also work here but token auth is for scripts / companion apps.

### Download endpoints (optionally auth-off)

| Path                                    | Required scope normally | With `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true` |
| --------------------------------------- | ----------------------- | ------------------------------------------ |
| `/api/roms/{id}/content/{filename}`     | `roms.read`             | None                                       |
| `/api/firmware/{id}/content/{filename}` | `firmware.read`         | None                                       |

See [Authentication → Download-endpoint auth bypass](../administration/authentication.md#download-endpoint-auth-bypass) for the security context.

### Feed endpoints

| Path                     | Client                               | Auth                                                                |
| ------------------------ | ------------------------------------ | ------------------------------------------------------------------- |
| `/api/feeds/tinfoil`     | [Tinfoil](../ecosystem/tinfoil.md)   | Respects `DISABLE_DOWNLOAD_ENDPOINT_AUTH`, and can send basic auth. |
| `/api/feeds/pkgi/...`    | [pkgj](../ecosystem/pkgj.md)         | Same.                                                               |
| `/api/feeds/fpkgi/...`   | [fpkgi](../ecosystem/fpkgi.md)       | Same.                                                               |
| `/api/feeds/kekatsu/...` | [Kekatsu](../ecosystem/kekatsu.md)   | Same.                                                               |
| `/api/feeds/webrcade`    | [WebRcade](../ecosystem/webrcade.md) | Same.                                                               |

Full catalogue in [Feeds](feeds.md).

### WebSocket endpoints

| Path                 | Purpose                              |
| -------------------- | ------------------------------------ |
| `/ws/socket.io`      | General live updates (scans, tasks). |
| `/netplay/socket.io` | Netplay session coordination.        |

Both use Socket.IO, so the reverse proxy must pass through the upgrade. See [WebSockets](../developers/websockets.md) and [Reverse Proxy](../install/reverse-proxy.md).

## Volumes (not ports but relevant)

Inside the container:

| Path              | Purpose                                                | Backup?                     |
| ----------------- | ------------------------------------------------------ | --------------------------- |
| `/romm/library`   | Your ROM + firmware source. Typically read-only mount. | No (back up separately).    |
| `/romm/assets`    | User uploads (saves, states, screenshots).             | **Critical.**               |
| `/romm/resources` | Provider-fetched cover art, screenshots.               | Low priority (rebuildable). |
| `/romm/config`    | `config.yml`.                                          | **Critical.**               |
| `/redis-data`     | Persistence for the in-container Valkey.               | Low priority.               |

See [Install & Deploy → Docker Compose](../install/docker-compose.md) for the full volume spec.

## External services RomM talks to

Outbound connections a running RomM instance may make:

| Destination                       | Purpose                    | Optional?                      |
| --------------------------------- | -------------------------- | ------------------------------ |
| `api.igdb.com`                    | IGDB metadata.             | Yes (if `IGDB_CLIENT_ID` set). |
| `www.screenscraper.fr`            | ScreenScraper metadata.    | Yes.                           |
| `www.mobygames.com`               | MobyGames metadata.        | Yes.                           |
| `retroachievements.org`           | RA metadata + progression. | Yes.                           |
| `www.steamgriddb.com`             | Cover art.                 | Yes.                           |
| `gamesdb.launchbox-app.com`       | LaunchBox DB download.     | Yes.                           |
| `hasheous.org`                    | Hash-based matching.       | Yes.                           |
| Your OIDC provider                | SSO.                       | Yes.                           |
| `sentry.io` or self-hosted Sentry | Error reporting.           | Yes.                           |
| Your OTEL collector               | Observability.             | Yes.                           |

If your firewall is egress-restrictive, allow-list these based on which features you've enabled.

## Reverse proxy path rewriting

Some users put RomM behind a path prefix (`/romm/...` instead of the bare host root). Set `ROMM_BASE_PATH` to match:

```yaml
environment:
    - ROMM_BASE_PATH=/romm
```

nginx inside the container rewrites paths internally, and your reverse proxy forwards the full path.

Not the most common pattern. Most deployments use a subdomain (`romm.example.com`) rather than a path.

## See also

- [Reverse Proxy](../install/reverse-proxy.md): passthrough recipes per proxy.
- [Environment Variables](environment-variables.md): including `ROMM_PORT`, `ROMM_BASE_PATH`, `ROMM_BASE_URL`.
- [Architecture](../developers/architecture.md): how the port layout fits into the bigger picture.
