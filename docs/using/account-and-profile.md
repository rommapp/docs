---
title: Account & Profile
description: Manage your user account
---

# Account & Profile

Every user (Viewer, Editor, Admin) can manage their own profile. Admins can edit _other_ users' profiles (see [Users & Roles](../administration/users-and-roles.md) for the admin side).

## Preferred username in OIDC

If you're an OIDC user and want to show your `preferred_username` from the token instead of your email local-part, the operator can set `OIDC_USERNAME_ATTRIBUTE=preferred_username` (see [OIDC Setup](../administration/oidc/index.md)).

## Client API tokens

Long-lived API tokens for companion apps, scripts, and integrations. Each token is scoped to a subset of your user's scopes, and optionally expires. Full spec in [Client API Tokens](../developers/client-api-tokens.md).

Token format: `rmm_` + 40 hex chars, treat it like a password.

For handheld apps where typing a 44-character token isn't realistic, RomM exposes a pairing flow: the server issues a short numeric code (8 digits, valid for 5 minutes) that the device exchanges for the full token via the pairing API. Full flow in [Client API Tokens](../developers/client-api-tokens.md).

### Limits

- **25 active tokens per user**, so revoke old ones to free slots.
- **Tokens carry a subset of your scopes**, so if an admin demotes you to Viewer, any token you hold with admin scopes stops working. Tokens don't escalate privileges beyond the owning user's current role.

## Accessibility

The main UI supports screen readers (VoiceOver, NVDA, JAWS, Orca). Every interactive element has proper ARIA labels, focus states are visible, and semantic heading structure is consistent.

Other accessibility features:

- **Keyboard-only navigation**: every user-facing action reachable without a mouse.
- **Dark / light / auto theme**, with auto following OS preference.
- **Reduced motion**: `prefers-reduced-motion` is respected from your OS, so animations shorten or disable automatically.
- **19 locales**: see [Languages](languages.md).

Gaps you should know about:

- **[Console Mode](console-mode.md)** isn't currently screen-reader-friendly the way the main UI is. It's built around gamepad / spatial navigation. Stick with the main UI if you use assistive tech.
- **In-browser play**: EmulatorJS is a third-party component and its accessibility is outside our control.

Known issue? Please file on [rommapp/romm](https://github.com/rommapp/romm/issues). Accessibility fixes get prioritised.

## Personal data

Per-game data you set (ratings, notes, status, playtime) is all stored per-user. Admins can't see your per-game ratings unless you share them via a public collection.

To export your personal data (GDPR-ish use case):

```http
GET /api/users/me?include=personal
Authorization: Bearer <your-token>
```

Returns your user record plus a `personal_data` array of per-ROM ratings, notes, and play sessions. Full API details in [API Reference](../developers/api-reference.md).

## Deleting your account

Ask an admin to delete your account. When deleted:

- Your profile is removed.
- Your saves, states, screenshots, personal ROM data (ratings, notes, play sessions) are removed.
- Your **public collections** stay (they belong to the community) but show as orphaned.
- Your **private collections** are deleted.
- Your **Client API Tokens** are revoked.

## OIDC-specific notes

If you signed in via OIDC:

- Most fields are still editable on the app side. Email and role may be overwritten on next login based on IdP claims.
- **Logging out of RomM doesn't log out of the IdP** unless the operator has enabled `OIDC_RP_INITIATED_LOGOUT` (see [OIDC Setup](../administration/oidc/index.md)).
- Unlinking OIDC isn't currently supported. To convert to a local account, ask an admin to delete your OIDC-linked account, then re-register with a local email+password.

## Troubleshooting

- **"Current password incorrect"**: caps lock, or the password was changed by an admin. Ask them.
- **Can't create API token**: you've hit the 25-token cap. Revoke old ones.
- **OIDC login came back as Viewer when I'm an Admin**: role claim mapping is misconfigured or missing (see [OIDC Troubleshooting → Role mapping](../troubleshooting/authentication.md#user-is-created-but-stays-viewer-even-though-they-should-be-admin)).
