<!-- trunk-ignore-all(markdownlint/MD033) -->
<!-- trunk-ignore-all(markdownlint/MD041) -->

This quick start guide will help you get a RomM instance up and running. It is split into 3 parts:

- Prepare
- Build
- Configure

## Prepare

This guide will assume that you already have the following done, if not - stop here and come back when you do.

- [Docker installed](https://docs.docker.com/get-docker/) and running on your system
- Your ROMs organized in the correct [folder structure](./Folder-Structure.md)
- The recommended [metadata providers](./Metadata-Providers.md) set up

<!-- prettier-ignore -->
!!! warning
    RomM works without a metadata API for basic use, but may cause issues with plugins like Playnite. Setting up IGDB API keys is recommended to prevent setup problems.

## Build

Now that we have everything gathered, we can begin getting your instance set up!

1. Download a copy of the latest <a href="https://github.com/rommapp/romm/blob/release/examples/docker-compose.example.yml" target="_blank" rel="noopener noreferrer">docker-compose.example.yml</a> file from GitHub
2. Edit the file and modify the following values to configure the database
    - `MARIADB_ROOT_PASSWORD`: Sets the root password of the database. Use a unique and secure password (_use a password generator for simplicity_)
    - `MARIADB_DATABASE`: Sets the database name for RomM. This can be modified - but it's not necessary
    - `MARIADB_USER`: User to connect to the database with. This can be modified - but it's not necessary
    - `MARIADB_PASSWORD`: Password for the user to connect to the database with. Use a unique and secure password (_use a password generator for simplicity_)
3. Modify the following values in the **environment** to configure the application. _-- Other values can be changed, but should not be done unless you know what you are doing, and are outside the scope of this guide_
    - `DB_NAME`: Name of the database set in the database section
    - `DB_USER`: Name of the user to connect to the database
    - `DB_PASSWD`: Password of the user to connect to the database
4. Run the following command in a terminal and save the output to the `ROMM_AUTH_SECRET_KEY` environment variable:
    ```sh
    openssl rand -hex 32
    ```
    It should look something like this:
    ```sh
    03a054b6ca27e0107c5eed552ea66becd9f3a2a8a91e7595cd462a593f9ecd09
    ```
5. Add your metadata sources API keys:
    - IGDB: `IGDB_CLIENT_ID` and `IGDB_CLIENT_SECRET`
    - ScreenScraper.fr: `SCREENSCRAPER_USER` and `SCREENSCRAPER_PASSWORD`
    - RetroAchievements: `RETROACHIEVEMENTS_USERNAME` and `RETROACHIEVEMENTS_API_KEY`
    - MobyGames: `MOBYGAMES_API_KEY`
    - SteamGridDB: `STEAMGRIDDB_API_KEY`
    - PlayMatch: `PLAYMATCH_API_ENABLED=true`
    - Hasheous: `HASHEOUS_API_ENABLED=true`
    - LaunchBox: `LAUNCHBOX_API_ENABLED=true`
6. Modify the following values in the **volumes** to configure the application
    - `/path/to/library`: Path to the directory where your rom files will be stored (usually the parent folder of the `roms` folder)
    - `/path/to/assets`: Path to the directory where you will store your saves, etc
    - `/path/to/config`: Path to the directory where you will store the config.yml
7. Save the file as _docker-compose.yml_ instead of _docker-compose.example.yml_. It should look something like this:

    <!-- prettier-ignore -->
    ???+ example "Example Docker Compose"
        ``` yaml
        --8<-- "quick-start.docker-compose.yml"
        ```

8. Open the terminal and navigate to the directory containing the docker-compose file
9. Run `docker compose up -d` to kick off the docker pull. You will see it pull the container and set up the volumes and network:

```asciinema-player
    {
        "file": "../latest/resources/asciinema/quick-start-docker-compose.cast",
        "title": "RomM docker compose install",
        "preload": true,
        "loop": true,
        "auto_play": true,
        "cols": 140,
        "rows": 30,
        "fit": "width",
        "terminal_font_size": "small",
        "terminal_line_height": "1.2",
        "terminal_font_family": "Roboto Mono, Monaco, Consolas, monospace"
    }
```

1.  Run `docker ps -f name=romm` to verify that the containers are running
2.  Open a web browser and navigate to `http://localhost:80`, where you should be greeted with the RomM setup page
3.  Go through the setup wizard, setting your admin username and password
4.  Log in with the credentials you set in the last step

## Configure

### Importing your ROMs via scanner

This method is generally the fastest and recommended for first time setup. You need your library properly mounted as a container volume:

1. Log into RomM with your user credentials
2. Click the `Scan` button in the sidebar
3. Select the metadata providers you want to fetch metadata from
4. The system will now begin scanning the rom files and applying metadata to them. You can click on any of the items that it has tagged to see the metadata it pulled without having to stop the scan
5. After the scan completes, click the RomM logo to go back to the main screen. You should see the platforms and recent games it has scanned. You are now ready to rock and RomM!

### Uploading your ROMs via Web Interface

This method is certainly viable, but not recommended if you have a lot of ROMs and/or multiple platforms. It is good for adding after the fact as your collection grows, but wouldn't be recommended for the first set up, nor for multi-file ROMs:

1. Log into RomM with your user credentials
2. Click the `Upload` button in the sidebar
3. Select the platform, then click `+ ADD` and select the ROMs you want to upload in the file selector that appears
4. Click `Upload` to begin uploading the ROMs
5. Repeat for all the `roms/platforms` you have

<img src="https://raw.githubusercontent.com/rommapp/docs/refs/heads/main/docs/resources/quickstart/upload_roms.png" width="780" alt="upload dialog">
