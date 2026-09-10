---
title: Cloudzy
description: One-click deploy from the Cloudzy Marketplace
---

# Cloudzy

[Cloudzy](https://cloudzy.com/marketplace/romm) ships RomM in their VPS marketplace, so the whole stack comes up preinstalled on a fresh server.

[![Deploy on Cloudzy](../resources/cloudzy/button.svg)](https://cloudzy.com/marketplace/romm)

<!-- prettier-ignore -->
!!! note "Deployed and supported by Cloudzy"
    Cloudzy builds and maintains the marketplace image, and handles support for the deployment and the server itself.

## Picking a plan

Plans start at **$2.48/mo**, and the image needs at least **2 GB of RAM**. Disk is the real constraint: your ROMs, cover art and save files all live on the VPS, so size the plan around how large your library will grow.

## Deploying

Pick RomM from the [marketplace](https://cloudzy.com/marketplace/romm) and choose a plan and location. The server is provisioned from Ubuntu Server 24.04 LTS with IPv4 and IPv6, and RomM is deployed via Docker Compose.

## After deploy

1. Open `http://<your-server-ip>`. The first boot takes a minute while the database initializes.
2. Finish the Setup Wizard. The first account you create is the admin.
3. Drop ROMs into `/root/romm/library/roms` (and BIOS files into `/root/romm/library/bios`) using a supported [folder structure](../getting-started/folder-structure.md), then run [your first scan](../getting-started/first-scan.md).

The stack lives at `/root/romm`, with its compose file at `/root/romm/docker-compose.yml`, so everything in the [Quick Start](../getting-started/quick-start.md) and the [Environment Variables reference](../reference/environment-variables.md) applies. [Hasheous](../getting-started/metadata-providers.md#hasheous) is preconfigured and needs no API key, so scans work before you add any [provider credentials](../getting-started/metadata-providers.md).

## Putting it behind a domain

The image ships with Caddy. Point a domain at the server IP, set `BASE_URL` to the public URL, add the domain to `/etc/caddy/Caddyfile`, and reload Caddy. It requests a Let's Encrypt certificate automatically. HTTPS is required for OIDC and for installing RomM as a PWA.

## Getting help

For server, billing or image problems, use [Cloudzy's support](https://cloudzy.com/contact-us/). For RomM itself, try the [RomM Discord](https://discord.gg/P5HtHnhUDH) or:

- [Scanning Troubleshooting](../troubleshooting/scanning.md) for matching and ingest problems
- [Authentication Troubleshooting](../troubleshooting/authentication.md) for login issues
