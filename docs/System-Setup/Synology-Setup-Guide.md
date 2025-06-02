## Prerequisites

This guide assumes you're familiar with Docker and have basic knowledge of server management. You'll need:

- A Synology NAS or similar server
- Docker installed
- Basic command line knowledge
- Access to manage network settings

## Setup Process

### 1. Folder Structure Setup

#### ROM Storage Folders

Create the following directory structure for game assets and configuration:

```bash
mkdir -p /volume1/data/media/games/assets
mkdir -p /volume1/data/media/games/config
```

#### ROM Library Structure

RomM requires a **very specific folder structure** for rom files:

```bash
mkdir -p /volume1/data/media/games/library/roms
mkdir -p /volume1/data/media/games/library/bios
```

Note: For supported platforms and their specific folder names, refer to the [official RomM wiki](../Platforms-and-Players/Supported-Platforms.md).

#### Docker Data Folders

Create these folders for project and container data:

```bash
mkdir -p /volume1/docker/romm-project/
mkdir -p /volume1/docker/romm/resources
mkdir -p /volume1/docker/romm/redis-data
mkdir -p /volume1/docker/mariadb-romm
```

### 2. Network Bridge Setup

Create a new network bridge named `rommbridge` following standard Docker networking practices. You can use [this guide](https://drfrankenstein.co.uk/step-3-setting-up-a-docker-bridge-network-in-container-manager/) for reference.

### 3. Key Generation

#### Authentication Key

Generate your authentication key using:

```bash
openssl rand -hex 32
> 03a054b6ca27e0107c5eed552ea66bacd9f3a2a8a91e7595cd462a593f9ecd09
```

Save the output - you'll need it for the `ROMM_AUTH_SECRET_KEY` in your configuration.

#### API Integration Setup

RomM currently supports 3 metadata sources: IGDB, MobyGames and SteamGridDB. Follow the dedicated wiki page for [API key generation](../Getting-Started/Metadata-Providers.md) to set up your API keys. We recommend setting up IGDG at the minimum.

### 4. MariaDB Configuration

<!-- prettier-ignore -->
!!! important
    - This guide uses a dedicated MariaDB container for RomM, but you can use an existing MariaDB instance if preferred
    - We're using MariaDB version 10.7 for compatibility
    - The container uses port 3306 internally, mapped to 3309 externally
    - A simplified health check is implemented for stability

### 5. Docker Compose Configuration

Create a `docker-compose.yml` file with the following content:

<!-- prettier-ignore -->
???+ example "Example Docker Compose"
    ``` yaml
    --8<-- "synology.docker-compose.yml"
    ```

### 6. Initial Launch

1. Start the containers using Docker Compose
2. **Be patient!** The container can take a few minutes to setup on first launch
3. Monitor progress through container logs
4. Access RomM through your browser at `http://your-server-ip:7676`

<!-- prettier-ignore -->
!!! important
    - Replace placeholder values (UIDs, GIDs, passwords, API keys) with your own
    - Ensure proper permissions on all created directories
    - Back up your configuration after successful setup
    - Monitor logs during initial startup for any errors

## Troubleshooting

- If the web interface shows "page not found," wait for initial setup to complete
- For database connection issues, verify MariaDB container health status
- Check logs for both containers if experiencing issues
- Ensure all volumes are properly mounted with correct permissions

## Contributing

This guide is an abridged version of ChopFoo's original guide. If you have any suggestions or improvements, please submit a pull request to the [RomM wiki](https://github.com/rommapp/wiki).
