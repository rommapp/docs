<!-- trunk-ignore-all(prettier) -->

This quick start guide will help you get a RomM instance up and running. It is split into 3 parts:

- Prepare
- Build
- Configure

## Prepare

This guide will assume that you already have the following done, if not - stop here and come back when you do.

- Docker and Docker Compose installed
- A [Twitch](https://dev.twitch.tv) account (optional)
    - 2-factor authentication set up on your Twitch account
    - _This is required to get a developer account and an IGDB key_
- A [Screenscraper](https://www.screenscraper.fr/) account (optional)
- A [MobyGames](https://www.mobygames.com/) account (optional)
- Your ROMs organized in the correct format

<!-- prettier-ignore -->
!!! warning
    Not setting up RomM with a metadata API will work for basic operation but can cause issues with, for instance, the Playnite plugin. It is recommended to setup IGDB API keys to avoid issues during setup.

### Twitch and MobyGames API Keys

Head over to [API key docs](../Getting-Started/Generate-API-Keys.md) to get your Twitch and/or Screenscraper and/or MobyGames keys, then come back here

## Build

Now that we have everything gathered, we can begin getting your instance set up!

<!-- trunk-ignore-begin(markdownlint/MD040) -->
1. Download a copy of the latest [docker-compose.example.yml](https://github.com/rommapp/romm/blob/release/examples/docker-compose.example.yml) file from GitHub
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
5. Modify the following values in the **volumes** to configure the application
    - `/path/to/library`: Path to the directory where your rom files will be stored
    - `/path/to/assets`: Path to the directory where you will store your saves, etc
    - `/path/to/config`: Path to the directory where you will store the config.yml
6. Save the file as _docker-compose.yml_ instead of _docker-compose.example.yml_. It should look something like this:

    <!-- prettier-ignore -->
    ???+ example "Example Docker Compose"
        ``` yaml
        --8<-- "quick-start.docker-compose.yml"
        ```

7. Open the terminal and navigate to the directory containing the docker-compose file
8. Run `docker compose up -d` to kick off the docker pull. You will see it pull the container and set up the volumes and network:```asciinema-player
    {
        "file": "resources/asciinema/quick-start-docker-compose.cast",
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
9. Run `docker ps -f name=romm` to verify that the containers are running
10. Open a web browser and navigate to `http://localhost:80`, where you should be greeted with the RomM setup page
11. Go through the setup wizard, setting your admin username and password
12. Log in with the credentials you set in the setup flow
<!-- trunk-ignore-end(markdownlint/MD040) -->

## Configure

Now that the container is running, we will configure it by importing your ROMs

### Uploading Your ROMs via Web Interface

This method is certainly viable, but not recommended if you have a lot of ROMs and/or multiple platforms. It is good for adding after the fact as your collection grows, but wouldn't be recommended for the first set up, nor for multi-file ROMs

1. Log into RomM with your user credentials
2. Navigate to _Library_ -> _Upload ROMs_
3. Select the platform, then click _ADD ROMs_ and select the ROMs you want to upload in the file selector that appears
4. Click _UPLOAD_ to begin uploading the ROMs
5. Repeat for all the `roms/platforms` you have

<img src="https://github.com/rommapp/romm/assets/3247106/3e398e7a-d653-472c-9f11-82b2f0b52840" width="780" alt="upload dialog">

#### Importing Your ROMs via Scanner

This method is generally the fastest and recommended for first time setup

1. Stop your RomM instance. `docker compose down` if you are in the terminal and directory containing the docker-compose file, otherwise `docker stop romm`
2. Go to the library folder created by RomM, set in the docker-compose file under `:/romm/library` and create a folder named `roms`
3. Copy your platform folders/rom files into the `roms` folder you created
4. Start the RomM instance back up. `docker compose up -d` if you are in the terminal and directory containing the docker-compose file, otherwise `docker start romm`
5. Log into RomM with your user credentials
6. Navigate to _Library_ -> _Scan_
7. The system will now begin scanning the rom files and applying metadata to them. You can click on any of the items that it has tagged to see the metadata it pulled without having to stop the scan
8. After the scan completes, click the RomM logo to go back to the main screen. You should see the platforms and recent games it has scanned. You are now ready to rock and RomM!
```
