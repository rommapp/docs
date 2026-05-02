---
title: OIDC with Keycloak
description: Wire up SSO to Keycloak
---

# OIDC with Keycloak

[Keycloak](https://www.keycloak.org/) is the heavyweight open-source IAM standard. Before starting, read the [OIDC Setup overview](index.md), as it covers the RomM-side settings common to every provider.

## 1. Prerequisites

Keycloak installed and running via their [getting started guide](https://www.keycloak.org/getting-started).

Log into the **Admin Console** and either create a new realm for the app or reuse an existing one.

## 2. Add a client

In the Admin Console, select your realm → **Clients** → **Create client**.

1. **Client type**: `OpenID Connect`.
2. **Client ID**: `romm` (or something unique).
3. Click **Next**.
4. On the capability page:
    - Enable **Client authentication**
    - Leave only **Standard flow** enabled
    - Click **Next**
5. Set URLs:
    - **Root URL**: `https://demo.romm.app`
    - **Valid Redirect URIs**: `https://demo.romm.app/api/oauth/openid`
    - **Web origins**: `https://demo.romm.app`
6. Save, then head to the **Credentials** tab and copy the **Client Secret**.

## 3. Configure

```yaml
environment:
    - OIDC_ENABLED=true
    - OIDC_PROVIDER=keycloak
    - OIDC_CLIENT_ID=romm
    - OIDC_CLIENT_SECRET=<from Keycloak Credentials tab>
    - OIDC_REDIRECT_URI=https://demo.romm.app/api/oauth/openid
    - OIDC_SERVER_APPLICATION_URL=https://keycloak.example.com/realms/<realm-name>
    - ROMM_BASE_URL=https://demo.romm.app
```

`OIDC_SERVER_APPLICATION_URL` must include the realm (`.../realms/<realm-name>`), not just the Keycloak root.

## 4. Set email + verify in Keycloak

In **Profile** → set your email to the same address Keycloak has for you.

On the Keycloak side, go to **Admin Console → Users** and mark each user's email as **verified**. Users with unverified emails will be rejected on login.

## 5. Test

Restart, navigate to `/login` and click the **Login with OIDC** button. You're redirected to Keycloak → authenticate → bounced back and signed in!

If a local user already exists with a matching email, they're signed into that account. Otherwise a new account is created with Viewer permissions.

If it doesn't work, head to [Authentication Troubleshooting](../../troubleshooting/authentication.md).

## 6. (Optional) Disable local password logins

Force users through Keycloak:

```yaml
environment:
    - DISABLE_USERPASS_LOGIN=true
```

<!-- prettier-ignore -->
!!! warning
    Before flipping this, confirm at least one Admin account can sign in via OIDC, otherwise a broken OIDC flow locks you out.

## 7. (Optional) Role mapping

By default, new OIDC users come in as Viewers. To map Keycloak roles/groups to local roles:

```yaml
environment:
    - OIDC_CLAIM_ROLES=groups # or realm_access.roles, depending on your token
    - OIDC_ROLE_VIEWER=romm-viewer
    - OIDC_ROLE_EDITOR=romm-editor
    - OIDC_ROLE_ADMIN=romm-admin
```

Configure Keycloak's client to include the role/group claim in the ID token (usually via a **Group Membership** or **Realm Role** client scope mapper). Values in the claim are compared against the `OIDC_ROLE_*` env vars on every login, so demoting in Keycloak takes effect on the user's next sign-in.

See [OIDC Setup → Role mapping](index.md#role-mapping) for the generic version.
