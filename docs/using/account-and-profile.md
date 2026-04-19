---
title: Account & Profile
description: Manage your RomM account: profile, password, avatar, API tokens, device pairing.
---

# Account & Profile

Your account controls: profile drawer → **Profile**.

Every user (Viewer, Editor, Admin) can manage their own profile. Admins can edit *other* users' profiles. See [Users & Roles](../administration/users-and-roles.md) for the admin side.

## Profile basics

### Username and email

Editable from the profile page. Changing your email:

- **OIDC users**: email is usually governed by the IdP. RomM lets you change it here but OIDC login will re-match on the IdP-supplied email at next login.
- **Local users**: change freely. The new email is used for password reset (if email transport is configured, see [Authentication](../administration/authentication.md)).

### Password

For local accounts: **Current password** + **New password** (twice). RomM uses bcrypt: no plaintext storage, no password recovery by the admin (admins reset by setting a new password, but they can't see your old one).

OIDC users don't have local passwords, because authentication is via the IdP. Password fields are hidden on the profile page.

### Avatar

Upload a PNG / JPEG / WebP, and it shows next to your name across the UI.

### Preferred username in OIDC

If you're an OIDC user and want RomM to show your `preferred_username` from the token instead of your email local-part, the operator can set `OIDC_USERNAME_ATTRIBUTE=preferred_username`. See [OIDC Setup](../administration/oidc/index.md).

## Client API tokens

Long-lived API tokens for companion apps, scripts, and integrations. Each token is scoped to a subset of your user's scopes, and optionally expires.

See the full spec in [Client API Tokens](../ecosystem/client-api-tokens.md); this section is just the "how I create one from the UI" version.

### Creating a token

1. **Profile → Client API Tokens → + New Token**.
2. Pick:
    - **Name**: descriptive (e.g. "Grout on my RG35XX").
    - **Scopes**: which permissions to include. Default is read-only, so tick write scopes deliberately.
    - **Expiry**: optional, blank = never expires.
3. **Create**.
4. The token appears **once**, so copy it immediately because you can't retrieve it later.

Token format: `rmm_` + 40 hex chars, and you should treat it like a password.

### Pairing to a device

For handheld apps like Grout, typing a 44-character token on a thumbstick isn't realistic. Instead:


1. **Profile → Client API Tokens → [token] → Pair Device**.
2. A short numeric code appears (8 digits, valid for 5 minutes).
3. On the device (Grout app, etc.): enter the code.
4. The device exchanges the code for the full token via the pairing API.
5. Done: token is on the device, you never typed it.

Full flow in [Client API Tokens](../ecosystem/client-api-tokens.md).

### Limits

- **25 active tokens per user**, so delete old ones to free slots.
- **Tokens carry a subset of your scopes**, so if an admin demotes you to Viewer, any token you hold with admin scopes stops working. Tokens don't escalate privileges beyond the owning user's current role.

### Revoking

**Profile → Client API Tokens → [token] → Revoke** takes effect immediately, and the companion app loses access on its next API call.

## Keyboard shortcuts

Available throughout the app:

| Key | Action |
| --- | --- |
| `/` | Focus the search bar. |
| `Esc` | Close dialog, drawer, or player. |
| `g h` | Go to home dashboard. |
| `g s` | Open search page. |
| `g c` | Focus the scan / admin action in the sidebar. |
| `j` / `k` | Next / previous item in a list view. |
| `Enter` | Activate focused item. |

## Accessibility

RomM's main UI supports screen readers (VoiceOver, NVDA, JAWS, Orca). Every interactive element has proper ARIA labels, focus states are visible, and semantic heading structure is consistent.

Other accessibility features:

- **Keyboard-only navigation**: every user-facing action reachable without a mouse. Tab through interactive elements, and the shortcuts above get you around quickly.
- **Dark / light / auto theme**: Profile → User Interface → Theme. Auto follows OS preference.
- **Reduced motion**: RomM respects `prefers-reduced-motion` from your OS, so animations shorten or disable automatically.
- **19 locales**: see [Languages](languages.md).

Gaps you should know about:

- **[Console Mode](console-mode.md)** (the `/console` SPA) isn't currently screen-reader-friendly the way the main UI is. It's built around gamepad / spatial navigation. Stick with the main UI if you use assistive tech.
- **In-browser play**: EmulatorJS is a third-party component and its accessibility is outside RomM's control.

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

Self-deletion isn't available in 5.0. Ask an admin to delete your account. They can do it from **Administration → Users → [your account] → Delete**.

When deleted:

- Your profile is removed.
- Your saves, states, screenshots, personal ROM data (ratings, notes, play sessions) are removed.
- Your **public collections** stay (they belong to the community), but show as orphaned.
- Your **private collections** are deleted.
- Your **Client API Tokens** are revoked.

## OIDC-specific notes

If you signed in via OIDC:

- Most fields are still editable on the RomM side. Email and role may be overwritten on next login based on IdP claims.
- **Logging out of RomM doesn't log out of the IdP** unless the operator has enabled `OIDC_RP_INITIATED_LOGOUT`. See [OIDC Setup](../administration/oidc/index.md).
- Unlinking OIDC isn't currently supported from the profile page. If you want to convert to a local account, ask an admin to delete your OIDC-linked account, then re-register with a local email+password.

## Language and UI preferences

Lives on a separate page (**Profile → User Interface**), not here. Covers:

- [Language](languages.md): 19 locales.
- Theme (Dark / Light / Auto).
- Home dashboard ribbons.
- Collection types (toggle [virtual collections](virtual-collections.md) dimensions).
- Game card layout (cover style, 3D tilt, density).
- Full-screen on launch.

See those pages for detail.

## Troubleshooting

- **"Current password incorrect"**: caps lock, or the password was changed by an admin. Ask them.
- **Avatar upload silently fails**: file is too large. RomM accepts up to a few MB. Resize.
- **Can't create API token**: you've hit the 25-token cap. Revoke old ones.
- **OIDC login came back as Viewer when I'm an Admin**: role claim mapping is misconfigured or missing. See [OIDC Troubleshooting → Role mapping](../troubleshooting/authentication.md#user-is-created-but-stays-viewer-even-though-they-should-be-admin).
