---
title: Administration Page
description: A tour of the in-app administration UI
---

# Administration Page

Click your **profile avatar** (bottom left on any page) to open the settings drawer. The links you see depend on your role. Admins see everything, and Editors and Viewers see a subset. This page is a map of what's behind each link, where the deep mechanics of each feature live on their own pages.

## The drawer

- **Profile**: Change own username, email, password, avatar, and link a RetroAchievements account to sync achievements.
- **User Interface**: Locale, theme (dark/light/auto), game card layout, home dashboard ribbons, collection display settings
- **Library Management**: Platform bindings & version mappings, missing-ROMs tool, library folder settings
- **Metadata Sources**: Credentials for the 13 metadata providers, scan priority
- **Administration**: Users, Client API Tokens, Tasks. The main admin hub
- **Client API Tokens**: Each user's personal API tokens. Admins see a separate "all tokens" view under Administration.
- **Server Stats**: Platforms, games, saves, states, screenshots, disk usage
- **About**: RomM version, links to Discord / GitHub / docs

## Role-based visibility cheat sheet

| Section                       | Viewer | Editor | Admin |
| ----------------------------- | :----: | :----: | :---: |
| Profile                       |   ✓    |   ✓    |   ✓   |
| User Interface                |   ✓    |   ✓    |   ✓   |
| Client API Tokens (own)       |   ✓    |   ✓    |   ✓   |
| About                         |   ✓    |   ✓    |   ✓   |
| Library Management            |   -    |   ✓    |   ✓   |
| Metadata Sources              |   -    |   -    |   ✓   |
| Administration → Users        |   -    |   -    |   ✓   |
| Administration → Tokens (all) |   -    |   -    |   ✓   |
| Administration → Tasks        |   -    |   -    |   ✓   |
| Server Stats                  |   -    |   -    |   ✓   |
