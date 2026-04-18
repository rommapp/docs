---
title: OIDC with Keycloak
description: Wire RomM's SSO to Keycloak: realm, client, RomM env vars, optional role mapping.
---

# OIDC with Keycloak

[Keycloak](https://www.keycloak.org/) is the heavyweight open-source IAM standard. Feature-complete, well-documented, widely deployed. The default choice when your SSO needs are serious.

Before starting, read the [OIDC Setup overview](index.md). It covers the RomM-side settings common to every provider.

## 1. Prerequisites

Keycloak installed and running. Upstream: [Keycloak getting started](https://www.keycloak.org/getting-started).

Log into the **Admin Console** and either create a new realm for RomM or reuse an existing one.

## 2. Add a client

In the Admin Console, select your realm → **Clients** → **Create client**.

1. **Client type**: `OpenID Connect`.
2. **Client ID**: `romm` (or anything unique). Click **Next**.
3. On the capability page:
    - Enable **Client authentication**.
    - Leave only **Standard flow** enabled.
    - Click **Next**.
4. Set URLs:
    - **Root URL**: `https://romm.example.com`
    - **Valid Redirect URIs**: `https://romm.example.com/api/oauth/openid`
    - **Web origins**: `https://romm.example.com`
5. Save. Go to **Credentials** tab and copy the **Client Secret**.

## 3. Configure RomM

```yaml
environment:
  - OIDC_ENABLED=true
  - OIDC_PROVIDER=keycloak
  - OIDC_CLIENT_ID=romm
  - OIDC_CLIENT_SECRET=<from Keycloak Credentials tab>
  - OIDC_REDIRECT_URI=https://romm.example.com/api/oauth/openid
  - OIDC_SERVER_APPLICATION_URL=https://keycloak.example.com/realms/<realm-name>
  - ROMM_BASE_URL=https://romm.example.com
```

`OIDC_SERVER_APPLICATION_URL` must include the realm (`.../realms/<realm-name>`), not just the Keycloak root.

## 4. Set email on RomM + verify in Keycloak

In RomM → **Profile** → set your email to the same address Keycloak has for you.

On the Keycloak side, **Admin Console → Users**: mark each RomM user's email as **verified**. Users with unverified emails will be rejected on login.

## 5. Test

Restart RomM and open `/login`. Click **Login with Keycloak**. You're redirected to Keycloak, authenticate, and bounce back signed into RomM.

If a user already exists in RomM with a matching email, they're signed into that account. Otherwise RomM creates a new account with Viewer permissions.

If it doesn't work, head to [Authentication Troubleshooting](../../troubleshooting/authentication.md).

## 6. (Optional) Disable local password logins

Force users through Keycloak:

```yaml
environment:
  - DISABLE_USERPASS_LOGIN=true
```

!!! warning
    Before flipping this, confirm at least one Admin account can sign in via OIDC. Otherwise a broken OIDC flow locks you out.

## 7. (Optional) Role mapping

By default, new OIDC users come in as Viewers. To map Keycloak roles/groups to RomM roles:

```yaml
environment:
  - OIDC_CLAIM_ROLES=groups              # or realm_access.roles, depending on your token
  - OIDC_ROLE_VIEWER=romm-viewer
  - OIDC_ROLE_EDITOR=romm-editor
  - OIDC_ROLE_ADMIN=romm-admin
```

Configure Keycloak's client to include the role/group claim in the ID token (usually via a **Group Membership** or **Realm Role** client scope mapper). Values in the claim are compared against the `OIDC_ROLE_*` env vars on every login, so demoting in Keycloak takes effect on the user's next sign-in.

See [OIDC Setup → Role mapping](index.md#role-mapping-50) for the generic version.
