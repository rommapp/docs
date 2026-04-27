---
title: Feed Clients
description: Set up Tinfoil, pkgj, fpkgi, Kekatsu, and WebRcade against RomM's URL feeds.
---

<!-- trunk-ignore-all(markdownlint/MD033) -->

# Feed Clients

RomM exposes URL feeds for several homebrew installers and frontends. Point the client at a feed URL and it browses (and installs from) your library over Wi-Fi. This page collects setup for each supported client. The wire-level reference is [Feeds](../reference/feeds.md).

| Client                | Target hardware                  | File format     |
| --------------------- | -------------------------------- | --------------- |
| [Tinfoil](#tinfoil)   | Nintendo Switch (homebrew)       | `.nsp` / `.xci` |
| [pkgj](#pkgj)         | PS Vita / PSP                    | `.pkg`          |
| [fpkgi](#fpkgi)       | PS4 / PS5 (CFW)                  | `.pkg`          |
| [Kekatsu](#kekatsu)   | Nintendo DS                      | `.nds`          |
| [WebRcade](#webrcade) | Any modern browser               | varies          |

## Authentication, applies to every feed

All RomM feeds honour the same auth model. Two options:

- **Default (recommended).** `DISABLE_DOWNLOAD_ENDPOINT_AUTH=false`. Feeds require basic auth, and most clients (Tinfoil, pkgj, fpkgi) can send basic-auth credentials in their feed-URL config.
- **Open downloads.** `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true` makes the download endpoints public. **Only enable this when RomM isn't directly exposed to the public internet** (LAN-only, behind a VPN, or behind a reverse proxy that handles auth upstream of RomM).

See [Authentication → Download-endpoint auth bypass](../administration/authentication.md#download-endpoint-auth-bypass) for the full security discussion.

## Tinfoil

<div align="center">
    <img src="../../resources/romm/integrations/tinfoil.svg" height="200px" width="200px" alt="RomM Tinfoil logo">
</div>

[Tinfoil](https://tinfoil.io) is Nintendo Switch homebrew for installing software from custom feed URLs. Point it at RomM's Tinfoil feed endpoint, and your Switch library becomes installable from the Switch itself over Wi-Fi.

### Prerequisites

- **RomM 3.5.0 or newer.** Tinfoil feeds landed in that release. Much better in 5.0
- **`DISABLE_DOWNLOAD_ENDPOINT_AUTH=true`** on your RomM instance. Tinfoil can't send a bearer token, so the downloads endpoint has to be openable. Re-read the [Authentication](#authentication-applies-to-every-feed) caveat above before enabling this.
- **Tinfoil installed on the Switch.** Setup varies, so follow Tinfoil's own docs.
- **A Switch that can reach RomM over Wi-Fi.** Same LAN is easiest. Remote reachability requires reverse proxy + cert that the Switch accepts.

### Feed URL

```text
{romm_url}/api/feeds/tinfoil
```

No authentication: the endpoint works as long as `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true`.

### Configuring Tinfoil

1. Launch Tinfoil on the Switch → **File Browser**.
2. Scroll to the file-server list → press `-` (minus) to add a new one.
3. Enter:
    - **Protocol:** `http` or `https` (depending on your RomM reverse-proxy setup)
    - **Host:** RomM's hostname or IP
    - **Port:** RomM's port (usually 80 or 443)
    - **Path:** `/api/feeds/tinfoil`
    - **Username:** your RomM username (optional, Tinfoil can send basic auth, and RomM tries it)
    - **Password:** your RomM password
    - **Title:** anything (e.g. `RomM Switch`)
    - **Enabled:** yes
4. Press `X` to save.
5. Close and reopen Tinfoil. The library is parsed.

On reopen, you should see a custom message of the day: `RomM Switch Library`. If you do, it's working.

![Tinfoil after setup](../resources/tinfoil/tinfoilscreen.jpg)

### Using it

- **New Games** tab in Tinfoil: browseable list of your Switch ROMs
- **File Browser**: pick a file to install directly.

Tinfoil handles the install flow like any homebrew: downloads the `.nsp` / `.xci`, installs to eMMC or SD, cleans up.

### Filename requirements: TitleIDs

Tinfoil needs **Switch title IDs** in the filenames to parse and categorise games. The format:

```text
Super Mario Odyssey [0100000000010000][v0].nsp
```

The bracketed `[0100000000010000]` is the title ID. Without it, Tinfoil shows the file but doesn't parse it into the New Games tab or match against Switch metadata.

![TitleID example](../resources/tinfoil/titleid.jpg)

<!-- prettier-ignore -->
!!! info "Improvement coming"
    5.0 improves RomM's title-ID handling: it auto-detects title IDs from filenames that have them and feeds Tinfoil regardless of whether your filename format is standard. The guidance above still applies for older RomM releases.

#### Finding title IDs

- [No-Intro](https://datomatic.no-intro.org/) lists them per title.
- [tinfoildb.com](https://tinfoildb.com/) and similar databases are searchable.
- Pre-organised ROM sets ship with title IDs in filenames already.

#### Renaming files

Once renamed, the next time Tinfoil opens it re-parses.

### Alternative: through a reverse proxy

If you put RomM behind a reverse proxy, the proxy can handle auth separately from RomM. For example:

- Proxy challenges for basic auth before reaching RomM.
- RomM itself has `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true`.

Tinfoil sends basic auth upstream, proxy accepts and forwards, and RomM serves.

This gets you authenticated Tinfoil feeds without making RomM itself world-readable.

### Troubleshooting

- **"can't get list: list is empty".** Either your RomM library has no `.nsp`/`.xci` files that Tinfoil recognises, or filenames lack title IDs.
- **Tinfoil connects but nothing in New Games.** Title IDs missing from filenames. Rename.
- **Tinfoil can't connect at all.** LAN reachability issue, or wrong port in the feed setup. Try `http://<ip>:<port>/api/feeds/tinfoil` in a browser. You should get JSON.
- **Downloads fail with 401.** `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true` isn't set on RomM, or you forgot to restart the container after setting it.

## pkgj

[pkgj](https://github.com/blastrock/pkgj) is PS Vita homebrew for installing `.pkg`-format games and DLC. Default config points at well-known community URLs but you can point it at RomM's feed endpoints instead and install from your library over Wi-Fi.

### Prerequisites

- **PS Vita** with [pkgj](https://github.com/blastrock/pkgj) installed
- A way to edit files on the Vita: [VitaShell](https://github.com/TheOfficialFloW/VitaShell) works well.
- **RomM reachable from the Vita**: same LAN ideal, and HTTP or HTTPS both work.
- Your games stored as `.pkg` files (pkgj requires this format, and it won't work with `.iso` or other formats)

### Feed URLs

RomM exposes four pkgi-compatible feeds:

| Content       | URL                                     |
| ------------- | --------------------------------------- |
| PS Vita games | `{romm_url}/api/feeds/pkgi/psvita/game` |
| PS Vita DLCs  | `{romm_url}/api/feeds/pkgi/psvita/dlc`  |
| PSP games     | `{romm_url}/api/feeds/pkgi/psp/game`    |
| PSP DLCs      | `{romm_url}/api/feeds/pkgi/psp/dlc`     |

### Configuring pkgj

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

### Using pkgj

Once configured, pkgj shows your RomM PS Vita / PSP library. Select a title → install. pkgj downloads the `.pkg` from RomM and installs it to the Vita.

### File format requirements

**RomM only lists `.pkg` files in pkgi feeds.** If your Vita or PSP games are in `.iso`, `.chd`, or other formats, they won't appear in pkgj.

Why: pkgj is designed around the Sony installer format. Other formats aren't installable via the same mechanism.

If you have non-`.pkg` files you want on the Vita, you'll need to convert them or use a different workflow (FTP through VitaShell, for example).

### Authentication notes

The pkgi feeds honour basic auth. Unlike Tinfoil, pkgj sends basic auth headers natively, so you don't have to turn off download auth on RomM to use it. Some users prefer disabling auth for a smoother first-time flow. Either path works.

### Troubleshooting

- **"can't get list: list is empty".** You don't have any `.pkg` content for the feeds you configured. Check your library actually contains `.pkg` files on the corresponding platforms.
- **Refresh returns an error.** URL in `config.txt` is wrong. Verify the feed URL in a browser first (returns JSON).
- **Download fails partway.** LAN connectivity or disk space on Vita. pkgj reports both.
- **Game installs but won't boot.** The `.pkg` is for a different firmware / region. Not a RomM issue

## fpkgi

[fpkgi](https://github.com/CyberYoshi64/fpkgi) is PS4 / PS5 homebrew for installing `.pkg` packages from custom URL feeds. RomM exposes fpkgi-compatible feeds for its PS4 and PS5 libraries.

New in RomM 5.0. Earlier versions didn't have fpkgi feeds.

### Prerequisites

- **PS4 or PS5** with fpkgi installed (requires CFW / jailbreak, and setup is out of scope here)
- **RomM reachable from the console over Wi-Fi.** LAN simplest
- Games stored as `.pkg` files. fpkgi, like pkgj, only handles the Sony installer format.

### Feed URL

```text
{romm_url}/api/feeds/fpkgi/{platform_slug}
```

Where `{platform_slug}` is:

- `ps4` for PlayStation 4 content
- `ps5` for PlayStation 5 content

Example:

```text
http://192.168.1.100:3000/api/feeds/fpkgi/ps4
```

The feed returns JSON in the fpkgi-expected schema: titles, title IDs, content types, URLs back to RomM for the actual downloads.

### Configuring fpkgi

Exact steps depend on the fpkgi version but the gist:

1. Put RomM's feed URL in fpkgi's config (usually a JSON file on the console, so check fpkgi's own docs).
2. Restart fpkgi.
3. The RomM library appears in fpkgi's browse view.

Consult [fpkgi's README](https://github.com/CyberYoshi64/fpkgi) for the current config-file location and format. The project moves faster than these docs.

### Authentication notes

The `/api/feeds/fpkgi/` endpoints support basic auth the same way `/api/feeds/pkgi/` does. Either set basic-auth credentials in fpkgi's config (if it supports them) or use `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true` on the RomM server.

### File format: must be `.pkg`

PS4 `.pkg` files specifically, not `.iso`, not compressed. RomM filters to `.pkg` when building the feed. Any other file types are invisible to fpkgi.

### Troubleshooting

- **Feed is empty.** No `.pkg` files on the `ps4` / `ps5` platform. Check your library.
- **Downloads fail with 401.** Auth config mismatch, see [Authentication](#authentication-applies-to-every-feed) above.
- **Downloads succeed but install fails.** `.pkg` is for a different firmware version. Not a RomM problem

## Kekatsu

**Kekatsu** is Nintendo DS homebrew for loading games from a custom URL feed. RomM exposes a Kekatsu-compatible feed for its DS library.

New in RomM 5.0.

### Prerequisites

- A Nintendo DS with Kekatsu installed (requires a flashcart or homebrew launcher)
- **RomM reachable from the DS over Wi-Fi.** The DS's Wi-Fi is WEP / old WPA only, so this typically means a dedicated legacy-SSID on your router or a travel router bridging the DS to your modern network.
- DS games in `.nds` format

### Feed URL

```text
{romm_url}/api/feeds/kekatsu/{platform_slug}
```

For standard DS content, the platform slug is `nds`:

```text
http://192.168.1.100:3000/api/feeds/kekatsu/nds
```

### Configuring Kekatsu

Exact config steps depend on your Kekatsu build but the shared concept is "point the app at this URL and it fetches the manifest". Consult Kekatsu's own docs for the current config-file location.

### File format

`.nds` only. DSi Ware / iQue / other formats aren't listed in the feed.

### Authentication notes

Kekatsu can send basic auth. Either configure it on the DS side or use `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true` on RomM.

### Why the legacy-Wi-Fi hassle

The DS's original Wi-Fi hardware supports WEP and an older WPA variant only. Modern home routers usually don't. Workarounds:

- **Dedicated DS-friendly SSID.** Many routers allow per-SSID security, so add a WEP one just for the DS.
- **Travel router in bridge mode.** A cheap travel router configured for WEP uplinks to your main (secure) network
- **Use a DSi, 3DS, or homebrew replacement driver.** These support modern security.

If none of this is appealing, Kekatsu-over-LAN isn't going to work. Fall back to sideloading via flashcart or similar.

### Troubleshooting

- **Feed is empty.** No `.nds` files on the `nds` platform
- **DS can't see the network.** See the legacy-Wi-Fi section above.
- **Downloads fail.** Either network timeout (LAN latency over WEP is rough) or disk space. Retry one game at a time.

## WebRcade

[WebRcade](https://www.webrcade.com/) is a browser-based retro console frontend. It plays games in-browser, similar to RomM's built-in EmulatorJS player. The difference is UX: WebRcade has its own aesthetic, a curated preset-app model, and feed-based import.

If you prefer WebRcade's look-and-feel but want to point it at your RomM library, use the feed endpoint below.

### Feed URL

```text
{romm_url}/api/feeds/webrcade
```

WebRcade-compatible JSON listing every ROM in your library with metadata and direct download URLs back to RomM.

### Setting up WebRcade

1. Open [WebRcade.com](https://www.webrcade.com/) in a browser.
2. Create an account (or use it unauthenticated, with limited features).
3. Go to **My WebRcade → Add Feed**.
4. Enter RomM's feed URL: `{romm_url}/api/feeds/webrcade`.
5. Save. Your RomM library appears as WebRcade apps.

### Authentication notes

The `/api/feeds/webrcade` endpoint sends basic auth if WebRcade provides credentials. Either configure basic auth on WebRcade's feed-add screen (if it offers that) or use `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true` on RomM.

### RomM vs WebRcade

Why would you use WebRcade over RomM's built-in player?

- **Preset/curated lists.** WebRcade maintains a catalogue of vetted content that's searchable inside the app.
- **Different UI.** More console-like, less library-like
- **Per-game launch from WebRcade feeds.** You can mix-and-match RomM content with WebRcade's own catalogue in one frontend.

When to stay with RomM's player:

- **You want library management.** WebRcade is frontend-only but RomM owns the metadata and scanning.
- **You want user accounts + collections + per-user progress.** WebRcade is single-user-ish.
- **You want [Netplay](../using/netplay.md).** RomM has it but WebRcade doesn't.

Totally reasonable to run both: WebRcade as a launcher UI pointed at RomM for the library.

### Troubleshooting

- **Feed shows no games.** WebRcade filters by its own supported-platform set. Games on unsupported platforms won't show.
- **Games don't launch.** The ROM format isn't supported by WebRcade's emulator cores (which differ from EmulatorJS's). Check WebRcade's supported list.
- **Download fails.** Same auth / URL issues as other feeds. Check `{romm_url}/api/feeds/webrcade` returns JSON in a browser.

## See also

- [Feeds reference](../reference/feeds.md): wire-level catalogue of every endpoint
- [Authentication → Download-endpoint auth bypass](../administration/authentication.md#download-endpoint-auth-bypass): the `DISABLE_DOWNLOAD_ENDPOINT_AUTH` caveat
- [In-Browser Play](../using/in-browser-play.md): RomM's built-in player (alternative to WebRcade)
