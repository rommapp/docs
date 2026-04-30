---
title: OIDC with PocketID
description: Wire up SSO to PocketID
---

# OIDC with PocketID

[PocketID](https://github.com/stonith404/pocket-id) is a minimalist OIDC provider that **only** supports passkey authentication, with no passwords. Before starting, read the [OIDC Setup overview](index.md), as it covers the RomM-side settings common to every provider.

## 1. Prerequisites

PocketID installed, running, and your admin passkey already registered via their [PocketID setup guide](https://github.com/stonith404/pocket-id#setup).

## 2. Add the client

In PocketID admin:

1. **Application Configuration**: make sure **Emails Verified** is tickedas RomM requires verified emails.
2. Go to **OIDC Client** → **Add OIDC Client**.
3. Fill in:
    - **Name**: `RomM`
    - **Callback URLs**: `https://demo.romm.app/api/oauth/openid`
4. **Save**. Stay on this page as the client secret only displays **once**.
5. Copy both the Client ID and Client Secret now.

## 3. Configure RomM

```yaml
environment:
    - OIDC_ENABLED=true
    - OIDC_PROVIDER=pocket-id
    - OIDC_CLIENT_ID=<from PocketID>
    - OIDC_CLIENT_SECRET=<from PocketID>
    - OIDC_REDIRECT_URI=https://demo.romm.app/api/oauth/openid
    - OIDC_SERVER_APPLICATION_URL=https://id.example.com
    - ROMM_BASE_URL=https://demo.romm.app
```

`OIDC_SERVER_APPLICATION_URL` is the root URL of your PocketID instance.

## 4. Set your email

RomM → **Profile** → set your email to exactly the same address PocketID has for you.

![Set email](../../resources/authelia/1-user-profile.png)

## 5. Test

Restart, navigate to `/login` and click the **Login with OIDC** button. You're redirected to PocketID → authenticate → bounced back and signed in!

![Login with OIDC](../../resources/pocketid/2-romm-login.png)

If it doesn't work, head to [Authentication Troubleshooting](../../troubleshooting/authentication.md).
