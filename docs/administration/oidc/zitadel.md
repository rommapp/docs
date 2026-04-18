---
title: OIDC with Zitadel
description: Wire RomM's SSO to Zitadel: project, application, user info inside ID token, RomM env vars.
---

# OIDC with Zitadel

[Zitadel](https://zitadel.com/) is an enterprise-grade open-source IAM platform supporting OAuth2, OIDC, SAML, and passwordless. Good fit when you want an enterprise-ish IdP without running Keycloak.

Before starting, read the [OIDC Setup overview](index.md); it covers the RomM-side settings common to every provider.

## 1. Prerequisites

Zitadel installed and running. Upstream: [self-hosted deployment docs](https://zitadel.com/docs/self-hosting/deploy/overview). Change the default organization password before you go further.

## 2. Create a project

Create a new project (e.g. `RomM`). This holds the client and its auth settings.

On the project's **General** tab, the toggles mean:

- **Assert Roles on Authentication**: not useful today; RomM 5.0 reads roles via `OIDC_CLAIM_ROLES` regardless. Leave off unless you're setting up role mapping.
- **Check authorization on Authentication**: recommended. If off, anyone who can register in Zitadel can sign into RomM (as Viewer). Turn this on if Zitadel registration is open.
- **Check for Project on Authentication**: only matters if you're separating users by Zitadel organization. Skip for a single RomM instance.

### 2.5 (Optional) Grant users to the project

If you enabled **Check authorization on Authentication**:

1. **Authorization** tab → **New**.
2. Select user(s) → **Continue**.
3. "No role has been created yet" is fine: just **Save**. The user appears in the authorization list with no roles.

## 3. Create the application

On the project's **General** tab, under **Applications**, click **New**. Tick **I'm a pro. Skip this wizard** for the fast path.

- **Name**: `RomM`
- **Application Type**: `Web`
- **Grant Types**: `Authorization Code`
- **Response Types**: `Code`
- **Authentication Method**: `Basic`
- **Redirect URIs**: `https://romm.example.com/api/oauth/openid`
- **Post Logout URIs**: `https://romm.example.com/`

Click **Create**. The **client secret is shown once**; copy it now.

## 4. Enable claims in the ID Token

Without this, RomM throws "Email is missing from token" on login.

Open the application's **Token Settings** tab → tick **User Info inside ID Token** → **Save**.

## 5. Configure RomM

```yaml
environment:
  - OIDC_ENABLED=true
  - OIDC_PROVIDER=zitadel
  - OIDC_CLIENT_ID=<from Zitadel>
  - OIDC_CLIENT_SECRET=<from Zitadel>
  - OIDC_REDIRECT_URI=https://romm.example.com/api/oauth/openid
  - OIDC_SERVER_APPLICATION_URL=https://zitadel.example.com
  - ROMM_BASE_URL=https://romm.example.com
```

Zitadel's OIDC discovery URL is at `<OIDC_SERVER_APPLICATION_URL>/.well-known/openid-configuration`, handy for debugging.

For role mapping from Zitadel, see [OIDC Setup → Role mapping](index.md#role-mapping-50).

## 6. Set email on RomM + Zitadel

In RomM → **Profile** → set your email to exactly the same address your Zitadel user has.

## 7. Test

Restart RomM and open `/login`. Click **Login with Zitadel**; you're redirected, authenticate, and bounce back signed into RomM.

If it doesn't work, head to [Authentication Troubleshooting](../../troubleshooting/authentication.md).
