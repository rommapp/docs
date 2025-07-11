RomM supports multiple metadata providers to enrich your game library with titles, descriptions, cover art, and achievements. You don't need all providers, so this guide covers provider[combos](#combos) and [setup](#setup).

## Combos

Here are some common combinations you can use based on your needs:

### The Chef's Choice: [Hasheous](#hasheous) + [ScreenScraper](#screenscraper) + [Retroachievements](#retroachievements)
- Supports 135+ most popular systems
- Hasheous provides hash-based matching and proxies IGDB data (titles, descriptions and cover art)
- ScreenScraper adds additional artwork and manuals
- Retroachievements provides achievement progress
- **This is the recommended setup for most users**

### The Twitch Fan: [IGDB](#igdb) + [PlayMatch](#playmatch)
- Supports 200+ systems available on IGDB
- Provides titles, descriptions, cover art and related games from IGDB
- PlayMatch adds hash-based matching for unmatched files
- **Use this if you want a single-provider solution**

### The Quick Starter: [Hasheous](#hasheous)
- Hash-based matching exclusively
- Proxies titles, descriptions and cover art from IGDB
- **For users who want to avoid API keys**

### The Privacy Freak: [LaunchBox](#launchbox)
- Makes no API calls to cloud services
- LaunchBox provides titles, descriptions, and cover art
- Exact filename matching exclusively
- **Ideal for LaunchBox users with correct filenames**

## Setup

### IGDB

To access the IGDB API you'll need a Twitch account and a valid phone number for 2FA verification. Up-to-date instructions are available in the [IGDB API documentation](https://api-docs.igdb.com/#account-creation). When registering your application in the Twitch Developer Portal, fill out the form like so:

- Name: Something **unique or random** like `correct-horse-battery-staple` or `KVV8NDXMSRFJ2MRNPNRSL7GQT`
- OAuth Redirect URLs: `localhost`
- Category: `Application Integration`
- Client Type: `Confidential`

<!-- prettier-ignore -->
!!! important  
    The name you pick has to be unique! Picking an existing name will fail silently, with no error messages. We recommend using `romm-<random hash>`, like `romm-3fca6fd7f94dea4a05d029f654c0c44b`

Note the client ID and secret that appear on screen, and use them to set `IGDB_CLIENT_ID` and `IGDB_CLIENT_SECRET` in your environment variables.

![IGDB Creation](../resources/metadata_providers/1-igdb.png)
![IGDB Secret](../resources/metadata_providers/2-igdb.png)

### ScreenScraper

To access the ScreenScraper API, create a [ScreenScraper](https://www.screenscraper.fr/membreinscription.php) and copy the **user** and **password** you just created to `SCREENSCRAPER_USER` and `SCREENSCRAPER_PASSWORD` respectively.

### MobyGames

To access the MobyGames API, [create a MobyGames account](https://www.mobygames.com/user/register/) and then visit your profile page. Click the **API** link under your user name to sign up for an API key. Copy the key shown and use it to set `MOBYGAMES_API_KEY`.

<!-- prettier-ignore -->
!!! important
    MobyGames API became a [paid feature](https://www.mobygames.com/info/api/#non-commercial). RomM will still support it but we won't release any new feature for it.

## Artwork providers

### SteamGridDB

To access steamGridDB API, you need to login into their [website](https://www.steamgriddb.com/) with a [steam account](https://store.steampowered.com/join). Once logged in, go to your [API tab under the preferences page](https://www.steamgriddb.com/profile/preferences/api). Copy the key shown and use it to set `STEAMGRIDDB_API_KEY`.

SteamGridDB only provides custom cover art for games or collections. It's not accessed through the scanner but from the search cover button when manually editing a game.

## Achievements providers

### Retroachievements

RomM is able to display your achievements from [Retroachievements](https://retroachievements.org/). To sync it with your RomM instance, you need to generate an API key from your Retroechievements account in your [settings](https://retroachievements.org/settings)

![RA API key](../resources/metadata_providers/1-ra.png)

Copy the key shown and use it to set `RETROACHIEVEMENTS_API_KEY` and perform a partial scan targeting the platform you want to match with Retroachievements.

After that, each user need to set their own username in their profile and sync it with Retroachievements. A new ``retroachievements`` tab will appear in the `personal` tab in the game details.

![RA details](../resources/metadata_providers/2-ra.png)

To avoid unneccessary API calls, a cached file with the RA database is stored in RomM. Refresh time for that cache file can be changed with the env variable `REFRESH_RETROACHIEVEMENTS_CACHE_DAYS`
