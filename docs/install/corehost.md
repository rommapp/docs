---
title: CoreHost
description: Run a managed RomM instance on CoreHost
---

# CoreHost

[CoreHost](https://corehost.io/p/romm) runs RomM as a managed app. Each customer gets their own instance, with the database, cache, and scanner already set up next to the web app. CoreHost tests each RomM release before rolling it out, and instances run the same unmodified RomM that the rest of these docs describe.

[![Deploy on CoreHost](../resources/corehost/button.svg)](https://corehost.io/p/romm)

<!-- prettier-ignore -->
!!! info "Supporting RomM"
    CoreHost shares a portion of the revenue from RomM instances with the project.

## Plans

Instances are billed hourly from a prepaid balance, and new accounts start with free credit. Standard (1 vCPU, 2 GB RAM, 10 GB NVMe) is the smallest plan that fits RomM, and Power and Scale add more CPU, memory, and storage. Your games count against the plan's storage, so a large collection needs a bigger plan or extra 25 GB storage blocks, which you can add to any plan. See the [app page](https://corehost.io/p/romm) for current prices and regions.

## Install

Open the [RomM app on CoreHost](https://corehost.io/p/romm) and choose a plan and region. The new instance gets a generated password for the `admin` user, which the CoreHost panel shows on the app page. If you lose it, reset it under **Admin password** in the app settings and restart the app.

Set up metadata provider credentials before your first scan, because they decide how well games get matched (see [Metadata Providers](../getting-started/metadata-providers.md)). Hasheous and LaunchBox need no account, while the others take an API key.

## Adding ROMs

Small batches can go through the [upload dialog](../using/uploads.md) in the browser. For a larger collection, copy files over SFTP into `romm/library/roms/<platform>` (and BIOS files into `romm/library/bios/<platform>`), using the SFTP credentials from the CoreHost panel.

Platform folder names must follow RomM's naming (see [Folder Structure](../getting-started/folder-structure.md)). After the upload finishes, run a scan (see [Your First Scan](../getting-started/first-scan.md)). If you add files over SFTP often, turn on the nightly library scan so new files get picked up without a manual run.

## Backups and updates

CoreHost backs up every instance daily, and you can restore a backup in one click from the panel. It can also send encrypted backups to your own S3-compatible storage. Updates run on a copy of the instance first and roll back automatically if health checks fail. CoreHost deletes an instance's data 14 days after you cancel it, so copy your files off over SFTP first if you want to keep them.

## Custom domain

Point a domain at the instance with a CNAME and a TXT verification record, and CoreHost issues the TLS certificate. If your domain uses CAA records, allow `letsencrypt.org`.

## Getting help

For problems with billing, the instance, backups, or the panel, contact [CoreHost support](https://corehost.io/control/support), since they run the hosting. For issues with the app itself, try the [RomM Discord](https://discord.gg/romm) or:

- [Scanning Troubleshooting](../troubleshooting/scanning.md) for matching and ingest problems
- [Authentication Troubleshooting](../troubleshooting/authentication.md) for login issues
