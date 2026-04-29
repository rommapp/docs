---
title: OIDC with Authentik
description: Wire up SSO to Authentik
---

# OIDC with Authentik

[Authentik](https://goauthentik.io/) is a full-featured open-source IdP with MFA, flows, and a sizeable audit/admin surface. Before starting, read the [OIDC Setup overview](index.md), as it covers the RomM-side settings common to every provider.

## 1. Prerequisites

Authentik installed and running via their [install guide](https://docs.goauthentik.io/docs/install-config/install/docker-compose).

Log in as admin and open **Admin Interface**.

![Authentik user dashboard](../../resources/authentik/1-user-dashboard.png)

## 2. Create a property mapping (Authentik 2025.10+)

<!-- prettier-ignore -->
!!! important "Authentik 2025.10 breaking change"
    In version 2025.10, Authentik changed the default of `email_verified` from `true` to `false`. RomM requires a verified email, so without this property mapping, authentication silently fails.

In **Customization → Property Mappings → Create → Scope Mapping**:

- **Name**: `RomM Email Verification`
- **Scope name**: `email`
- **Expression**:

    ```py
    return {
        "email": user.email,
        "email_verified": True,
    }
    ```

![Property Mapping](../../resources/authentik/propperty-mapping.png)

Click **Create**. Upstream reference: [Authentik scope mappings](https://version-2025-10.goauthentik.io/add-secure-apps/providers/property-mappings/#scope-mappings-with-oauth2).

## 3. Create a provider

**Admin → Providers → Create**.

![Create a new provider](../../resources/authentik/2-create-provider.png)

Choose **OAuth2/OpenID Provider**.

![Select OAuth2 provider](../../resources/authentik/3-new-provider.png)

Configure:

- **Name**: `RomM OIDC Provider`
- **Authorization flow**: implicit consent
- **Redirect URIs**: `https://demo.romm.app/api/oauth/openid`
- **Scopes**: Under "Advanced protocol settings", move the property mapping you created above from "Available Scopes" to "Selected Scopes". You'll also need to make sure any existing mappings of `email` or `email_verified` are disabled. Authentik has an `email` mapping by default, so make sure to check for this and remove it if it's present.

Copy the generated **Client ID** and **Client Secret**. You'll use them as `OIDC_CLIENT_ID` / `OIDC_CLIENT_SECRET` on the RomM side.

![Provider settings](../../resources/authentik/4-provider-secrets.png)

Click **Create**.

## 4. Register the application

**Admin → Applications → Create**.

![Applications](../../resources/authentik/5-applications.png)

- **Name**: `RomM`
- **Slug**: `romm`
- **Provider**: the `RomM OIDC Provider` you just made

![New application](../../resources/authentik/6-new-application.png)

Click **Create**.

## 5. Configure RomM

```yaml
environment:
    - OIDC_ENABLED=true
    - OIDC_PROVIDER=authentik
    - OIDC_CLIENT_ID=<from Authentik>
    - OIDC_CLIENT_SECRET=<from Authentik>
    - OIDC_REDIRECT_URI=https://demo.romm.app/api/oauth/openid
    - OIDC_SERVER_APPLICATION_URL=https://auth.example.com/application/o/romm
    - ROMM_BASE_URL=https://demo.romm.app
```

Note that `OIDC_SERVER_APPLICATION_URL` points at the per-application URL (`/application/o/<slug>`), not the Authentik root.

For role mapping from Authentik groups, see [OIDC Setup → Role mapping](index.md#role-mapping).

## 6. Set your email on RomM

In RomM → **Profile** → set your email to exactly the same address Authentik has for you.

![Set email](../../resources/authentik/7-user-profile.png)

## 7. Test

Restart RomM, navigate to `/login` and click the **Login with OIDC** button. You're redirected to Authentik → authenticate → bounced back and signed into RomM!

![Login with OIDC](../../resources/authentik/8-romm-login.png)

If it doesn't work, head to [Authentication Troubleshooting](../../troubleshooting/authentication.md).
