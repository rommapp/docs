---
title: CoreHost
description: Run a managed RomM instance on CoreHost
---

# CoreHost

[CoreHost](https://corehost.io/apps/romm) runs RomM as a managed app: each customer gets their own instance, with the database, cache, and scanner already running alongside the web app. CoreHost tests new RomM releases on its platform before rolling them out, and the instance runs the same unmodified code documented everywhere else in these docs.

[![Deploy on CoreHost](../resources/corehost/button.svg)](https://corehost.io/apps/romm)

<!-- prettier-ignore -->
!!! info "Supporting RomM"
    CoreHost shares a portion of the revenue from RomM instances with the project.

## Plans

Instances are billed hourly from a prepaid balance, and new accounts start with free credit. **Standard** (1 vCPU, 2 GB RAM, 10 GB NVMe) is the smallest plan that fits RomM, and **Power** and **Scale** add CPU, memory, and storage. Your games count toward the plan's storage, so a large collection needs a bigger tier or extra 25 GB storage blocks, which stack on any plan. See the [app page](https://corehost.io/apps/romm) for current prices and regions.

## Install

Pick RomM from the [CoreHost app catalog](https://corehost.io/apps), choose a plan and region, and the instance comes up with a generated password for the `admin` user, shown on the app page in the CoreHost panel. If you lose it, reset it under **Admin password** in the app settings and restart the app.

Fill in the metadata provider credentials before your first scan, since matching quality depends on them (see [Metadata Providers](../getting-started/metadata-providers.md)). Hasheous and LaunchBox need no account, while the others take an API key.

## Adding ROMs

Small batches can go through the [upload dialog](../using/uploads.md) in the browser. For a larger collection, copy files over SFTP into `romm/library/roms/<platform>` (and BIOS files into `romm/library/bios/<platform>`), using the SFTP credentials from the CoreHost panel.

Platform folder names have to match the expected naming (see [Folder Structure](../getting-started/folder-structure.md)). Once the files land, run a scan (see [Your First Scan](../getting-started/first-scan.md)). If you add files over SFTP often, enabling the nightly library scan picks them up without a manual run.

## Backups and updates

CoreHost backs up every instance daily, with a one-click restore from the panel, and can also send encrypted backups to your own S3-compatible storage. Updates are tested on a copy of the instance and roll back on their own if health checks fail. Data is purged 14 days after an instance is cancelled, so take an SFTP copy first if you want to keep it.

## Custom domain

Point a domain at the instance with a CNAME and a TXT verification record, and CoreHost issues the TLS certificate. If your domain uses CAA records, allow `letsencrypt.org`.

## Getting help

For problems with billing, the instance, backups, or the panel, contact [CoreHost support](https://corehost.io/control/support), since they run the hosting. For issues with the app itself, try the [RomM Discord](https://discord.gg/romm) or:

- [Scanning Troubleshooting](../troubleshooting/scanning.md) for matching and ingest problems
- [Authentication Troubleshooting](../troubleshooting/authentication.md) for login issues
