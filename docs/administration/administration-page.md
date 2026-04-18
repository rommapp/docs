---
title: Administration Page
description: A tour of the in-app Administration UI, where every operator control lives.
---

# Administration Page

Click your **profile avatar** (top right, any page) to open the settings drawer. The links you see depend on your role. Admins see everything; Editors and Viewers see a subset.

This page is a map of what's behind each link. The deep mechanics of each feature live on their own pages; this is where to click.

## The drawer

| Link | Who sees it | What's there |
| --- | --- | --- |
| **Profile** | Everyone | Change own username, email, password, avatar. Link a RetroAchievements account and sync achievements. |
| **User Interface** | Everyone | Locale, theme (dark/light/auto), game card layout, home dashboard ribbons, collection display settings. |
| **Library Management** | Editors + Admins | Platform bindings & version mappings, missing-ROMs tool, library folder settings. |
| **Metadata Sources** | Admins | Credentials for the 13 metadata providers; scan priority. |
| **Administration** | Admins | Users, Client API Tokens, Tasks. The main admin hub. |
| **Client API Tokens** | Everyone (own tokens) | Each user's personal API tokens. Admins see a separate "all tokens" view under Administration. |
| **Server Stats** | Admins | Numbers: platforms, games, saves, states, screenshots, disk usage. |
| **About** | Everyone | RomM version, links to Discord / GitHub / docs. |

## Profile

The thing every user touches.

- **Username / email / password**: self-serve changes. Password changes require the current password.
- **Avatar**: upload a small image; displayed next to your name everywhere.
- **RetroAchievements**: set your RA username to link accounts; "Sync now" pulls fresh progression data.

See [Users & Roles](users-and-roles.md) for what role-specific self-serve is allowed.

## User Interface

Per-user UI preferences. Stored in the user's row + localStorage, not in `config.yml`.

- **Language**: 19 locales supported; see [Languages](../using/languages.md) for the list.
- **Theme**: Dark, Light, or Auto (follows OS preference). Palette overrides via `extra_css` are operator-level.
- **Game card layout**: cover style (2D, 3D boxart, poster), info-density, the `vanilla-tilt` 3D hover effect on/off.
- **Home dashboard ribbons**: show/hide "Recently Added", "Continue Playing", "Collections", etc.
- **Virtual collections**: enable/disable auto-generated groupings (by genre, developer, year, etc.).

## Library Management

Editor-grade tools for catalogue hygiene.

- **Platform bindings**: map a filesystem folder name (`super_nintendo/`) to a platform slug (`snes`). Mirrors `system.platforms` in `config.yml`.
- **Platform versions**: some platforms have multiple IGDB "versions" (e.g. Mega Drive vs Genesis). Pin which one RomM uses for lookups.
- **Missing ROMs**: a filter/table view showing DB entries whose files are gone. Bulk-delete from here, or run the [Cleanup Missing ROMs](scheduled-tasks.md#cleanup-missing-roms-manual) task.

## Metadata Sources

Admin-only. Per-provider credentials, test buttons, and the priority-ordering drag-and-drop UI. Equivalent to editing the `*_CLIENT_ID` / `*_API_KEY` env vars and `scan.priority` in `config.yml`, but interactive.

Full provider details in [Metadata Providers](metadata-providers.md).

## Administration

The main admin hub. Three sub-panels:

### Users

- Table of all users with role, last login, creation date.
- **Add**: manual user creation with username + email + password + role.
- **Invite**: generate an invite link. See [Invitations & Registration](invitations-and-registration.md).
- **Edit**: change username, email, role, password. Reset password by typing a new one.
- **Delete**: red trash icon. RomM won't let you delete yourself or the last admin.

### Client API Tokens

- Table of every token on the server (admin view; users see only their own via their Profile).
- Filter by user. Revoke any token.
- See [Authentication → Client API Tokens](authentication.md#client-api-tokens) for the create-your-own flow.

### Tasks

- Status of every scheduled / manual / watcher task: queued, running, idle, failed.
- **Run** button per task (requires `tasks.run` scope).
- See [Scheduled Tasks](scheduled-tasks.md) for what each one does.

## Server Stats

Admin-only. A dashboard of counts and sizes:

- Total platforms, games, saves, states, screenshots.
- Total disk footprint (library + resources + assets).
- Per-platform breakdown: handy for spotting a platform that's ballooned.

Full details in [Server Stats](server-stats.md).

## Keyboard shortcuts

A few useful ones wherever the drawer is open:

| Key | Action |
| --- | --- |
| `Esc` | Close the drawer. |
| `g h` | Go home. |
| `g s` | Open the Search page. |
| `g c` | Focus the Scan button in the sidebar. |

Full shortcut reference is on the [Using RomM](../using/index.md) page.

## Role-based visibility cheat sheet

| Section | Viewer | Editor | Admin |
| --- | :---: | :---: | :---: |
| Profile | ✓ | ✓ | ✓ |
| User Interface | ✓ | ✓ | ✓ |
| Client API Tokens (own) | ✓ | ✓ | ✓ |
| About | ✓ | ✓ | ✓ |
| Library Management | - | ✓ | ✓ |
| Metadata Sources | - | - | ✓ |
| Administration → Users | - | - | ✓ |
| Administration → Tokens (all) | - | - | ✓ |
| Administration → Tasks | - | - | ✓ |
| Server Stats | - | - | ✓ |
