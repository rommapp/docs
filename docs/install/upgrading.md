---
title: Upgrading
description: Move to a new RomM release safely, and what changes in each one
---

# Upgrading

RomM upgrades in place. Pull the new image, recreate the container, and the database migrations run on the first start:

```sh
docker compose pull
docker compose up -d
```

Before a minor or major upgrade:

- Take a backup of the database and `/romm/assets` (see [Backup & Restore](backup-and-restore.md)). Migrations only run forward, so a backup is the only way back to the old version.
- Read the [release notes](https://github.com/rommapp/romm/releases) for anything marked as a breaking change, and the section for your target version below.
- Pin a version tag such as `rommapp/romm:5.4.0` instead of `latest`, so a container recreated later doesn't upgrade without you noticing.

## 5.3 to 5.4

### Let the first start finish its migrations

Several migrations rewrite the `roms` table and backfill it in batches, which can take a while on a large library. RomM doesn't start serving the web UI until they finish, and the container log lists each migration as it runs, then `Database migrations succeeded` once they're done.

<!-- prettier-ignore -->
!!! warning "Don't restart the container while migrations run"
    Stopping mid-migration can leave the database half upgraded. If an orchestrator restarts containers that fail a health check, such as Kubernetes or a NAS app manager, give the first start a longer grace period or turn the check off until that line appears.

### Cross-origin requests are denied by default

An unset or empty `ROMM_CORS_ALLOWED_ORIGINS` used to allow every origin, and now allows none. The web UI and the API share an origin, so most installs need no change, and you only need to act if a browser-based app on another origin calls your RomM, such as a custom dashboard on a different domain. Native companion apps like Argosy, Grout and Playnite don't use CORS and are unaffected.

List each origin that should be allowed, comma-separated, with no trailing slash:

```yaml
environment:
    - ROMM_CORS_ALLOWED_ORIGINS=https://dashboard.example.com,http://localhost:5173
```

A `*` still answers any origin, but without credentials, so a browser client that signs in with the session cookie needs its origin listed explicitly (see [Reverse Proxy → Cookies and CORS](reverse-proxy.md#harden-cookies-and-cors-behind-https)).

### Add a reverse proxy on a public address to `FORWARDED_ALLOW_IPS`

RomM now trusts `X-Forwarded-For` only from loopback and private ranges. The new default is:

```text
127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,100.64.0.0/10,fc00::/7
```

A reverse proxy on the same host, on a Docker network or on your LAN already falls inside those ranges and needs no change. A proxy that reaches RomM from a public address, such as a VPS that forwards to your home server, has to be added, or every request is logged, audited and rate limited as coming from the proxy's address. Append it to the default rather than replacing the list:

```yaml
environment:
    - FORWARDED_ALLOW_IPS=127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,100.64.0.0/10,fc00::/7,203.0.113.10
```

Earlier releases trusted every hop, which let any client choose the address RomM recorded for it. Setting `FORWARDED_ALLOW_IPS=*` brings that behavior back, so avoid it (see [Reverse Proxy → `FORWARDED_ALLOW_IPS`](reverse-proxy.md#set-forwarded_allow_ips-for-your-proxy)).

### Seeded permission groups are renamed

The "Viewer (legacy)" and "Editor (legacy)" groups become "Viewer" and "Editor". The upgrade leaves a group alone if you'd already renamed it, or if another group already holds the new name (see [Users & Roles → Seeded groups](../administration/users-and-roles.md#seeded-groups)).

### New settings worth reviewing

Several new features are configured through environment variables with working defaults, and these are the ones you may want to set right away:

- `SMTP_*` to send notification and password reset emails (see [Email](../administration/email.md))
- `AUDIT_LOG_RETENTION_DAYS` to keep audit events for longer or shorter than 90 days (see [Audit Log](../administration/audit-log.md))
- `ROM_CONVERTO_ENABLED` to turn on library conversion and converted downloads (see [Library Conversion](../administration/library-conversion.md))
- `DEVICE_INSTALL_ENABLED` and `DEVICE_INSTALL_EXCLUDED_PLATFORM_SLUGS` to control pushing games to devices
- `DISABLE_EASYRPG` to turn off the RPG Maker 2000/2003 player

The [Environment Variables](../reference/environment-variables.md) reference lists every one of them.

### API changes for client authors

Most changes are additions. These can break an existing client:

| Change                                      | What to do                                                                                                                                                                                                                                                                   |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PermissionGroupSchema.is_system` removed   | Read `system_key` instead, which is `viewer`, `editor` or `null` for a group an admin created.                                                                                                                                                                               |
| `PlaySessionSchema.sync_session_id` removed | Stop reading it, since play sessions are no longer linked to sync sessions.                                                                                                                                                                                                  |
| `GET /api/play-sessions`                    | Without the `devices.read` scope, `device_id` is required and must equal the calling token's own device. The endpoint no longer fills `device_id` in from the token.                                                                                                         |
| `GET /api/netplay/list`                     | Requires `roms.read` instead of `assets.read`. `game_id` is now an integer ROM id, and a missing or hidden ROM returns `404`.                                                                                                                                                |
| Netplay socket rooms                        | `open-room`, and `join-room` on a room without a password, need a signed-in user with `roms.read` who can see the ROM. The room password moved from `extra.room_password` to a top-level `password` field (see [WebSockets → Netplay](../developers/websockets.md#netplay)). |
| `scan` socket event                         | The payload is validated strictly and unknown keys are rejected. Invalid options, no running scan worker, or a library scan already in flight now emit `scan:done_ko` (see [WebSockets → Scans](../developers/websockets.md#scans)).                                         |
| `activity:update` socket event              | Sent only to users who can see the ROM, instead of to every client. Refetch the activity list on the new `activity:refresh` event.                                                                                                                                           |
| Collection names                            | Creating or renaming a collection onto a name that already exists returns `409` (was `500`). A name over 400 characters returns `422`.                                                                                                                                       |
| `PUT /api/roms/{id}` rename                 | Renaming onto an existing file returns `409` (was `500`). An invalid or overlong `fs_name` returns `400` before any metadata fetch.                                                                                                                                          |
| CORS                                        | See [above](#cross-origin-requests-are-denied-by-default). A browser client on another origin must be allowlisted.                                                                                                                                                           |
| Sync `delete` operation                     | `SyncOperationSchema.action` can now be `delete`, meaning the slot was emptied on the server. Handle it, or at least ignore it, rather than failing on an unknown action (see [Device Sync Protocol](../developers/device-sync-protocol.md)).                                |

A malformed Basic header or an invalid or expired JWT bearer now leaves the request unauthenticated, so it gets the route's `401` or `403` instead of a `500` (see [API Authentication → Errors](../developers/api-authentication.md#errors)).
