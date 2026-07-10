---
title: Users & Roles
description: User management, roles, and the permission-group model
---

# Users & Roles

The first user created during Setup is always an **Admin**, and everyone after that is a regular **User** whose access is governed by the [permission group](#permission-groups) you assign.

## Roles

There are only two roles:

| Role      | Who it's for                     | Access                                                                             |
| --------- | -------------------------------- | ---------------------------------------------------------------------------------- |
| **Admin** | You, and anyone you fully trust. | Admins **bypass permission groups** entirely, including user management and tasks. |
| **User**  | Everyone else                    | Whatever their assigned permission group grants, plus any per-user overrides.      |

## Permission groups

Each User belongs to a **permission group**: a named template of capabilities that you manage in the new UI (**Administration → Permissions**). A group is a **grant matrix** over entity types and actions:

| Entity        | `read`                        | `write`                          | `delete`         |
| ------------- | ----------------------------- | -------------------------------- | ---------------- |
| `platforms`   | Browse platforms              | Edit/create platforms            | Delete platforms |
| `roms`        | Browse ROMs                   | Edit ROM metadata                | Delete ROMs      |
| `collections` | Browse collections            | Create/edit                      | Delete           |
| `firmware`    | List firmware                 | Upload firmware                  | Delete firmware  |
| `assets`      | View saves/states/screenshots | Upload/replace                   | Delete           |
| `devices`     | View paired devices           | Pair/manage devices              | Unpair devices   |
| `users`       | List users                    | Create/edit users                | Delete users     |
| `tasks`       | View task status              | Trigger tasks (scan, cleanup, …) | —                |
| `logs`        | View server logs              | —                                | —                |

Rules of the model:

- **A missing grant means denied.** A group only allows what it explicitly lists.
- **`own_only`** narrows a grant to entities the user owns. For example, `assets.write` with `own_only` lets a user manage their own saves/states/screenshots but not anyone else's.
- **Default group**: exactly one group is marked as the server-wide default and is applied automatically to every new User (invite sign-up, OIDC first login, admin-created accounts without an explicit group).

### Per-user overrides

On top of the group, you can **add or revoke individual capabilities** for one user without creating a whole new group:

- **Grant** an override to give a user something their group lacks.
- **Revoke** an override to take away something their group provides.

Use overrides for one-offs ("this one user can also delete ROMs"), and use groups for anything you'd apply to more than one person.

### Hidden entities

Beyond allow/deny, you can **hide specific platforms or ROMs** from a user or from an entire group. A hidden entity simply doesn't appear for that principal, regardless of read grants. Firmware visibility isn't hidden directly, as it cascades from the platform it belongs to.

## Creating users

Three paths:

- **Admin page**: set username, email, password, role, and a permission group. The account is usable immediately.
- **Invite link**: when you don't want to handle someone else's password. The admin generates a single-use link, and the recipient picks their own credentials. New Users land in the default permission group. Invite links expire after 600 seconds by default, configurable via [`INVITE_TOKEN_EXPIRY_SECONDS`](../reference/environment-variables.md).
- **OIDC**: if you've wired up OIDC, new identities can be provisioned on first login. Whether that happens is controlled by `OIDC_ALLOW_REGISTRATION`, and Admin mapping from OIDC claims is covered in [OIDC Setup](oidc/index.md).

## Editing and deleting users

Admins can change any user's role, move them between permission groups, add per-user overrides, reset their password, or delete the account. Role and permission changes take effect on next login. You can't delete the last admin or delete yourself while signed in.

Deleting a user keeps their contributions (collections they made public, ROM metadata edits) but removes their personal data from the database (per-ROM ratings, saves, states, play sessions, paired devices, API tokens). It does not delete any files from disk.

## OAuth scopes

The permission groups above are the source of truth for the UI. For the **API**, RomM derives a flat set of OAuth **scopes** from a user's effective grants (group + overrides). Each `(entity, action)` grant maps to the scope of the same name, e.g. `roms` + `write` → `roms.write`. Client API Tokens and OIDC sessions carry a **subset** of the owning user's scopes, and every endpoint declares which scopes it requires.

The full scope list (grouped by resource):

| Resource    | Scopes                                                         |
| ----------- | -------------------------------------------------------------- |
| Profile     | `me.read`, `me.write`                                          |
| ROMs        | `roms.read`, `roms.write`, `roms.user.read`, `roms.user.write` |
| Platforms   | `platforms.read`, `platforms.write`                            |
| Assets      | `assets.read`, `assets.write`                                  |
| Collections | `collections.read`, `collections.write`                        |
| Firmware    | `firmware.read`, `firmware.write`                              |
| Devices     | `devices.read`, `devices.write`                                |
| Users       | `users.read`, `users.write`                                    |
| Tasks       | `tasks.run`                                                    |
| Logs        | `logs.read`                                                    |

## API tokens (advanced)

Each user can issue up to 25 **Client API Tokens**. A token carries a subset of the owning user's scopes (see above), whichever you pick at creation time. Tokens are the right way to authenticate companion apps (Argosy, Grout, Playnite, custom scripts). The pairing flow for devices is covered in [Client API Tokens](../developers/client-api-tokens.md), and the API side is in [API Authentication](../developers/api-authentication.md).
