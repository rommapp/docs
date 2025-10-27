# Setting up RomM for development

Docker provides a quick and easy way to get started with RomM by encapsulating all dependencies within Docker containers. This guide will walk you through the process of setting up RomM for development using Docker.

## Environment setup

### Create the mock structure with at least one rom and empty config for manual testing

```sh
mkdir -p romm_mock/library/roms/switch
touch romm_mock/library/roms/switch/metroid.xci
mkdir -p romm_mock/resources
mkdir -p romm_mock/assets
mkdir -p romm_mock/config
touch romm_mock/config/config.yml
```

### Copy env.template to .env and fill the variables

```sh
cp env.template .env
```

```dotenv
ROMM_BASE_PATH=/app/romm
DEV_MODE=true
```

### Build the image

```sh
docker compose build  # or `docker compose build --no-cache` to rebuild from scratch
```

### Spin up the Docker containers

```sh
docker compose up -d
```

And you're done! You can access the app at `http://localhost:3000`. Any changes made to the code will be automatically reflected in the app thanks to the volume mounts.
