---
title: Authentication
description: Configure how users sign in.
---

# Authentication

This page is the **operator-side** authentication reference, the knobs you turn on the server to control how people sign in. The **client-side** reference ("how do I actually authenticate an API call?") is in [API Authentication](../developers/api-authentication.md).

Authentication flows RomM supports:

- **Username + password** (default): local account, bcrypt-hashed, stored in the DB
- **OIDC**: single sign-on via an external IdP
- **Client API Tokens**: long-lived per-user tokens for companion apps and scripts
- **Device pairing**: short codes for bootstrapping a token onto a handheld
- **Kiosk mode**: unauthenticated read-only access, handy for public demos

## Session config

Sessions are cookie-based and stored in Redis. Relevant env vars:

| Variable                             | Default        | What it controls                                                                                                                                                                                    |
| ------------------------------------ | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ROMM_AUTH_SECRET_KEY`               | _(required)_   | HS256 signing key for session tokens and JWTs. Generate with `openssl rand -hex 32`. **Never rotate this casually**, because it invalidates every active session and every outstanding invite link. |
| `ROMM_AUTH_SECRET_KEY_FILE`          |                | Read the secret from a file (e.g. via Docker secrets) instead of an env var.                                                                                                                        |
| `SESSION_MAX_AGE_SECONDS`            | 86400 (24 h)   | How long a session cookie lives before the user has to sign in again.                                                                                                                               |
| `OAUTH_ACCESS_TOKEN_EXPIRE_SECONDS`  | 900 (15 min)   | Short-lived OAuth2 access token TTL.                                                                                                                                                                |
| `OAUTH_REFRESH_TOKEN_EXPIRE_SECONDS` | 2592000 (30 d) | Refresh token TTL for OAuth2.                                                                                                                                                                       |
| `DISABLE_CSRF_PROTECTION`            | `false`        | Disable CSRF middleware. Only do this behind a trusted reverse proxy that strips unwanted cross-origin traffic.                                                                                     |

## Local (username + password)

Local accounts are created via [invitations, registration, admin setup, or the Setup Wizard](invitations-and-registration.md), and passwords are bcrypt-hashed.

**Disable local password login entirely** (force OIDC-only):

```yaml
environment:
    - DISABLE_USERPASS_LOGIN=true
```

<!-- prettier-ignore -->
!!! warning "Keep a way in"
    Before setting `DISABLE_USERPASS_LOGIN=true`, confirm that at least one Admin account can sign in via OIDC and reach the Administration page. If OIDC breaks and you've already disabled local login, your only way in is editing the container env.

### Admin-triggered password reset

Until email-based self-serve reset lands, admins set passwords manually:

**Administration → Users → Edit → New password → Save.**

The next login on that account will use the new password but existing sessions for that user remain valid until they expire.

## OIDC

See [OIDC Setup](oidc/index.md) for the full walkthrough. One-liner config sketch:

```yaml
environment:
    - OIDC_ENABLED=true
    - OIDC_PROVIDER=keycloak
    - OIDC_CLIENT_ID=...
    - OIDC_CLIENT_SECRET=...
    - OIDC_SERVER_APPLICATION_URL=https://auth.example.com
    - OIDC_REDIRECT_URI=https://demo.romm.app/api/oauth/openid
```

When OIDC is configured, the login page shows an "OIDC" button. Set `OIDC_AUTOLOGIN=true` to redirect straight to the IdP without the user having to click it.

## Client API Tokens

For anything long-lived (a companion app, a cron job, a script) use **Client API Tokens** instead of storing a password.

Create from **Administration → Client API Tokens**. Each token:

- Belongs to a specific user
- Carries a **subset** of that user's scopes (you choose which at creation time)
- Has an optional expiry (no expiry = never expires until manually revoked)
- Can be "paired" to a device via a short code

Each user gets up to 25 active tokens, revokable from the same page. The API side ("how do I send this thing in a request?") lives in [API Authentication](../developers/api-authentication.md).

## Kiosk mode

Grants unauthenticated, read-only access to nearly every GET endpoint. Anyone reaching the instance can browse but only a logged-in admin can write, scan, upload, or manage users.

```yaml
environment:
    - KIOSK_MODE=true
```

Appropriate for:

- Shared-terminal demos
- Public-facing "display" instances
- `demo.romm.app`

Authenticated users (when you do sign in) will still see the full UI with all actions available to their role.

## Download-endpoint auth bypass

```yaml
environment:
    - DISABLE_DOWNLOAD_ENDPOINT_AUTH=true
```

Skips auth on `GET /api/roms/{id}/content/…` and the firmware download endpoint. Exists so third-party apps that can't carry a bearer header (like dumb emulators loading a ROM by URL) can still pull files. **Only enable this when the public internet can't reach RomM directly**, i.e. there's auth or an IP allowlist at the reverse-proxy layer. Otherwise you've just made your library world-downloadable.

## Revoking access

To fully cut a user off:

1. **Administration → Client API Tokens** → Delete active tokens for that user.
2. **Administration → Users** → Disable the user.
3. **Administration → Users → Edit** → Delete the user.
