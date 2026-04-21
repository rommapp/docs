---
title: Invitations & Registration
description: Inviting users, the first-user flow, and role assignment.
---

# Invitations & Registration

There are three ways a new account ends up on a RomM instance:

1. **First-admin setup**: the person who completes the Setup Wizard.
2. **Invite link**: an admin generates a one-shot link carrying a pre-assigned role.
3. **OIDC auto-provisioning**: first login through your IdP creates a matching account (covered in [OIDC Setup](oidc/index.md)).

## First-admin setup

When a fresh RomM container starts against an empty database, hitting any page redirects to the **Setup Wizard**. The wizard collects a username, email, and password. The resulting account is **always an Admin**, regardless of any env var.

To skip the wizard (e.g. when provisioning via automation and you'll create users through the API), set:

```yaml
environment:
    - DISABLE_SETUP_WIZARD=true
```

You'll then need to create the first admin via the API or by injecting a database row at deploy time, because the UI won't offer a setup flow.

## Invite links

The recommended way to add users, because it avoids you ever touching their password.

1. **Administration → Users c Invite.** Pick a role (Viewer, Editor, Admin).
2. RomM generates a single-use URL → copy it and send it to the invitee.
3. When they open it, they pick their own username and password.
4. RomM creates the account with the role you chose and logs them straight in.

Invite tokens are **single-use** and **time-limited**. Defaults:

| Setting | Default | Env var             |
| ------- | ------- | ------------------- |
| Expiry  | 30 days | `INVITE_TOKEN_DAYS` |

Expired links return a clear error on the `/register` page. Generate a new one from the Users panel.

## Role assignment at sign-up

| Sign-up method          | Role assigned                                                |
| ----------------------- | ------------------------------------------------------------ |
| First-user Setup Wizard | Admin (always)                                               |
| Invite link             | Whatever role the admin picked when generating the link      |
| OIDC first login        | Default Viewer, or mapped from claims via `OIDC_CLAIM_ROLES` |

Changing a user's role afterwards is a normal admin action. See [Users & Roles](users-and-roles.md).

## Password reset

Admins can reset passwords manually in **Administration → Users → Edit → New password**. A temporary password will be printed to the container's logs.
