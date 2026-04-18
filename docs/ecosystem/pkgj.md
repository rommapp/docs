---
title: pkgj
description: Install PS Vita and PSP games from your RomM library via pkgj homebrew.
---

# pkgj

[pkgj](https://github.com/blastrock/pkgj) is PS Vita homebrew for installing `.pkg`-format games and DLC. Default config points at well-known community URLs; point it at RomM's feed endpoints instead and you can install from your library over Wi-Fi.

## Prerequisites

- **PS Vita** with [pkgj](https://github.com/blastrock/pkgj) installed.
- A way to edit files on the Vita — [VitaShell](https://github.com/TheOfficialFloW/VitaShell) works well.
- **RomM reachable from the Vita** — same LAN ideal; HTTP or HTTPS both work.
- Your games stored as `.pkg` files (pkgj requires this format — it won't work with `.iso` or other formats).

## Feed URLs

RomM exposes four pkgi-compatible feeds:

| Content | URL |
| --- | --- |
| PS Vita games | `{romm_url}/api/feeds/pkgi/psvita/game` |
| PS Vita DLCs | `{romm_url}/api/feeds/pkgi/psvita/dlc` |
| PSP games | `{romm_url}/api/feeds/pkgi/psp/game` |
| PSP DLCs | `{romm_url}/api/feeds/pkgi/psp/dlc` |

## Configuring pkgj

1. Connect the Vita to your PC over USB with VitaShell running.
2. Open `/pkgj/config.txt` on the Vita in a text editor.
3. Append lines for each feed you have content for:

    ```ini
    url_games       {romm_url}/api/feeds/pkgi/psvita/game
    url_dlcs        {romm_url}/api/feeds/pkgi/psvita/dlc
    url_psp_games   {romm_url}/api/feeds/pkgi/psp/game
    url_psp_dlcs    {romm_url}/api/feeds/pkgi/psp/dlc
    ```

    Replace `{romm_url}` with your actual RomM URL (e.g. `http://192.168.1.100:3000`).

4. Save and disconnect from VitaShell.
5. On the Vita: open pkgj → press `△` to open the menu → **Refresh**.

## Using pkgj

Once configured, pkgj shows your RomM PS Vita / PSP library. Select a title → install. pkgj downloads the `.pkg` from RomM and installs it to the Vita.

## File format requirements

**RomM only lists `.pkg` files in pkgi feeds.** If your Vita or PSP games are in `.iso`, `.chd`, or other formats, they won't appear in pkgj.

Why: pkgj is designed around the Sony installer format. Other formats aren't installable via the same mechanism.

If you have non-`.pkg` files you want on the Vita, you'll need to convert them or use a different workflow (FTP through VitaShell, for example).

## Authentication

The pkgi feeds honour basic auth. If your RomM doesn't have `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true`, pkgj sends basic auth headers.

Unlike [Tinfoil](tinfoil.md), pkgj handles auth natively — you don't have to turn off download auth on RomM to use it. Still, some users prefer disabling auth for a smoother first-time flow; either path works.

## Troubleshooting

- **"can't get list: list is empty"** — you don't have any `.pkg` content for the feeds you configured. Check your library actually contains `.pkg` files on the corresponding platforms.
- **Refresh returns an error** — URL in `config.txt` is wrong. Verify the feed URL in a browser first (returns JSON).
- **Download fails partway** — LAN connectivity or disk space on Vita. pkgj reports both.
- **Game installs but won't boot** — the `.pkg` is for a different firmware / region. Not a RomM issue.

## See also

- [Feeds reference](../reference/feeds.md) — full feeds catalogue.
- [Tinfoil](tinfoil.md) — Switch equivalent.
- [fpkgi](fpkgi.md) — PS4 / PS5 equivalent.
- [pkgj](https://github.com/blastrock/pkgj) — upstream homebrew.
