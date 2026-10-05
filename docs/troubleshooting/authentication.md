---
title: Authentication Troubleshooting
description: Fix login, session, CSRF, and OIDC issues
---

# Authentication Troubleshooting

## `401 Unauthorized` or `403 Forbidden` on API calls

The two codes mean different things:

- **`401 Unauthorized`**: the request carries no credential RomM can use. You're signed out, your session expired or was revoked, or the `Authorization` header is malformed, has the wrong password, or holds an expired token. Sign in again, or refresh or replace the token.
- **`403 Forbidden`**: you're signed in, but your account or token lacks the scope the endpoint needs. Check the user's permission group and the token's scopes (see [API Authentication → Errors](../developers/api-authentication.md#errors)).

If a browser session seems broken in a way signing in again doesn't fix (for example a session signed with an old `ROMM_AUTH_SECRET_KEY`), [clear cookies](https://support.google.com/accounts/answer/32050) for the host and sign in again.

## Browser app on another origin is blocked by CORS

The browser console shows `blocked by CORS policy` or `No 'Access-Control-Allow-Origin' header` when a web app served from another domain or port calls RomM. Since 5.4, an empty `ROMM_CORS_ALLOWED_ORIGINS` denies every cross-origin request, so list the app's origin:

```yaml
environment:
    - ROMM_CORS_ALLOWED_ORIGINS=https://dashboard.example.com
```

Write it as scheme, host and port, exactly as the browser shows it in the `Origin` request header, with no trailing slash. A `*` entry won't fix an app that signs in with the session cookie, because RomM never allows credentials for a wildcard (see [Reverse Proxy → Cookies and CORS](../install/reverse-proxy.md#harden-cookies-and-cors-behind-https)).

## `Forbidden (403) CSRF verification failed`

CSRF protection is on by default, so a mismatched or missing `csrftoken` cookie causes this.

1. Reload the page, and a fresh CSRF cookie is set on GET requests, which should fix it on the next POST.
2. Still broken? Clear cookies for the host and hard-reload (`CMD+SHIFT+R`/`CTRL+F5`).
3. As a last resort, disable CSRF verification with `DISABLE_CSRF_PROTECTION=true` in your env, but **we strongly discourage this** as it opens you up to CSRF attacks.

If you're behind a reverse proxy and CSRF keeps failing, the proxy is probably stripping the `csrftoken` cookie or the `X-CSRFToken` header (see the [Reverse Proxy recipes](../install/reverse-proxy.md)). Every one of them forwards `Cookie` and all custom headers by default, so if yours doesn't, fix the proxy config.

## `400 Bad Request` on the WebSocket endpoint

Your reverse proxy is stripping the WebSocket upgrade, and live updates (scan progress, Netplay) use socket.io. Fixes for each proxy:

- **Nginx/NPM**: enable WebSockets Support (the [Reverse Proxy](../install/reverse-proxy.md) snippets already do this).
- **Traefik**: add `proxy_set_header Upgrade $http_upgrade` (or use the Traefik middleware equivalent).
- **Caddy**: WebSockets work out of the box with `reverse_proxy`.
- **Cloudflare**: enable **WebSockets** under Network settings.

The main UI falls back to HTTP long polling when the upgrade fails, so it mostly keeps working, but [Netplay](../using/netplay.md) connects over WebSockets only and fails outright.

## `Error: Could not get twitch auth token: check client_id and client_secret`

IGDB creds are wrong or revoked on the Twitch side.

