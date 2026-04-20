---
title: Invitations & Registration
description: Inviting users, public signup, the first-user flow, and role assignment at sign-up.
---

# Invitations & Registration

Three ways a new account ends up on a RomM instance:

1. **First-user setup**: the person who completes the Setup Wizard.
2. **Invite link**: an admin generates a one-shot link carrying a pre-assigned role.
3. **Public registration**: anyone who reaches `/register` signs themselves up as a Viewer. Off by default.
4. **OIDC auto-provisioning**: first login through your IdP creates a matching account. Covered in [OIDC Setup](oidc/index.md).

## First-user setup

When a fresh RomM container starts against an empty database, hitting any page redirects to the **Setup Wizard**. The wizard collects a username, email, and password. The resulting account is **always an Admin**, regardless of any env var.

To skip the wizard (e.g. when provisioning via automation and you'll create users through the API), set:

```yaml
environment:
    - DISABLE_SETUP_WIZARD=true
```

You'll then need to create the first admin via the API or by injecting a row at deploy time, because the UI won't offer a setup flow.

## Invite links

The recommended way to add users, because it avoids you ever touching their password.

1. **Administration → Users → Invite.** Pick a role (Viewer, Editor, Admin).
2. RomM generates a single-use URL. Copy it and send it to the invitee.
3. When they open it, they pick their own username and password. RomM creates the account with the role you chose and logs them straight in.

Invite tokens are **single-use** and **time-limited**. Defaults:

| Setting | Default | Env var             |
| ------- | ------- | ------------------- |
| Expiry  | 30 days | `INVITE_TOKEN_DAYS` |

Expired links return a clear error on the `/register` page. Generate a new one from the Users panel.

<!-- prettier-ignore -->
!!! tip "Invitations over HTTPS"
    Invite URLs include a signed token, so they're not useful to anyone without RomM's `ROMM_AUTH_SECRET_KEY`. Still, send them over a trusted channel, because once someone has a valid invite URL, they can claim the account.

## Public self-registration

Off by default. To let anyone with the `/register` URL create a Viewer account with no invite:

```yaml
environment:
    - ALLOW_PUBLIC_REGISTRATION=true
```

When on, the login page grows a "Register" link and `/register` becomes an open endpoint.

Appropriate for:

- Instances behind auth at the reverse-proxy layer (Authelia, Cloudflare Access, an IP allowlist). RomM's registration is just paperwork once the proxy has already authenticated the visitor.
- Truly public or group-shared instances where you genuinely want open signup

Inappropriate for everything else. **If RomM is exposed to the internet with no upstream auth, leave this off**: it's the single fastest way to fill your DB with spam accounts.

Anyone who signs up this way is a Viewer. Promote them manually from **Administration → Users → Edit** if needed.

## Role assignment at sign-up

| Sign-up method                                         | Role assigned                                                |
| ------------------------------------------------------ | ------------------------------------------------------------ |
| First-user Setup Wizard                                | Admin (always)                                               |
| Invite link                                            | Whatever role the admin picked when generating the link      |
| Public registration (`ALLOW_PUBLIC_REGISTRATION=true`) | Viewer                                                       |
| OIDC first login                                       | Default Viewer, or mapped from claims via `OIDC_CLAIM_ROLES` |

Changing a user's role afterwards is a normal admin action. See [Users & Roles](users-and-roles.md).

## Password reset

Admins can reset passwords manually in **Administration → Users → Edit → New password**. A temporary password will be printed to the container's logs.

See [Authentication](authentication.md) for the session and token side of the auth model.
