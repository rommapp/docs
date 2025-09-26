# Migrating RomM to a new system

Migrating RomM to a new system is possible; all of the docker volumes must be copied for RomM to run correctly.

Following the the setup in the [Quick Start Guide](https://docs.romm.app/latest/Getting-Started/Quick-Start-Guide/#build) these volumes are created be default

RomM should be stopped before following this guide.

```yaml
volumes:
    mysql_data:
    romm_resources:
    romm_redis_data:

services:
    romm:
        volumes:
         - romm_resources
         - romm_redis_data
    romm-db:
        volumes:
         - mysql_data
```

These volumes will need to manually moved to the new system. This is a straightforward process that includes determining their location and then copying them.

### Determining the docker root directory and copying the volumes
1. First determine the docker root directory
```bash
docker info | grep 'Docker Root Dir'
```
The expected output on a standard linux system:
```bash
Docker Root Dir: /var/lib/docker
```

2. Double check that the volumes have been created by docker and are owned by the docker engine

```bash
docker volume ls
```

Following the default quick start guide the following volumes will have been made

```
DRIVER    VOLUME NAME
local     romm_mysql_data
local     romm_romm_redis_data
local     romm_romm_resources
```

3. Inspect each volume to get the exact location of the volume data

```bash
docker volume inspect romm_mysql_data | grep Mountpoint
```

* The output of the ``docker inspect`` will return the exact storage location of the volumes data
```bash
"Mountpoint": "/var/lib/docker/volumes/romm_mysql_data/_data",
```

4. Copy those volumes into a new location so that they can be safely migrated to a new system **each volume needs to be in its own folder**

```bash
cp -r /var/lib/docker/volumes/romm_mysql_data/_data/ /your/new/path/romm_mysql_data

cp-r /var/lib/docker/volumes/romm_romm_redis_data/_data /your/new/path/romm_romm_redis_data

cp -r /var/lib/docker/volumes/romm_romm_resources/_data /your/new/path/romm_romm_resources
```

5. Update the ``docker-compose.yml`` volume paths with the newly copied data to determine RomM still loads correctly.

```yaml
services:
    romm:
        volumes:
#         - romm_resources
         - /your/new/path/romm_romm_resources
#         - romm_redis_data
         - /your/new/path/romm_romm_redis_data
    romm-db:
        volumes:
#         - mysql_data
        - /your/new/path/romm_mysql_data
```


If RomM starts up correctly, then it is safe to copy all of your RomM folders to a new system.