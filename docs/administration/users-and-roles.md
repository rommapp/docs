---
title: Users & Roles
description: User management, roles, and the scope model
---

# Users & Roles

RomM is multi-user from the start. The first user created during Setup is always an **Admin**, and everyone after that gets the role you assign when creating the account.

## Roles

| Role       | Who it's for                                                            | Default scopes                                                                |
| ---------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **Admin**  | You, and anyone you fully trust.                                        | All scopes, including user management and task execution.                     |
| **Editor** | Household members who help curate the library.                          | Read everything, edit ROMs/platforms/collections, upload, but no user management. |
| **Viewer** | Guests, kids, anyone who should only play and track their own progress. | Read the library, manage their own saves/states/screenshots/profile.          |

Roles are a convenience layer on top of **scopes** (see the scope matrix below for exactly what each role grants). You can't create custom roles (yet), so if you need finer-grained access, use the most restrictive role and rely on [Client API Tokens](../developers/client-api-tokens.md) for per-app customisation.

## Scope matrix

RomM authorisation is scope-based. Every API call and UI action maps to one or more scopes, and OAuth tokens and OIDC sessions carry a subset of them. Nineteen scopes total, grouped by resource:

| Scope               | Purpose                                         | Viewer | Editor | Admin |
| ------------------- | ----------------------------------------------- | :----: | :----: | :---: |
| `me.read`           | View own profile                                |   ✓    |   ✓    |   ✓   |
| `me.write`          | Edit own profile                                |   ✓    |   ✓    |   ✓   |
| `roms.read`         | Browse ROMs                                     |   ✓    |   ✓    |   ✓   |
| `roms.user.read`    | View own per-ROM data (rating, playtime, notes) |   ✓    |   ✓    |   ✓   |
| `roms.user.write`   | Edit own per-ROM data                           |   ✓    |   ✓    |   ✓   |
| `platforms.read`    | Browse platforms                                |   ✓    |   ✓    |   ✓   |
| `assets.read`       | View own saves/states/screenshots               |   ✓    |   ✓    |   ✓   |
| `assets.write`      | Upload saves/states/screenshots                 |   ✓    |   ✓    |   ✓   |
| `collections.read`  | Browse collections                              |   ✓    |   ✓    |   ✓   |
| `collections.write` | Create/edit collections                         |   -    |   ✓    |   ✓   |
| `roms.write`        | Edit ROM metadata                               |   -    |   ✓    |   ✓   |
| `platforms.write`   | Edit/create platforms                           |   -    |   ✓    |   ✓   |
| `firmware.read`     | List firmware                                   |   -    |   ✓    |   ✓   |
| `firmware.write`    | Upload/delete firmware                          |   -    |   ✓    |   ✓   |
| `devices.read`      | View own paired devices                         |   ✓    |   ✓    |   ✓   |
| `devices.write`     | Manage own paired devices                       |   ✓    |   ✓    |   ✓   |
| `users.read`        | List all users                                  |   -    |   -    |   ✓   |
| `users.write`       | Create/edit/delete users                        |   -    |   -    |   ✓   |
| `tasks.run`         | Trigger background tasks (scan, cleanup, etc.)  |   -    |   -    |   ✓   |

## Creating users

### Admin adds directly

**Administration → Users → Add.** Set username, email, password, and role, and the account is usable immediately.

### Invite link

Better when you don't want to handle someone else's password.

1. **Administration → Users → Invite.** Pick a role, and RomM generates a single-use invite link.
2. Send the link and the recipient opens it, picks their own username and password, and is logged in.
3. Invite links expire after 600 seconds by default, configurable via [`INVITE_TOKEN_EXPIRY_SECONDS`](../reference/environment-variables.md).

### OIDC

If you've wired up OIDC, new identities can be provisioned on first login. Role mapping from OIDC claims is covered in [OIDC Setup](oidc/index.md).

## Editing and deleting users

- **Change role**: Admin → Users → Edit → Role dropdown, taking effect on next login.
- **Reset password**: Admin → Users → Edit → New password.
- **Delete**: Admin → Users → Delete → Confirm. Note that you can't delete the last admin or delete yourself while signed in.

Deleting a user keeps their contributions (collections they made public, ROM metadata edits) but removes their personal data from the database (per-ROM ratings, saves, states, play sessions, paired devices, API tokens) but does not delete any files from disk.

## API tokens (advanced)

Each user can issue up to 25 **Client API Tokens** from **Administration → Client API Tokens**. Tokens carry a subset of the user's scopes and are the right way to authenticate companion apps (Argosy, Grout, Playnite, custom scripts). The pairing flow for devices is covered in [Client API Tokens](../developers/client-api-tokens.md), and the API side is in [API Authentication](../developers/api-authentication.md).
