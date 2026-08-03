---
title: NixOS
description: Install RomM natively on NixOS via the services.romm module
---

# NixOS

Unlike the other platforms in this section, NixOS doesn't run the Docker image: RomM is packaged natively in [nixpkgs](https://github.com/NixOS/nixpkgs). The `services.romm` module sets up everything RomM needs — the RomM services themselves, a database, Redis, and a web server — from a few lines of configuration.

<!-- prettier-ignore -->
!!! note "Availability"
    RomM was recently merged into nixpkgs `master`, so it can take a little while to land in the `nixos-unstable` channel. It will be part of the next stable release (NixOS 26.11); whether it gets backported to 26.05 is not decided. You can check which channels have it on [search.nixos.org](https://search.nixos.org/packages?query=romm).

## Before you start

You'll need:

- A NixOS system on a channel that includes the `romm` package (see the note above)
- Your ROM files organised in the expected [folder structure](../getting-started/folder-structure.md)
- API credentials for at least one [metadata provider](../getting-started/metadata-providers.md)

## Minimal configuration

```nix
{
  services.romm = {
    enable = true;
    nginx.virtualHost = "romm.example.org";
  };
}
```

After a `nixos-rebuild switch`, RomM is up on that domain with everything included: a local PostgreSQL database and Redis instance (no credentials to manage), an nginx virtual host serving the app, and in-browser play, streamed downloads and RetroAchievements hashing all working out of the box.

<!-- prettier-ignore -->
!!! note "PostgreSQL, not MariaDB"
    The NixOS module uses PostgreSQL rather than the MariaDB default of the Docker setup. If you're migrating an existing instance from Docker, see [Backup & Restore](backup-and-restore.md) — you can't reuse a MariaDB dump directly.

Don't forget to open the firewall if the machine should be reachable from elsewhere:

```nix
networking.firewall.allowedTCPPorts = [
  80
  443
];
```

## Metadata provider credentials

Secrets don't belong in the Nix store, so provider credentials go into an environment file readable only by root:

```nix
{
  services.romm = {
    enable = true;
    nginx.virtualHost = "romm.example.org";
    environmentFile = "/run/secrets/romm.env";
  };
}
```

With `/run/secrets/romm.env` (deployed via [sops-nix](https://github.com/Mic92/sops-nix), [agenix](https://github.com/ryantm/agenix), or by hand) containing the usual RomM variables:

```bash
IGDB_CLIENT_ID=xxxx
IGDB_CLIENT_SECRET=yyyy
SCREENSCRAPER_USER=zzzz
SCREENSCRAPER_PASSWORD=wwww
```

Non-secret settings can go straight into your configuration via `extraEnvironment`, which accepts any of RomM's [environment variables](../reference/environment-variables.md):

```nix
services.romm.extraEnvironment = {
  WEB_CONCURRENCY = "4";
};
```

## HTTPS

The virtual host is a regular NixOS nginx virtual host, so TLS is the standard one-liner away (HTTPS is required for OIDC and PWA install):

```nix
services.nginx.virtualHosts."romm.example.org" = {
  enableACME = true;
  forceSSL = true;
};
```

The module detects TLS on the virtual host and configures RomM accordingly — no extra settings needed. If you terminate TLS on a different machine instead, point your external [reverse proxy](reverse-proxy.md) at this host's virtual host.

## Library location

RomM expects the library at `/var/lib/romm/library`. To use an existing collection stored elsewhere, bind-mount it there:

```nix
fileSystems."/var/lib/romm/library" = {
  device = "/tank/roms";
  options = [ "bind" ];
};
```

Make sure the mounted collection is readable and writable by the `romm` user. Changes to the library are picked up automatically.

## External database or Redis

`services.romm.database.createLocally` and `services.romm.redis.createLocally` default to `true`. Set them to `false` to use an existing PostgreSQL or Redis instance, and configure `services.romm.database.{host,port,name,user}` / `services.romm.redis.{host,port}` accordingly. Credentials for remote instances (`DB_PASSWD`, `REDIS_PASSWORD`) belong in the `environmentFile`.

## All options

The full set of module options is documented in the NixOS options search: [`services.romm.*`](https://search.nixos.org/options?channel=unstable&query=services.romm).

## Updating

RomM updates arrive with your channel: `nixos-rebuild switch --upgrade` (or your flake update workflow) picks up new versions, and database migrations run automatically.

## Troubleshooting

- Check the services: `systemctl status romm romm-worker romm-scheduler romm-watcher`
- Follow the logs: `journalctl -fu romm`
- Scan issues are usually permissions on the library path — everything under `/var/lib/romm` must be readable and writable by the `romm` user.
