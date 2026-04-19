---
title: OIDC with Zitadel
description: Wire up SSO to Zitadel
---

# OIDC with Zitadel

[Zitadel](https://zitadel.com/) is an enterprise-grade open-source IAM platform supporting OAuth2, OIDC, SAML, and passwordless. Before starting, read the [OIDC Setup overview](index.md), as it covers the RomM-side settings common to every provider.

## 1. Prerequisites

Zitadel installed and running via their [self-hosted deployment docs](https://zitadel.com/docs/self-hosting/deploy/overview). Change the default organization password before you go further!

## 2. Create a project

Create a new project (e.g. `RomM`). This holds the client and its auth settings. On the **General** tab, **Check authorization on Authentication** is recommended. If turned off, anyone who can register in Zitadel can sign into RomM (as a Viewer). Turn this on if Zitadel registration is open.

### 2.5 (Optional) Grant users to the project

If you enabled **Check authorization on Authentication**:

1. **Authorization** tab → **New**.
2. Select user(s) → **Continue**.
3. "No role has been created yet" is fine, just **Save**.
4. The user appears in the authorization list with no roles.

## 3. Create the application

On the project's **General** tab, under **Applications**, click **New**. Tick **I'm a pro. Skip this wizard** for the fast path.

- **Name**: `RomM`
- **Application Type**: `Web`
- **Grant Types**: `Authorization Code`
- **Response Types**: `Code`
- **Authentication Method**: `Basic`
- **Redirect URIs**: `https://romm.example.com/api/oauth/openid`
- **Post Logout URIs**: `https://romm.example.com/`

Click **Create**. The **client secret is shown once**, copy it now!

## 4. Enable claims in the ID Token

Without this, RomM throws "Email is missing from token" on login. Open the application's **Token Settings** tab → tick **User Info inside ID Token** → **Save**.

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

Zitadel's OIDC discovery URL is at `<OIDC_SERVER_APPLICATION_URL>/.well-known/openid-configuration`, which is handy for debugging.

For role mapping from Zitadel, see [OIDC Setup → Role mapping](index.md#role-mapping).

## 6. Set email on RomM + Zitadel

In RomM → **Profile** → set your email to exactly the same address your Zitadel user has.

## 7. Test

Restart RomM, navigate to `/login` and click the **Login with OIDC** button. You're redirected to Zitadel → authenticate → bounced back and signed into RomM!

If it doesn't work, head to [Authentication Troubleshooting](../../troubleshooting/authentication.md).
