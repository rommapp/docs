---
title: OIDC with VoidAuth
description: Wire up SSO to VoidAuth
---

# OIDC with VoidAuth

[VoidAuth](https://voidauth.app/) is an open-source SSO authentication and user management provider that stands guard in front of your self-hosted application. Before starting, read the [OIDC Setup overview](index.md), as it covers the RomM-side settings common to every provider.

## 1. Prerequisites

VoidAuth installed and running via their [self-hosted deployment docs](https://voidauth.app/#/?id=quick-start). We will use the APP_URL provided in the compose.yml exemple for reference in this documentation : https://auth.example.com
Your RomM instance will be referenced as https://demo.romm.app .

## 2. Create a new app

Login as an admin in VoidAuth web interface. Create a new OIDC Apps  (e.g. `RomM`). 

- **Name**: `RomM`
- **Home Page URL**: `https://romm.example.com`
- **Logo URL**: `https://github.com/HydrelioxGitHub/romm-docs/blob/main/.github/resources/isotipo.png?raw=true`
- **Group**: You could add a group that the user must belong to get access to your RomM instance. If left empty, any user created in your VoidAuth instance will be allowed.
- **Skip Consent** and **MFA Required** : This options could be checked or not as you wish.
- **Client ID**: Generate an ID using the button
- **Auth Method**: `Client Secred Basic`
- **Client Secret**: Generate a secret using the button
- **Redirect URLs**: add `https://demo.romm.app/api/oauth/openid`
- **Response Types**: check `code`
- **Grant Types**: check `authorization_code` and `refresh_token`
- **Post Logout URL**: `https://demo.romm.app/`

Don't forget to click on the `Create` button to valid your app.

## 3. Configure

```yaml
environment:
    - OIDC_ENABLED=true
    - OIDC_PROVIDER=VoidAuth
    - OIDC_CLIENT_ID=<from VoidAuth>
    - OIDC_CLIENT_SECRET=<from VoidAuth>
    - OIDC_REDIRECT_URI=https://demo.romm.app/api/oauth/openid
    - OIDC_SERVER_APPLICATION_URL=https://auth.example.com
    - OIDC_SERVER_METADATA_URL=https://auth.example.com/oidc/.well-known/openid-configuration
    - ROMM_BASE_URL=https://demo.romm.app
```

VoidAuth's OIDC discovery URL can be found at the top of your OIDC App page, by clicking on OIDC Endpoints.

For role mapping from VoidAuth, see [OIDC Setup → Role mapping](index.md#role-mapping).

## 4. Test

Restart, navigate to `/login` and click the **Login with VoidAuth** button. You're redirected to VoidAuth → authenticate → bounced back and signed in!

If it doesn't work, head to [Authentication Troubleshooting](../../troubleshooting/authentication.md).
