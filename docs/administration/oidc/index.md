---
title: OIDC Setup
description: Wire up to an OpenID Connect provider for SSO and centralised user management
---

# OIDC Setup

OpenID Connect (OIDC) lets users sign in through an external identity provider: Authelia, Authentik, Keycloak, PocketID, Zitadel, Okta, Auth0, or anything standards-compliant. Single sign-on across your homelab, no app-specific password to manage, centralised MFA, and map OIDC groups/claims to roles.

<!-- prettier-ignore -->
!!! note "OIDC is optional"
    The local user system works fine without OIDC. Enable OIDC when you already run an IdP and want auth to follow suit, or when you want to unify user management across multiple apps.

## How it works

1. User clicks the OIDC login button on `/login`.
2. They're redirected to your provider.
3. They authenticate (password, passkey, MFA, whatever your provider enforces).
4. Provider redirects back to `{ROMM_BASE_URL}/api/oauth/openid` with an authorisation code.
5. The code is exchanged for an ID token, the user's email and role claims are read, and either a matching local user is created on the fly or an existing one is logged in.

## Provider guides

Pick your provider and follow the step-by-step instructions. They all end with the same set of app-side env vars. The guides just differ on how to register the app and where to find the client ID/secret.

- [Authelia](authelia.md)
- [Authentik](authentik.md)
- [Keycloak](keycloak.md)
- [PocketID](pocketid.md)
- [Zitadel](zitadel.md)

Not listed? Most standards-compliant OIDC providers work: Okta, Auth0, Google Workspace, Microsoft Entra, etc. Use one of the above as a template and consult your provider's docs for the registration side.

## Minimum config

Whichever provider you pick, set these in the `romm` service's environment:

```yaml
environment:
    - OIDC_ENABLED=true
    - OIDC_PROVIDER=<authelia|authentik|keycloak|pocketid|zitadel|generic>
    - OIDC_CLIENT_ID=<from your provider>
    - OIDC_CLIENT_SECRET=<from your provider>
    - OIDC_SERVER_APPLICATION_URL=https://auth.example.com
    - OIDC_REDIRECT_URI=https://demo.romm.app/api/oauth/openid
    - ROMM_BASE_URL=https://demo.romm.app # must match your reverse-proxy URL
```

`OIDC_REDIRECT_URI` must exactly match what you register at the provider (same scheme, host, path, no trailing slash).

## Role mapping

By default, new OIDC users are provisioned as **Viewers**. To let your IdP assign roles based on group membership, set:

```yaml
environment:
    - OIDC_CLAIM_ROLES=groups # which claim to read
    - OIDC_ROLE_VIEWER=romm-viewer,guests # group names → Viewer
    - OIDC_ROLE_EDITOR=romm-editor
    - OIDC_ROLE_ADMIN=romm-admin,platform-admins
```

On every login, the claim named by `OIDC_CLAIM_ROLES` is read (often `groups`, sometimes `realm_access.roles` on Keycloak, check your provider's token output). Whichever role has a matching value wins. If nothing matches, the user stays/becomes a Viewer.

Roles are re-evaluated on **every login**, so demoting someone on the IdP side takes effect the next time they sign in.

## Autologin

To bypass the login page entirely and redirect straight to the IdP:

```yaml
environment:
    - OIDC_AUTOLOGIN=true
```

Useful when you want this to feel like a native part of your SSO stack. Combine with `DISABLE_USERPASS_LOGIN=true` to lock out local accounts entirely.

<!-- prettier-ignore -->
!!! warning "Keep one local admin"
    Don't set `DISABLE_USERPASS_LOGIN=true` without first confirming an admin account exists on the IdP side and can log in. If OIDC breaks and you've disabled local login, you're locked out until you fix the container env.

## RP-Initiated Logout

When set, hitting "Sign out" in RomM also signs the user out at the IdP:

```yaml
environment:
    - OIDC_RP_INITIATED_LOGOUT=true
    - OIDC_END_SESSION_ENDPOINT=https://auth.example.com/application/o/end-session/
```

The endpoint URL is provider-specific, check the per-provider guides or your IdP's docs.

## Username source

By default the local part of the email (the bit before `@`) becomes the username, but you can override it with:

```yaml
environment:
    - OIDC_USERNAME_ATTRIBUTE=preferred_username
```

## Important notes

- **Email must match** between OIDC and any existing local account, otherwise OIDC creates a new account alongside the old one.
- **HTTPS is required** in production, as OIDC will refuse to redirect to a plain-HTTP `ROMM_BASE_URL`.
- Large drift between the RomM host and IdP will lead to **clock skew** and cause ID-token validation to fail.

## Troubleshooting

Common failures and fixes live in [Authentication Troubleshooting](../../troubleshooting/authentication.md). Two of the usual suspects:

- `redirect_uri_mismatch`: `OIDC_REDIRECT_URI` differs from what's registered at the provider. Even a trailing slash can matter!
- User created but stuck at Viewer: check `OIDC_CLAIM_ROLES` points at a claim that actually exists in the token, and the group names match exactly (case-sensitive).
