---
title: Account & Profile
description: Manage your user account
---

# Account & Profile

Every user (Viewer, Editor, Admin) can manage their own profile, but Admins can edit _other_ users' profiles (see [Users & Roles](../administration/users-and-roles.md) for the admin side).

## Preferred username in OIDC

If you're an OIDC user and want to show your `preferred_username` from the token instead of your email local-part, the operator can set `OIDC_USERNAME_ATTRIBUTE=preferred_username` (see [OIDC Setup](../administration/oidc/index.md)).

## Client API tokens

These are long-lived API tokens for companion apps, scripts, and integrations. Each token is scoped to a subset of your user's scopes, and optionally expires.

For handheld apps where typing a 44-character token isn't realistic, a pairing flow is exposed where the server issues a short numeric code (8 digits, valid for 5 minutes) that the device exchanges for the full token via the pairing API. Full flow in [Client API Tokens](../developers/client-api-tokens.md).

## Deleting your account

Ask an admin to delete your account. When deleted:

- Your profile is removed.
- Personal ROM data (ratings, notes, play sessions) is removed.
- **Saves and states** files are retained but disassociated from your account.
- **Public collections** stay (they belong to the community) but show as orphaned.
- **Private collections** are deleted.
- **Client API Tokens** are revoked.

## Troubleshooting

- **"Current password incorrect"**: caps lock, or the password was changed by an admin.
- **Can't create API token**: you've hit the 25-token cap, revoke older/unused ones.
