---
title: Authentication Troubleshooting
description: Fix login, session, CSRF, and OIDC issues
---

# Authentication Troubleshooting

## `403 Forbidden` on API calls

When auth is enabled (almost always), any endpoint that requires a session returns `403` if:

- You're not authenticated.
- Your session is in a broken state (expired, signed with an old secret, missing CSRF).

Fix: [clear cookies](https://support.google.com/accounts/answer/32050) for the host and sign in again.

## `Forbidden (403) CSRF verification failed`

CSRF protection is on by default, so a mismatched or missing `csrftoken` cookie causes this.

1. Reload the page, and a fresh CSRF cookie is set on GET requests, which should fix it on the next POST.
2. Still broken? Clear cookies for the host and hard-reload (`CMD+SHIFT+R` / `CTRL+F5`).
3. As a last resort, disable CSRF verification with `DISABLE_CSRF_PROTECTION=true` in your env, but **we strongly discourage this** as it opens you up to CSRF attacks.

If you're behind a reverse proxy and CSRF keeps failing, the proxy is probably stripping the `csrftoken` cookie or the `X-CSRFToken` header. See the [Reverse Proxy recipes](../install/reverse-proxy.md). Every one of them forwards `Cookie` and all custom headers by default, so if yours doesn't, fix the proxy config.

## `400 Bad Request` on the WebSocket endpoint

Your reverse proxy is stripping the WebSocket upgrade, and live updates (scan progress, Netplay) use socket.io. Fixes for each proxy:

- **Nginx / NPM**: enable WebSockets Support (the [Reverse Proxy](../install/reverse-proxy.md) snippets already do this).
- **Traefik**: add `proxy_set_header Upgrade $http_upgrade` (or use the Traefik middleware equivalent).
- **Caddy**: WebSockets work out of the box with `reverse_proxy`.
- **Cloudflare**: enable **WebSockets** under Network settings.

## `Error: Could not get twitch auth token: check client_id and client_secret`

IGDB creds are wrong or revoked on the Twitch side.

1. Go to [dev.twitch.tv/console/apps](https://dev.twitch.tv/console/apps).
2. Verify your application still exists.
3. Regenerate the Client Secret, and copy both Client ID and Client Secret.
4. Update `IGDB_CLIENT_ID` and `IGDB_CLIENT_SECRET` in your env.
5. `docker compose up -d` to pick up the new values.

## Password logins are disabled, OIDC is broken, I'm locked out

You set `DISABLE_USERPASS_LOGIN=true` and now OIDC isn't working.

1. Edit your compose / env to unset `DISABLE_USERPASS_LOGIN` (or set it to `false`).
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
- **Port**: implied `80` / `443` on HTTPS vs an explicit port

### User is created but stays Viewer, even though they should be Admin

You configured `OIDC_CLAIM_ROLES` but it's not being honoured.

1. **Is the claim actually in the token?** Decode your IdP's ID token at [jwt.io](https://jwt.io) and verify the claim name (e.g. `groups`, `realm_access.roles`) is present and non-empty.
2. **Does the value match?** `OIDC_ROLE_ADMIN=romm-admin` will only match if the claim contains exactly the string `romm-admin`, and it's case-sensitive.
3. **Is the claim mapper on the IdP side configured to include the claim?** On Keycloak, for example, you need a Client Scope with a Group Membership mapper added to the client.

Roles are re-evaluated on every login with no cache to bust, so log out and back in to test the fix.

### "Email is missing from token" (Zitadel-specific)

On Zitadel, open the application → **Token Settings** → tick **User Info inside ID Token** → Save.

See [OIDC with Zitadel → Enable claims](../administration/oidc/zitadel.md) for the full walkthrough.

### Authentik 2025.10: login succeeds but the user is rejected

Authentik 2025.10 changed the default `email_verified` claim from `true` to `false` but a verified email is required so the claim must arrive as `true`.

Fix: add the property mapping documented in [OIDC with Authentik → Create a property mapping](../administration/oidc/authentik.md#2-create-a-property-mapping-authentik-202510).

### Keycloak: user created locally but can't log in

Two possibilities:

1. **Email not verified in Keycloak**: Admin Console → Users → open the user → **Email Verified**: on. Unverified emails are rejected.
2. **Email mismatch between Keycloak and a pre-existing local user**: if a local account `alice@example.com` already exists, the first OIDC login for `alice@example.com` signs into that account. If the emails don't match exactly, a _second_ account is created. Fix: edit the local user to set the correct email, then log in via OIDC.

### `OAuthException: expired token` on callback

Your host and the IdP have significant clock drift, so run NTP on both.

### Autologin loops forever

You set `OIDC_AUTOLOGIN=true` and your IdP keeps bouncing you back, which bounces you back to the IdP.

Usually because something else in the chain (a CSRF check, a cookie domain mismatch, a reverse-proxy rewrite) is breaking the post-callback handoff. To escape:

1. Hit `/login?bypass_autologin=true` directly to land on the normal login page.
2. Sign in as a local admin.
3. Disable `OIDC_AUTOLOGIN`, restart, and debug the IdP config with autologin off.

If `bypass_autologin` doesn't work in your version, shell into the container and unset `OIDC_AUTOLOGIN` in the env, or edit your compose and restart.

## Still stuck?

- Check the container logs: `docker logs romm 2>&1 | grep -iE 'auth|oidc|oauth'`.
- Cross-reference your IdP's audit logs, which often show exactly why a login was rejected on their side.
- Ask on [Discord](https://discord.gg/romm) `#help` with the IdP name and the exact error text.
