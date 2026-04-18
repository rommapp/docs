---
title: Authentication
description: Configure how users sign in — sessions, password policy, client tokens, OIDC hooks, and kiosk mode.
---

# Authentication

This page is the **operator-side** authentication reference: knobs you turn on the server to control how people sign in. The **client-side** reference — "how do I actually authenticate an API call?" — is in [API Authentication](../developers/api-authentication.md).

Authentication flows RomM supports:

- **Username + password** (default) — local account, bcrypt-hashed, stored in the DB.
- **OIDC** — single sign-on via an external IdP. See [OIDC Setup](oidc/index.md).
- **Client API Tokens** — long-lived per-user tokens for companion apps and scripts.
- **Device pairing** — short codes for bootstrapping a token onto a handheld. Covered in [Client API Tokens](../ecosystem/client-api-tokens.md).
- **Kiosk mode** — unauthenticated read-only access. Toggle for public demos / shared terminals.

## Session config

Sessions are cookie-based and stored in Redis. Relevant env vars:

| Variable | Default | What it controls |
| --- | --- | --- |
| `ROMM_AUTH_SECRET_KEY` | _(required)_ | HS256 signing key for session tokens and JWTs. Generate with `openssl rand -hex 32`. **Never rotate this casually** — it invalidates every active session and every outstanding invite link. |
| `ROMM_AUTH_SECRET_KEY_FILE` | — | Alternative: read the secret from a file. Useful with Docker secrets. |
| `SESSION_MAX_AGE_SECONDS` | 86400 (24 h) | How long a session cookie lives before the user has to sign in again. |
| `OAUTH_ACCESS_TOKEN_EXPIRE_SECONDS` | 900 (15 min) | Short-lived OAuth2 access token TTL. |
| `OAUTH_REFRESH_TOKEN_EXPIRE_SECONDS` | 2592000 (30 d) | Refresh token TTL for OAuth2. |
| `DISABLE_CSRF_PROTECTION` | `false` | Disable CSRF middleware. Only do this behind a trusted reverse proxy that strips unwanted cross-origin traffic. |

## Local (username + password)

The default. Accounts are created via [invitations, registration, or the Setup Wizard](invitations-and-registration.md). Passwords are bcrypt-hashed — RomM does not log or store plaintext passwords at any point.

**Disable local password login entirely** (force OIDC-only):

```yaml
environment:
  - DISABLE_USERPASS_LOGIN=true
```

!!! warning "Keep a way in"
    Before setting `DISABLE_USERPASS_LOGIN=true`, confirm that at least one Admin account can sign in via OIDC and reach the Administration page. If OIDC breaks and you've already disabled local login, your only way in is editing the container env.

### Admin-triggered password reset

Until email-based self-serve reset lands, admins set passwords manually:

**Administration → Users → Edit → New password → Save.**

The next login on that account will use the new password; existing sessions for that user remain valid until they expire — revoke them explicitly by deleting all of the user's Client API Tokens if that's a concern.

### Self-serve password reset

Users can click "Forgot password?" on the login page if you've configured an SMTP transport. (Not part of 5.0 GA — the UI path exists and will light up once email config is exposed.)

## OIDC

See [OIDC Setup](oidc/index.md) for the full walkthrough. One-liner config sketch:

```yaml
environment:
  - OIDC_ENABLED=true
  - OIDC_PROVIDER=keycloak
  - OIDC_CLIENT_ID=...
  - OIDC_CLIENT_SECRET=...
  - OIDC_SERVER_APPLICATION_URL=https://auth.example.com
  - OIDC_REDIRECT_URI=https://romm.example.com/api/oauth/openid
```

When OIDC is configured, the login page grows an "OIDC" button. Set `OIDC_AUTOLOGIN=true` to redirect straight to the IdP without the user having to click it.

## Client API Tokens

For anything long-lived — a companion app, a cron job, a script — use **Client API Tokens** instead of storing a password.

Create from **Administration → Client API Tokens**. Each token:

- Belongs to a specific user.
- Carries a **subset** of that user's scopes (you choose which at creation time).
- Has an optional expiry (no expiry = never expires until manually revoked).
- Can be "paired" to a device via a short code (covered in [Client API Tokens](../ecosystem/client-api-tokens.md)).

Each user gets up to 25 active tokens. Revoke from the same page. The API side — "how do I send this thing in a request?" — lives in [API Authentication](../developers/api-authentication.md).

## Kiosk mode

Turns every GET endpoint into unauthenticated read-only access — anyone reaching the instance can browse, but nobody can write, scan, upload, or manage users.

```yaml
environment:
  - KIOSK_MODE=true
```

Appropriate for:

- Shared-terminal demos.
- Public-facing "display" instances (e.g. a wall-mounted browse-only catalogue).
- `demo.romm.app`.

Authenticated users (when you do sign in) still see their full role; kiosk only affects anonymous traffic.

## Download-endpoint auth bypass

```yaml
environment:
  - DISABLE_DOWNLOAD_ENDPOINT_AUTH=true
```

Skips auth on `GET /api/roms/{id}/content/…` and the firmware download endpoint. Exists so third-party apps that can't carry a bearer header (dumb emulators loading a ROM by URL) can still pull files.

**Only enable this when the public internet can't reach RomM directly** — i.e. there's auth or an IP allowlist at the reverse-proxy layer. Otherwise you've just made your library world-downloadable.

## Revoking access

To fully cut a user off:

1. **Administration → Users → Edit** → set password to something random and toggle to Viewer (so even if they're mid-session they can't do damage).
2. Delete all their Client API Tokens (**Administration → Client API Tokens**, filter by user).
3. Delete the user.

Steps 1 + 2 together ensure any in-flight session and any token-based companion app lose access immediately. Step 3 removes the account.
