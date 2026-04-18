---
title: WebRcade
description: Load your RomM library into WebRcade, an alternative browser-based retro frontend.
---

# WebRcade

[WebRcade](https://www.webrcade.com/) is a browser-based retro console frontend. It plays games in-browser, similar to RomM's built-in EmulatorJS player. The difference is UX: WebRcade has its own aesthetic, a curated preset-app model, and feed-based import.

If you prefer WebRcade's look-and-feel but want to point it at your RomM library, use the feed endpoint below.

## Feed URL

```text
{romm_url}/api/feeds/webrcade
```

WebRcade-compatible JSON listing every ROM in your library with metadata and direct download URLs back to RomM.

## Setting up WebRcade

1. Open [WebRcade.com](https://www.webrcade.com/) in a browser.
2. Create an account (or use it unauthenticated, with limited features).
3. Go to **My WebRcade → Add Feed**.
4. Enter RomM's feed URL: `{romm_url}/api/feeds/webrcade`.
5. Save. Your RomM library appears as WebRcade apps.

## Authentication

The `/api/feeds/webrcade` endpoint sends basic auth if WebRcade provides credentials. Either:

- Configure basic auth on WebRcade's feed-add screen (if it offers that), OR
- Set `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true` on RomM.

The same security caveats apply. See [Tinfoil prerequisites](tinfoil.md#prerequisites) for context on turning off download auth.

## RomM vs WebRcade

Why would you use WebRcade over RomM's built-in player?

- **Preset/curated lists.** WebRcade maintains a catalogue of vetted content that's searchable inside the app.
- **Different UI.** More console-like, less library-like.
- **Per-game launch from WebRcade feeds.** You can mix-and-match RomM content with WebRcade's own catalogue in one frontend.

When to stay with RomM's player:

- **You want library management.** WebRcade is frontend-only, but RomM owns the metadata and scanning.
- **You want user accounts + collections + per-user progress.** WebRcade is single-user-ish.
- **You want [Netplay](../using/netplay.md).** RomM has it, but WebRcade doesn't.

Totally reasonable to run both: WebRcade as a launcher UI pointed at RomM for the library.

## Troubleshooting

- **Feed shows no games.** WebRcade filters by its own supported-platform set. Games on unsupported platforms won't show.
- **Games don't launch.** The ROM format isn't supported by WebRcade's emulator cores (which differ from EmulatorJS's). Check WebRcade's supported list.
- **Download fails.** Same auth / URL issues as other feeds. Check `{romm_url}/api/feeds/webrcade` returns JSON in a browser.

## See also

- [Feeds reference](../reference/feeds.md): all feed endpoints.
- [In-Browser Play](../using/in-browser-play.md): RomM's built-in player.
- [WebRcade](https://www.webrcade.com/): upstream frontend.
