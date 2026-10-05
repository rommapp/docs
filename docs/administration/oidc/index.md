---
title: OIDC Setup
description: Wire up to an OpenID Connect provider for SSO and centralised user management
---

# OIDC Setup

OpenID Connect (OIDC) lets users sign in through an external identity provider: Authelia, Authentik, Keycloak, PocketID, Zitadel, Okta, Auth0, VoidAuth, or anything standards-compliant. You get single sign-on across your homelab and centralised MFA, with no app-specific password to manage, and you can map OIDC groups or claims to roles.

<!-- prettier-ignore -->
!!! note "OIDC is optional"
    The local user system works fine without OIDC. Enable OIDC when you already run an IdP and want auth to follow suit, or when you want to unify user management across multiple apps.

## How it works

1. User clicks the OIDC login button on `/login`.
2. They're redirected to your provider.
3. They authenticate (password, passkey, MFA, whatever your provider enforces).
4. Provider redirects back to `{ROMM_BASE_URL}/api/oauth/openid` with an authorisation code.
5. The code is exchanged for an ID token and the user's email, username and role claims are read. Claims the ID token leaves out are fetched from the provider's UserInfo endpoint.
6. The matching local user is logged in (see [Account matching](#account-matching)), or a new one is created on the fly unless you've [turned off registration](#auto-provisioning).

If the provider returns an error, or the callback fails validation, RomM logs the reason on an `OIDC callback rejected` line and sends the browser to `/login?bypass_autologin=true`, where the bypass flag keeps [autologin](#autologin) from looping straight back to the provider.

## Provider guides

Pick your provider and follow the step-by-step instructions. Every guide ends with the same set of app-side env vars and differs only in how you register the app and where you find the client ID and secret.

- [Authelia](authelia.md)
- [Authentik](authentik.md)
- [Keycloak](keycloak.md)
- [PocketID](pocketid.md)
- [Zitadel](zitadel.md)
- [VoidAuth](voidauth.md)

Not listed? Most standards-compliant OIDC providers work: Okta, Auth0, Google Workspace, Microsoft Entra, etc. Use one of the above as a template and consult your provider's docs for the registration side.

## Minimum config

Whichever provider you pick, set these in the `romm` service's environment:

```yaml
environment:
    - OIDC_ENABLED=true
    - OIDC_PROVIDER=<authelia|authentik|keycloak|pocket-id|zitadel|voidauth|generic>
    - OIDC_CLIENT_ID=<from your provider>
    - OIDC_CLIENT_SECRET=<from your provider>
    - OIDC_SERVER_APPLICATION_URL=https://auth.example.com
    - OIDC_REDIRECT_URI=https://demo.romm.app/api/oauth/openid
    - ROMM_BASE_URL=https://demo.romm.app # must match your reverse-proxy URL
```

`OIDC_REDIRECT_URI` must exactly match what you register at the provider (same scheme, host, path, no trailing slash).

## Private certificate authority

If your provider's HTTPS certificate comes from a private CA, such as a homelab step-ca or an internal Active Directory CA, RomM can't verify it out of the box. Mount the CA certificate into the container and point `OIDC_TLS_CACERTFILE` at it:

```yaml
environment:
    - OIDC_TLS_CACERTFILE=/romm/config/ca/homelab-root.pem
volumes:
    - ./ca:/romm/config/ca:ro
```

The path can be a single bundle file or a directory, in which case every file in it is read, and PEM, DER and PKCS#7 (`.p7b`) certificates all work. RomM trusts these certificates alongside the system CAs, so public providers keep working. A path that doesn't exist, or a file with no certificate in it, is logged and skipped.

## Auto-provisioning

By default, the first successful OIDC login for an email that has no matching account creates a local account automatically. To require accounts to exist beforehand (so only pre-provisioned users can sign in via OIDC), turn registration off:

```yaml
environment:
    - OIDC_ALLOW_REGISTRATION=false # default: true
```

With it disabled, an unknown user is rejected at login instead of getting a fresh account. New accounts land in the [default permission group](../users-and-roles.md#permission-groups) unless a role claim maps them to Admin.

## Role mapping

RomM has only two roles: **User** and **Admin** (see [Users & Roles](../users-and-roles.md#roles)). New OIDC users are provisioned as **Users**. To let your IdP promote someone to **Admin** based on group membership, set:

```yaml
environment:
    - OIDC_CLAIM_ROLES=groups # which claim to read
    - OIDC_ROLE_ADMIN=romm-admin,platform-admins # group values → Admin
```

On every login, the claim named by `OIDC_CLAIM_ROLES` is read (often `groups`, or `realm_access.roles` on Keycloak, so check your provider's ID token or UserInfo response). If a value matches `OIDC_ROLE_ADMIN`, the user becomes an Admin.

Roles are re-evaluated on every login, so demoting someone on the IdP side takes effect the next time they sign in.

<!-- markdownlint-disable MD046 -->
<!-- prettier-ignore -->
!!! warning "Once `OIDC_CLAIM_ROLES` is set, users must match a mapped group"
    As soon as `OIDC_CLAIM_ROLES` is configured, RomM expects every user to match at least one mapped role group. A user whose claim matches none of the configured groups is rejected at login with:

    ```json
    {"detail":"User has not been granted any roles for this application."}
    ```

    To let non-admin users in, map their group to the **User** role with `OIDC_ROLE_VIEWER` (or `OIDC_ROLE_EDITOR`):

    ```yaml
    environment:
        - OIDC_CLAIM_ROLES=groups
        - OIDC_ROLE_ADMIN=romm-admin,platform-admins # → Admin
        - OIDC_ROLE_VIEWER=platform-users # non-admins → User (grants access)
    ```

    `OIDC_ROLE_VIEWER` and `OIDC_ROLE_EDITOR` no longer map to distinct roles (matching users all resolve to **User**), but they're still how you grant those users access when role claims are enabled. Point them at a group that all your non-admin users belong to. Only `OIDC_ROLE_ADMIN` changes the role, so use [permission groups](../users-and-roles.md#permission-groups) for finer-grained access.

    If you don't set `OIDC_CLAIM_ROLES` at all, role mapping is skipped entirely and everyone is provisioned as a **User** in the default permission group.

<!-- markdownlint-enable MD046 -->

## Account matching

The first OIDC login for an existing local account matches it by email, so set the account's email to exactly the address your provider has for the user. That login links the account to the user's identity at the provider (the token's `iss` issuer and `sub` subject). Every later login matches on that identity:

- **Email changes at the provider carry over.** The user still signs into the same account, and RomM stores the new email, unless another account already uses it.
- **Switching providers keeps accounts.** A login from a new issuer matches by email again and relinks the account to the new provider.
- **A new subject for a linked email is refused.** When the same provider sends a different subject for an email that is already linked, RomM rejects the login with a 403 rather than hand the account to someone else. This happens when the provider reassigns the email or recreates the user. See [Authentication Troubleshooting](../../troubleshooting/authentication.md#this-account-is-linked-to-a-different-identity-at-the-provider) to relink it.

## Autologin

To bypass the login page entirely and redirect straight to the IdP, so RomM feels like a native part of your SSO stack:

```yaml
environment:
    - OIDC_AUTOLOGIN=true
```

Combine with `DISABLE_USERPASS_LOGIN=true` to lock out local accounts entirely.

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

The endpoint URL is provider-specific, so check the per-provider guides or your IdP's docs.

## Username source

By default the local part of the email (the bit before `@`) becomes the username, but you can override it with:

```yaml
environment:
    - OIDC_USERNAME_ATTRIBUTE=preferred_username
```

Whatever that attribute holds gets sanitised before it becomes a username to prevent invalid characters from being used. RomM also sends a PKCE challenge on every authorization request, so it's safe to mark PKCE required for the client if your IdP offers that.

## Important notes

- **Email must match** between OIDC and an existing local account on its first OIDC login, otherwise OIDC creates a new account alongside the old one. After that, the account follows the user's identity at the provider (see [Account matching](#account-matching)).
- **HTTPS is required** in production, as OIDC will refuse to redirect to a plain-HTTP `ROMM_BASE_URL`.
- Large drift between the RomM host and IdP will lead to **clock skew** and cause ID-token validation to fail.

## Troubleshooting

Common failures and fixes live in [Authentication Troubleshooting](../../troubleshooting/authentication.md). Two of the usual suspects:

- `redirect_uri_mismatch`: `OIDC_REDIRECT_URI` differs from what's registered at the provider. A trailing slash alone is enough to trigger it.
- User created but not made Admin: check `OIDC_CLAIM_ROLES` points at a claim that actually exists in the ID token or the UserInfo response, and that the group values match `OIDC_ROLE_ADMIN` exactly (case-sensitive).
