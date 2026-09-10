---
title: Hostinger
description: One-click deploy on a Hostinger VPS with their maintained Docker template
---

# Hostinger

[Hostinger](https://www.hostinger.com/applications/romm) builds and maintains a 1-click RomM template for their VPS plans, so you get a running instance without touching a compose file.

[![Deploy on Hostinger](../resources/hostinger/button.svg)](https://www.hostg.xyz/aff_c?offer_id=815&aff_id=243561&url_id=6779)

<!-- prettier-ignore -->
!!! info "Supporting RomM"
    The link above is an affiliate link. Signups through it send a share of the revenue back to RomM, which helps fund the project. Hostinger builds and maintains the template, and handles support for the VPS itself.

## Picking a plan

Plans start at **$6.49/mo** for KVM 1 (1 vCPU, 4 GB RAM, 50 GB NVMe), which is plenty for RomM itself. Disk is the real constraint: your ROMs, cover art and save files all live on the VPS, so size the plan around how large your library will grow rather than around CPU.

## Deploying

The template installs onto an Ubuntu 24.04 image with Docker and Compose preinstalled. From hPanel, open your VPS, go to **Docker Manager**, and pick RomM from the one-click catalog (see [Hostinger's Docker Manager guide](https://www.hostinger.com/support/12040815-how-to-deploy-your-first-container-with-hostinger-docker-manager/)). You can also select the app while ordering the VPS.

## After deploy

1. Open `http://<your-vps-ip>` (Docker Manager shows the mapped port if it isn't `80`). The first boot takes a minute while the database initializes.
2. Finish the Setup Wizard. The first account you create is the admin.
3. Upload ROMs into the library volume using a supported [folder structure](../getting-started/folder-structure.md), then run [your first scan](../getting-started/first-scan.md).

Environment variables, ports and volumes stay editable from Docker Manager after the fact. Two worth setting early:

- **`ROMM_AUTH_SECRET_KEY`**: generate one with `openssl rand -hex 32`. Rotating it later invalidates every session and invite link.
- **Metadata provider credentials**: see [Metadata Providers](../getting-started/metadata-providers.md). [Hasheous](../getting-started/metadata-providers.md#hasheous) needs no API key, so scans work before you set anything up.

## Putting it behind a domain

Point a domain at the VPS IP, terminate TLS with a [reverse proxy](reverse-proxy.md), and set `BASE_URL` to the public URL. HTTPS is required for OIDC and for installing RomM as a PWA.

## Getting help

For VPS, billing or template problems, use [Hostinger's support](https://www.hostinger.com/support/). For RomM itself, try the [RomM Discord](https://discord.gg/P5HtHnhUDH) or:

- [Scanning Troubleshooting](../troubleshooting/scanning.md) for matching and ingest problems
- [Authentication Troubleshooting](../troubleshooting/authentication.md) for login issues
