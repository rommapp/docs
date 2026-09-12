---
title: Scheduled Tasks
description: Runs tasks in the background, reschedule and trigger them on demand
---

# Scheduled Tasks

RomM runs background work through **RQ** (Redis Queue). Tasks fall into four categories:

- **Scheduled**: cron-driven, run on their own
- **Watcher**: triggered by filesystem events
- **Manual**: user-triggered from the UI or API
- **Enqueued**: side effects of user actions (a scan on the `/scan` page, a metadata refresh on a ROM edit, etc.)

## The full table

--8<-- "scheduled-tasks.md"

## Configuring cadence

Every scheduled task takes a standard 5-field cron expression:

- `0 3 * * *`: 3 AM daily
- `0 */6 * * *`: every 6 hours, on the hour
- `*/30 * * * *`: every 30 minutes
- `0 2 * * 0`: 2 AM every Sunday

Set the env var and restart the container. The scheduler picks up the new schedule as soon as RomM is back.

## Enabling a scheduled task

Most tasks have an `ENABLE_*` environment variable, like `ENABLE_SCHEDULED_UPDATE_LAUNCHBOX_METADATA=true` which enables the LaunchBox sync. Set both the enable var and its cron var, since a task with an empty cron string has nothing to schedule and stays unscheduled even when enabled.

Unlike other tasks, **build recommendations index** ships enabled, because the [recommendation](../using/recommendations.md) sections read that index and similar games sits empty without it. Setting `ENABLE_SCHEDULED_BUILD_RECOMMENDATIONS=false` stops the nightly rebuild, but doesn't hide either section; users turn those off in their own settings.

The housekeeping tasks (netplay cleanup, upload tmp cleanup, ZIP cache cleanup) are always on and have no env vars. Check the [env var reference](../reference/environment-variables.md) for the full list.

## Triggering a task manually

### From the Administration page

**Administration → Tasks** lists every task with its status and a way to run it. Anyone with the `tasks.run` scope can fire one off, scheduled tasks included, which saves waiting for the next cron tick after a config change.

### From the API

```http
POST /api/tasks/run/{task_name}
Authorization: Bearer <token-with-tasks.run>
```

## Monitoring tasks

- **Live**: Administration → Tasks page shows every task's current status (queued, running, idle, failed).
- **API**: `GET /api/tasks/status` for a JSON summary. Wire this to an uptime monitor if you want alerts.
- **Logs**: `docker logs romm` → look for `rq.worker` lines.

A task that's been "running" for hours is usually a scan that hit `SCAN_TIMEOUT`, and the logs will say so. Tasks that fail leave a stack trace in the container logs, and the RQ `failed` queue retains the last few for inspection.

## Tuning for small hosts

On a Raspberry Pi or NAS with 2 GB of RAM and/or a single CPU core:

- Raise the cron intervals (daily → weekly) for the nightlies
- Set `SCAN_WORKERS=1` and `WEB_SERVER_CONCURRENCY=1`, both of which default to `4`
- Enable the watcher but raise `RESCAN_ON_FILESYSTEM_CHANGE_DELAY` to 30+ minutes
- Disable image conversion if you don't care about WebP (`ENABLE_SCHEDULED_CONVERT_IMAGES_TO_WEBP=false`)
- On a big library, set `ENABLE_SCHEDULED_BUILD_RECOMMENDATIONS=false` to skip the nightly build
