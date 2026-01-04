<!-- trunk-ignore-all(markdownlint/MD033) -->
<!-- trunk-ignore-all(markdownlint/MD041) -->

<a href="https://github.com/blastrock/pkgj">pkgj</a> is a homebrew application for the PS Vita, primarily used for installing PS Vita and PSP Games. While its default configuration talks to a set of pre-defined URLs, you can configure it to talk to custom feeds.

This will help you install PSP or PS Vita games from your RomM library over Wi-Fi

## Setup

### Prepare

Please note down the following in order to make this as smooth as possible, as well as some pre-reqs:

- Your PS Vita should already have the following installed:
    - <a href="https://github.com/blastrock/pkgj">pkgj</a>
    - A method to access files to edit on your Vita, such as <a href="https://github.com/TheOfficialFloW/VitaShell">VitaShell</a>
- The URL you use to access RomM
    - This can either be `http` or `https`
- Feed URLs:
    - `/api/feeds/pkgi/psp/game`
    - `/api/feeds/pkgi/psp/dlc`
    - `/api/feeds/pkgi/psvita/game`
    - `/api/feeds/pkgi/psvita/dlc`

### Configure

1. Connect your PS Vita to your PC over USB using VitaShell
2. Open `/pkgj/config.txt` in a text editor to add the feed URLs
3. If you have PS Vita games in `.pkg` format, add a `url_games {romm_url}/api/feeds/pkgi/psvita/game` to the end of the file
4. If you have PS Vita DLCs in `.pkg` format, add a `url_dlcs {romm_url}/api/feeds/pkgi/psvita/dlc` to the end of the file
5. If you have PSP games in `.pkg` format, add a `url_psp_games  {romm_url}/api/feeds/pkgi/psp/game` to the end of the file
6. If you have PSP DLCs in `.pkg` format, add a `url_psp_dlcs  {romm_url}/api/feeds/pkgi/psp/dlc` to the end of the file
7. Save the file and disconnect from VitaShell
8. Open pkgj, Press `△` to open the menu and select "Refresh"

### Additional

If, during a Refresh, pkgj presents an error saying "can't get list: list is empty...", check whether you have any Games/DLCs for the feeds you've added in `.pkg` format. RomM won't list any Games in other formats such as `.iso`.
