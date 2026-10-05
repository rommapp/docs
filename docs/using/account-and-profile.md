---
title: Account & Profile
description: Manage your user account
---

# Account & Profile

Every user (User or Admin) can manage their own profile, and Admins can also edit _other_ users' profiles (see [Users & Roles](../administration/users-and-roles.md) for the admin side).

## Preferred username in OIDC

If you're an OIDC user and want to show your `preferred_username` from the token instead of your email local-part, the server owner can set `OIDC_USERNAME_ATTRIBUTE=preferred_username` (see [OIDC Setup](../administration/oidc/index.md)).

## Forgotten password

The sign-in page can send you a password reset link, valid for 10 minutes. If the server has [email](../administration/email.md) set up and your account has an email address, the link arrives by email. Otherwise it goes to the server log, so ask an admin for it, or to set a new password for you. A new password must be 6 to 255 ASCII characters.

## Notifications

Scans, tasks, role changes and other events leave a notification in your inbox. You can forward them to a webhook, an email address or (for admins) chat services like Discord and Telegram (see [Notifications](notifications.md)).

## Client API tokens

These are long-lived API tokens for companion apps, scripts, and integrations. Each token is scoped to a subset of your user's scopes, and optionally expires.

For handheld apps where typing a 68-character token isn't realistic, the server exposes a pairing flow: it issues a short numeric code (8 digits, valid for 5 minutes) that the device exchanges for the full token via the pairing API (see [Client API Tokens](../developers/client-api-tokens.md) for the full flow).

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
- **Can't create API token**: you've hit the 25-token cap, so revoke older or unused ones.