1. Go to [dev.twitch.tv/console/apps](https://dev.twitch.tv/console/apps).
2. Verify your application still exists.
3. Regenerate the Client Secret, and copy both Client ID and Client Secret.
4. Update `IGDB_CLIENT_ID` and `IGDB_CLIENT_SECRET` in your env.
5. `docker compose up -d` to pick up the new values.

## Password logins are disabled, OIDC is broken, I'm locked out

You set `DISABLE_USERPASS_LOGIN=true` and now OIDC isn't working.

1. Edit your compose/env to unset `DISABLE_USERPASS_LOGIN` (or set it to `false`).
2. `docker compose up -d` to restart with the new config.
3. Log in with your local admin and fix OIDC with the steps below.
4. Re-enable `DISABLE_USERPASS_LOGIN` only after confirming OIDC works end-to-end.

This is the reason [OIDC Setup](../administration/oidc/index.md) tells you to verify OIDC before turning off local login.

## OIDC

### `redirect_uri_mismatch`

The `OIDC_REDIRECT_URI` in the env doesn't **exactly** match what's registered at the IdP. Check for:

- **Trailing slashes**: `/api/oauth/openid` vs `/api/oauth/openid/` are different to the IdP.
- **Scheme**: `http://` vs `https://`
- **Host**: `demo.romm.app` vs `www.demo.romm.app` vs the bare IP
- **Port**: implied `80`/`443` on HTTPS vs an explicit port

### User is created but stays a regular User, even though they should be Admin

You configured `OIDC_CLAIM_ROLES` but it's not being honoured.

1. **Is the claim actually sent?** Decode your IdP's ID token at [jwt.io](https://jwt.io), or check its UserInfo response, and verify the claim name (e.g. `groups`, `realm_access.roles`) is present and non-empty. RomM reads the ID token first and falls back to UserInfo for a claim it leaves out.
2. **Does the value match?** `OIDC_ROLE_ADMIN=romm-admin` will only match if the claim contains exactly the string `romm-admin`, and it's case-sensitive.
3. **Is the claim mapper on the IdP side configured to include the claim?** On Keycloak, for example, you need a Client Scope with a Group Membership mapper added to the client.

Roles are re-evaluated on every login with no cache to bust, so log out and back in to test the fix.

### `User has not been granted any roles for this application.`

A newly created (non-admin) user logs in and is rejected with:

```json
{ "detail": "User has not been granted any roles for this application." }
```

You set `OIDC_CLAIM_ROLES`, which makes RomM require every user to match at least one mapped role group. Admins work because they match `OIDC_ROLE_ADMIN`, but users in no mapped group are turned away.

Fix: map your non-admin group to the **User** role with `OIDC_ROLE_VIEWER` (or `OIDC_ROLE_EDITOR`), pointing at a group all your regular users belong to:

```yaml
environment:
    - OIDC_CLAIM_ROLES=groups
    - OIDC_ROLE_ADMIN=romm-admin,platform-admins
    - OIDC_ROLE_VIEWER=platform-users # grants login to non-admins
```

`OIDC_ROLE_VIEWER` and `OIDC_ROLE_EDITOR` both resolve to **User**, but they still grant access when role claims are enabled (see [Role mapping](../administration/oidc/index.md#role-mapping)).

### "Email is missing from token"

Neither the ID token nor the provider's UserInfo endpoint returned an `email` claim. Check that the client requests the `email` scope and that the provider releases it. On Zitadel, also open the application → **Token Settings** → tick **User Info inside ID Token** → Save (see [OIDC with Zitadel → Enable claims](../administration/oidc/zitadel.md) for the full walkthrough).

### Authentik 2025.10: login succeeds but the user is rejected

Authentik 2025.10 changed the default `email_verified` claim from `true` to `false`. RomM requires a verified email, so the claim must arrive as `true`.

Fix: add the property mapping documented in [OIDC with Authentik → Create a property mapping](../administration/oidc/authentik.md#2-create-a-property-mapping-authentik-202510).

### Keycloak: user created locally but can't log in

Two possibilities:

1. **Email not verified in Keycloak**: Admin Console → Users → open the user → **Email Verified**: on. Unverified emails are rejected.
2. **Email mismatch between Keycloak and a pre-existing local user**: if a local account `alice@example.com` already exists, the first OIDC login for `alice@example.com` signs into that account. If the emails don't match exactly, a _second_ account is created. Fix: edit the local user to set the correct email, then log in via OIDC.

### `This account is linked to a different identity at the provider`

The login's email belongs to a RomM account that is already linked to another user (subject) at the same provider. RomM refuses it so that an email reassigned at the provider can't take over the account. It also happens when you delete and recreate the user at the provider.

If the new provider user really is the account's owner, clear the stored link in the database, then log in again to relink it:

```sql
UPDATE users SET oidc_issuer = NULL, oidc_sub = NULL WHERE username = 'alice';
```

### Signing in at the provider lands back on the RomM login page

You authenticate at the provider, but end up on `/login?bypass_autologin=true` instead of signed in. RomM rejected the provider's callback, for example because the provider returned an error, the authorization code was already used or expired, or the ID token failed validation. The `bypass_autologin` flag keeps `OIDC_AUTOLOGIN` from sending you straight back into the same failure.

The container log names the reason on an `OIDC callback rejected` line:

```sh
docker logs romm 2>&1 | grep -i "OIDC callback rejected"
```

Common causes are clock drift (see below), a client secret that changed at the provider, or a provider that expects a different redirect URI.

### `certificate verify failed` when RomM talks to the provider

Your provider's certificate is signed by a private CA that the container doesn't trust. Mount the CA certificate and point `OIDC_TLS_CACERTFILE` at it (see [OIDC Setup → Private certificate authority](../administration/oidc/index.md#private-certificate-authority)). The certificate is trusted in addition to the system CAs, so public providers keep working.

### `OAuthException: expired token` on callback

Your host and the IdP have significant clock drift, so run NTP on both.

### Autologin loops forever

You set `OIDC_AUTOLOGIN=true` and your IdP keeps bouncing you back, which bounces you back to the IdP.

This usually happens because something else in the chain (a CSRF check, a cookie domain mismatch, a reverse-proxy rewrite) is breaking the post-callback handoff. To escape:

1. Hit `/login?bypass_autologin=true` directly to land on the normal login page.
2. Sign in as a local admin.
3. Disable `OIDC_AUTOLOGIN`, restart, and debug the IdP config with autologin off.

Since 5.4, a callback the provider or RomM rejects already redirects to `/login?bypass_autologin=true`, so a loop usually means the callback succeeds but the session doesn't stick, which points at cookies or the proxy. If `bypass_autologin` doesn't work in your version, shell into the container and unset `OIDC_AUTOLOGIN` in the env, or edit your compose and restart.

## Still stuck?

- Check the container logs: `docker logs romm 2>&1 | grep -iE 'auth|oidc|oauth'`.
- Cross-reference your IdP's audit logs, which often show exactly why a login was rejected on their side.
- Ask on [Discord](https://discord.gg/romm) `#help` with the IdP name and the exact error text.
