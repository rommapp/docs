---
title: Scheduled Tasks
description: What RomM runs in the background, how to reschedule it, and how to trigger on demand.
---

# Scheduled Tasks

RomM runs background work through **RQ** (Redis Queue). Tasks fall into four categories:

- **Scheduled**: cron-driven, run on their own.
- **Watcher**: triggered by filesystem events.
- **Manual**: admin-triggered from the UI or API.
- **Enqueued**: side effects of user actions (a scan started from the Scan page, a metadata refresh on a ROM edit). Not listed here.

For the lookup-only reference (every task, its cron default, its env var), see [Scheduled Tasks Reference](../reference/scheduled-tasks.md). This page is the narrative: what each one is for, when to worry, and how to tune.

## The full table

--8<-- "scheduled-tasks.md"

## Configuring cadence

Every scheduled task takes a standard 5-field cron expression:

```text
minute  hour  day-of-month  month  day-of-week
```

Examples:

- `0 3 * * *`: 3 AM daily.
- `0 */6 * * *`: every 6 hours, on the hour.
- `*/30 * * * *`: every 30 minutes.
- `0 2 * * 0`: 2 AM every Sunday.

Set the env var, restart the container. Alembic runs on every start, and the scheduler picks up the new schedule the moment RomM comes back up.

## Disabling a scheduled task

Two ways:

- **The clean way**: set the cron to a time that essentially never fires. `0 0 31 2 *` (Feb 31st) works.
- **The feature-flag way**: some tasks have a dedicated enable toggle, e.g. `ENABLE_SCHEDULED_UPDATE_LAUNCHBOX_METADATA=false` disables the LaunchBox sync.

Check the [env var reference](../reference/environment-variables.md) for which toggles exist.

## Triggering a task manually

Three paths:

### From the Administration page

**Administration → Tasks** shows every task with a Run button. Admins (anyone with `tasks.run` scope) can trigger:

- Folder Scan (launches the Scan page with the task pre-started).
- Cleanup Missing ROMs.
- Cleanup Orphaned Resources.
- LaunchBox Metadata Sync.
- Switch titleDB Fetch.
- Image Conversion.
- RetroAchievements Sync.
- Netplay Cleanup.
- Push-Pull Device Sync.

### From the API

```http
POST /api/tasks/run/{task_name}
Authorization: Bearer <token-with-tasks.run>
```

Full details in the [API Reference](../developers/api-reference.md). Useful for cron runs driven from outside RomM (e.g. an Ansible playbook).

### Via Redis Queue directly

Advanced. Connect to Redis, inspect the `rq` queues, enqueue a job manually. Only do this if you know what you're doing and have a reason the API doesn't serve.

## What each task does

### Folder Scan

The nightly library scan. Defaults to **Quick** mode (skips files already in the DB) so it's cheap even on big libraries. See [Scanning & Watcher](scanning-and-watcher.md) for the full scan mechanic.

### Switch titleDB Fetch

Downloads an updated copy of the Nintendo Switch title ID database used for matching files with names like `0100000000010000.xci`. Weekly is plenty.

### LaunchBox Metadata Sync

Refreshes the local LaunchBox metadata cache used when LaunchBox is enabled as a metadata provider. Nightly at 2 AM by default. Only useful if `LAUNCHBOX_API_ENABLED=true`. Disable it otherwise to save a handful of CPU seconds.

### Image Conversion

Re-encodes fetched cover art, screenshots, and manuals to WebP for faster serving. Nightly at 3 AM. Idempotent, so safe to run more often if you're importing a lot of media.

### RetroAchievements Sync

Refreshes per-user RA progression. Nightly at 4 AM. Users see updated achievement counts on their next load.

### Netplay Cleanup

Sweeps orphaned netplay sessions: rooms where every participant has disconnected but the metadata lingers. Every 30 minutes by default.

### Push-Pull Device Sync

Bidirectional sync with registered devices (handhelds, etc.). Every 15 minutes by default. Disabled implicitly if no devices are registered or if `SSH_PRIVATE_KEY_PATH` isn't configured. See [SSH Sync](ssh-sync.md).

### Cleanup Missing ROMs (manual)

Walks the DB, checks each ROM's file still exists on disk, drops entries whose files are gone. Run after major library moves.

### Cleanup Orphaned Resources (manual)

Deletes cover images, screenshots, and manuals no longer referenced by any ROM. Safe to run any time, and can free tens of GB if you've been churning the library.

## Monitoring tasks

- **Live**: Administration → Tasks page shows every task's current status (queued, running, idle, failed).
- **API**: `GET /api/tasks/status` for a JSON summary. Wire this to an uptime monitor if you want alerts.
- **Logs**: `docker logs romm` → look for `rq.worker` lines.
- **Heartbeat**: `GET /api/heartbeat` returns overall health plus per-task summary, handy for monitoring dashboards.

A task that's been "running" for hours is usually a scan that hit `SCAN_TIMEOUT_HOURS`, and the log will say so. Tasks that fail leave a stack trace in the container logs, and the RQ `failed` queue retains the last few for inspection.

## Tuning for small hosts

Defaults assume you've got a reasonable box. On a Pi or NAS with 2 GB of RAM and a single core:

- Raise the cron intervals (daily → weekly) for the nightlies.
- Set `SCAN_WORKERS=1` to avoid concurrent scan processes.
- Enable the watcher but raise `RESCAN_ON_FILESYSTEM_CHANGE_DELAY` to 60+ seconds: slower reaction, far less churn.
- Disable image conversion if you don't care about WebP (`IMAGE_CONVERSION_INTERVAL_CRON=0 0 31 2 *`).
