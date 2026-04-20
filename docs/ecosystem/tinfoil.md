---
title: Tinfoil
description: Install Nintendo Switch games from your RomM library over Wi-Fi via Tinfoil's feed mechanism.
---

<!-- trunk-ignore-all(markdownlint/MD033) -->

# Tinfoil

<div align="center">
    <img src="../../resources/romm/integrations/tinfoil.svg" height="200px" width="200px" alt="RomM Tinfoil logo">
</div>

[Tinfoil](https://tinfoil.io) is Nintendo Switch homebrew for installing software from custom feed URLs. Point it at RomM's Tinfoil feed endpoint, and your Switch library becomes installable from the Switch itself over Wi-Fi.

## Prerequisites

- **RomM 3.5.0 or newer.** Tinfoil feeds landed in that release. Much better in 5.0
- **`DISABLE_DOWNLOAD_ENDPOINT_AUTH=true`** on your RomM instance. Tinfoil can't send a bearer token, so the downloads endpoint has to be openable. **Only enable this when RomM isn't directly exposed to the public internet.** See [Authentication → Download-endpoint auth bypass](../administration/authentication.md#download-endpoint-auth-bypass).
- **Tinfoil installed on the Switch.** Setup varies, so follow Tinfoil's own docs.
- **A Switch that can reach RomM over Wi-Fi.** Same LAN is easiest. Remote reachability requires reverse proxy + cert that the Switch accepts.

## Feed URL

```text
{romm_url}/api/feeds/tinfoil
```

No authentication: the endpoint works as long as `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true`.

## Configuring Tinfoil

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

## Using it

- **New Games** tab in Tinfoil: browseable list of your Switch ROMs
- **File Browser**: pick a file to install directly.

Tinfoil handles the install flow like any homebrew: downloads the `.nsp` / `.xci`, installs to eMMC or SD, cleans up.

## Filename requirements: TitleIDs

Tinfoil needs **Switch title IDs** in the filenames to parse and categorise games. The format:

```text
Super Mario Odyssey [0100000000010000][v0].nsp
```

The bracketed `[0100000000010000]` is the title ID. Without it, Tinfoil shows the file but doesn't parse it into the New Games tab or match against Switch metadata.

![TitleID example](../resources/tinfoil/titleid.jpg)

<!-- prettier-ignore -->
!!! info "Improvement coming"
    5.0 improves RomM's title-ID handling: it auto-detects title IDs from filenames that have them and feeds Tinfoil regardless of whether your filename format is standard. The guidance above still applies for older RomM releases.

### Finding title IDs

- [No-Intro](https://datomatic.no-intro.org/) lists them per title.
- [tinfoildb.com](https://tinfoildb.com/) and similar databases are searchable.
- Pre-organised ROM sets ship with title IDs in filenames already.

### Renaming files

Once renamed, the next time Tinfoil opens it re-parses.

## Alternative: through a reverse proxy

If you put RomM behind a reverse proxy, the proxy can handle auth separately from RomM. For example:

- Proxy challenges for basic auth before reaching RomM.
- RomM itself has `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true`.

Tinfoil sends basic auth upstream, proxy accepts and forwards, and RomM serves.

This gets you authenticated Tinfoil feeds without making RomM itself world-readable.

## Troubleshooting

- **"can't get list: list is empty".** Either your RomM library has no `.nsp`/`.xci` files that Tinfoil recognises, or filenames lack title IDs.
- **Tinfoil connects but nothing in New Games.** Title IDs missing from filenames. Rename.
- **Tinfoil can't connect at all.** LAN reachability issue, or wrong port in the feed setup. Try `http://<ip>:<port>/api/feeds/tinfoil` in a browser. You should get JSON.
- **Downloads fail with 401.** `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true` isn't set on RomM, or you forgot to restart the container after setting it.

## See also

- [Authentication → Download-endpoint auth bypass](../administration/authentication.md#download-endpoint-auth-bypass): the `DISABLE_DOWNLOAD_ENDPOINT_AUTH` caveat
- [Feeds reference](../reference/feeds.md): full feeds catalogue
