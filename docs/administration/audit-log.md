---
title: Audit Log
description: A record of who downloaded, played, changed and signed in to what
---

# Audit Log

The audit log records who did what on the server: downloads and player launches, play sessions, uploads and edits, collection changes, scans and tasks, and security events like sign-ins, failed sign-ins and permission changes. Admins read it in the Events tab of the logs settings page, filtered by user, category and date, with a search over names and IP addresses.

Each event keeps the actor, the action, its target, when it happened, the client's IP address and, for a request made with a device-bound token, the [device](../using/devices.md) it came from. Names are copied into the event, so it still reads after the user or the game it names is deleted. Recording is best effort, so a request still succeeds when its event can't be written.

## What's recorded

Events fall into five categories:

| Category      | Actions                                                                                                                                                                                                                                                                                                                                                                                        |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `consumption` | `rom.download`, `rom.bulk_download`, `rom.player_load`, `rom.play`                                                                                                                                                                                                                                                                                                                             |
| `library`     | `rom.upload`, `rom.create`, `rom.edit`, `rom.match`, `rom.unmatch`, `rom.delete`, `rom.file_delete`, `platform.create`, `platform.edit`, `platform.delete`, `firmware.upload`, `firmware.delete`, `config.update`                                                                                                                                                                              |
| `collections` | `collection.create`, `collection.edit`, `collection.delete`, `collection.add_roms`, `collection.remove_roms`, `smart_collection.create`, `smart_collection.edit`, `smart_collection.delete`                                                                                                                                                                                                    |
| `operations`  | `scan.start`, `scan.finish`, `scan.stop`, `task.run`                                                                                                                                                                                                                                                                                                                                           |
| `security`    | `auth.login`, `auth.login_failed`, `auth.password_reset_request`, `auth.password_reset`, `user.create`, `user.register`, `user.edit`, `user.delete`, `user.permissions_edit`, `permission_group.create`, `permission_group.edit`, `permission_group.delete`, `visibility.hide`, `visibility.unhide`, `client_token.create`, `client_token.regenerate`, `client_token.revoke`, `device.approve` |

Some actions and actors need more detail:

- **`rom.download` and `rom.player_load`** both come from the ROM content endpoint. When a player fetches the file to run it, the client passes `purpose=play` on `GET /api/roms/{id}/content/{file_name}` and the fetch is recorded as a player load. Any other fetch is a download (`purpose=download`, the default). A repeat of the same download by the same caller within 10 minutes counts as one event, so resumed and ranged downloads don't flood the log.
- **`rom.play`** is a [play session](../using/saves-and-states.md) reported by a player or a companion app, recorded at the time the session started.
- **Actors** are a user, an anonymous visitor (a [kiosk](authentication.md#kiosk-mode) guest, a download with endpoint auth turned off, or a failed sign-in for a username that doesn't exist), or the system for scheduled tasks and the filesystem watcher.

## Who can read it

| Caller                               | Sees                        |
| ------------------------------------ | --------------------------- |
| An admin with the `users.read` scope | Everyone's events           |
| Any other signed-in user (`me.read`) | Only the events they caused |

Only admins get the Events tab in the UI, but other users can still read their own history through the API. Either way, events about a platform or game the caller [can't see](users-and-roles.md) are left out, so a hidden or age-restricted game doesn't leak through the log.

## Client IP addresses

Each event records the client address as the web server resolved it. Behind a reverse proxy, that's the address from `X-Forwarded-For`, which is only trusted when the proxy's own address is in `FORWARDED_ALLOW_IPS`. The default trusts loopback and the private ranges, so a proxy on a public address has to be added, or every event is logged as coming from the proxy (see [Reverse Proxy](../install/reverse-proxy.md)).

## Retention

Events are kept for 90 days by default, and a scheduled cleanup deletes older ones daily at `30 4 * * *`, in batches so the table stays writable while it runs.

```yaml
environment:
    - AUDIT_LOG_RETENTION_DAYS=365 # 0 keeps events forever
```

With `AUDIT_LOG_RETENTION_DAYS=0` the cleanup task is turned off and the table only grows, so keep an eye on the database's size on a busy instance (see [Scheduled Tasks](scheduled-tasks.md)).

## API

`GET /api/audit-events` returns events newest first, `50` per page by default and at most `200`.

| Query param   | Description                                                                                                 |
| ------------- | ----------------------------------------------------------------------------------------------------------- |
| `limit`       | Page size, `1` to `200`                                                                                     |
| `offset`      | Events to skip                                                                                              |
| `actor_id`    | Only these users' events, repeatable. Ignored unless the caller sees everyone.                              |
| `action`      | Only these actions, repeatable, such as `action=rom.download&action=rom.player_load`                        |
| `category`    | Only these categories, repeatable: `consumption`, `library`, `collections`, `operations`, `security`        |
| `target_type` | `rom`, `platform`, `firmware`, `collection`, `smart_collection`, `user`, `client_token`, `device` and so on |
| `target_id`   | The target's id, used with `target_type`                                                                    |
| `since`       | ISO 8601 timestamp, inclusive                                                                               |
| `until`       | ISO 8601 timestamp, exclusive                                                                               |
| `search`      | Substring match on the actor's name, the target's name or the IP address                                    |
| `max_id`      | Pins later pages to the events the first page saw                                                           |

The response is a page of `items` with `total`, `limit`, `offset` and `max_id`. Pass the first page's `max_id` back on later pages, so events recorded while you page through don't shift the results.

```sh
curl -G https://romm.example.com/api/audit-events \
  -H "Authorization: Bearer $ROMM_TOKEN" \
  --data-urlencode "category=security" \
  --data-urlencode "since=2026-10-01T00:00:00Z"
```
