<!-- trunk-ignore-all(markdownlint/MD041) -->

Version 3.0 of RomM introduces a number of breaking changes aimed at improving performance and usability, which will require some users to make specific changes before upgrading to ensure compatibility and to take full advantage of the new features.

All of the following changes are reflected in the [example docker-compose.yml file](https://github.com/rommapp/romm/blob/master/examples/docker-compose.example.yml), which has been simplified greatly. **Please read this entire file carefully, as failing to do so may cause RomM to become inaccessible or unresponsive.**

## Dropped support for SQLite

We're removed support for SQLite as we've faced a number of engineering issues with it in the past, and MariaDB has proven more stable and robust. If you currently use SQLite, we'll automatically migrate your data from SQLite to MariaDB, but you'll **first need to make the following changes before upgrading to the latest image.**

In your environment variables, change `ROMM_DB_DRIVER` to `mariadb` (or remove it completely as it's no longer needed). You'll then want to add the following environment variables:

```yaml
- DB_HOST=mariadb
- DB_PORT=3306
- DB_NAME=romm # Should match MYSQL_DATABASE in mariadb
- DB_USER=romm-user # Should match MYSQL_USER in mariadb
- DB_PASSWD= # Should match MYSQL_PASSWORD in mariadb
```

To setup a new MariaDB container, have a look at the [example docker-compose.yml file](https://github.com/rommapp/romm/blob/master/examples/docker-compose.example.yml).

## Authentication as standard

To support new features like EmulatorJS and saves/states management, we've decided to require authentication for all users. Anyone currently running RomM with authentication disabled will need to remove the `ROMM_AUTH_ENABLED` environment variable and add the following ones:

```yaml
- ROMM_AUTH_SECRET_KEY= # Generate a key with `openssl rand -hex 32`
```

We understand that this requirement for authentication might conflict with the way some users currently share their collection with others (unrestricted access for all). However, given the exciting new features we've built, and the ones we're looking to build in the near future, we feel this is the right decision for the project.

## Redis is now built-in

As Redis is [required for authentication](../Getting-Started/Authentication.md) to work, we've integrated it directly into the docker image. If you're currently running the experimental Redis container, you can remove it, along with these environment variables:

```yaml
- ENABLE_EXPERIMENTAL_REDIS
- REDIS_HOST
- REDIS_PORT
```

## Configuration folder

Mounting the `config.yml` file is now done by mounting a `config` folder.. Place your existing `config.yml` file inside a folder and bind it to `/romm/config`:

```yaml
- /path/to/config:/romm/config
```

Updated [config.example.yml](https://github.com/rommapp/romm/blob/master/examples/config.example.yml)

## Support for saves, states and screenshots

This version introduces preliminary support for uploading/downloading saves, states and screenshots (read more about it in the 3.0 release notes). We've added a new volume mapping for these types of files called `assets`, which you'll want to bind to a local folder (or volume) so they'll persist. In your volumes section, add the following mapping, where `/path/to/assets/` is some folder where you'll want to store these assets (and make sure that folder exists):

```yaml
- /path/to/assets:/romm/assets
```

We recommend creating a folder next to your `library`/the one mapped to `/romm/library` in order to keep all your RomM files in the same place.
