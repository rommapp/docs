---
title: Synology Troubleshooting
description: Fix DSM-specific permission and Docker issues
---

# Synology Troubleshooting

## `ErrNo 13: Access Denied` in Portainer or Container Manager

The usual Synology permission issue. Fix via SSH:

1. **Enable SSH** on the NAS if you haven't (see the [DSM guide](https://kb.synology.com/en-uk/DSM/tutorial/How_to_login_to_DSM_with_root_permission_via_SSH_Telnet)).
2. **SSH in** with your DSM admin account (same credentials as the DSM web UI).
3. **Find your UID/GID** and type `id` and note `uid=NNNN(user) gid=NNNN(group)`.
4. **Fix permissions on every host path**:

```sh
sudo chown -R <user>:<group> /path/to/library
sudo chmod -R a=,a+rX,u+w,g+w /path/to/library

sudo chown -R <user>:<group> /path/to/assets
sudo chmod -R a=,a+rX,u+w,g+w /path/to/assets

sudo chown -R <user>:<group> /path/to/config
sudo chmod -R a=,a+rX,u+w,g+w /path/to/config
```

The paths are whatever you mounted into the container as `/romm/library`, `/romm/assets`, and `/romm/config`.

5. **Restart the containers** with `docker compose restart` or click Restart in Container Manager.

Scans should now complete cleanly!

<!-- prettier-ignore -->
!!! tip
    If you're still getting permission errors *inside* the container after this, the UID/GID running inside the container doesn't match the host files. Either change the container's `user:` directive to match your Synology user, or change the host file ownership to match the container's expected UID.

The permission-mode string comes from [DrFrankenstein's Docker user guide](https://drfrankenstein.co.uk/step-2-setting-up-a-restricted-docker-user-and-obtaining-ids/).

## DSM's built-in MariaDB conflicts

Synology ships its own MariaDB on port `3306`. If you try to run RomM's MariaDB container on the same port, one of them won't bind. To fix, map MariaDB to a different host port in your compose file (the Synology install guide uses `3309:3306`, see [Synology install guide](../install/synology.md)).

## "Page not found" on first open

First-run takes a few minutes on a NAS, as the DB initialisation, migrations, and static asset seeding complete. Wait until the logs show the server is ready, then refresh the page:

```sh
sudo docker compose logs -f
```

## Volume drift after DSM updates

DSM occasionally rotates Docker's data directory or the BTRFS subvolume paths after an update. The container starts but it looks like all your data is gone. To fix:

1. Don't panic. Your host-mounted paths (`/volume1/...`) aren't touched.
2. Check your compose file. Any volumes declared as _named_ Docker volumes (as opposed to host bind mounts) might have been recreated empty.
3. Prefer host bind mounts on Synology specifically (`/volume1/docker/romm/resources`) instead of a named `romm_resources` volume. The [Synology install guide](../install/synology.md) uses this pattern.
