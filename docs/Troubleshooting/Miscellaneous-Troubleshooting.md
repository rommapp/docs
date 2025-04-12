---
title: Miscellaneous Troubleshooting
description: Troubleshooting miscellaneous issues
---

### Restarting the container when using SQLite drops all the data/requires a full re-scan

Verify that the database is mapped to a persistent storage volume in your docker compose or Unraid template.

```yaml
"/path/to/database:/romm/database" # [Optional] Only needed if ROMM_DB_DRIVER=sqlite or not set
```

### Error: `Could not get twitch auth token: check client_id and client_secret`

This is likely due to mis-configured environment variables; verify that `CLIENT_ID` and `CLIENT_SECRET` are set correctly, and that both match the values in IGDB.

### How to view RomM logs to assist with troubleshooting

Each platform may have different logs, but check the stdout logs for docker. For example when using the recommended docker compose setup `docker logs -f romm` will display a continuous stream of the log. Most lines start with `INFO`, `WARNING`, or `ERROR`
