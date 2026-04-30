---
title: Redis or Valkey
description: Session storage, task queue, metadata caching and pubsub
---

# Redis / Valkey

A Redis-protocol server is needed for session storage, the background task queue (RQ), metadata/heartbeat caching, and socket.io pubsub when running multiple replicas. Both **Redis** and **Valkey** (the open-source fork) are supported.

## Embedded

The default `full-image` container runs an embedded Valkey instance, no `REDIS_*` env vars needed. Data is persisted to `/redis-data` inside the container. The reference compose mounts this to a Docker volume (`romm_redis_data`). Don't skip the volume, or you'll lose in-flight tasks on every `docker compose up -d`.

## External container

```yaml
services:
    romm:
        environment:
            - REDIS_HOST=romm-redis
            - REDIS_PORT=6379
            - REDIS_PASSWD=<strong-password>
        depends_on:
            romm-redis:
                condition: service_healthy

    romm-redis:
        image: valkey/valkey:7-alpine # or redis:7-alpine, identical command/volume
        command: ["valkey-server", "--requirepass", "<strong-password>", "--appendonly", "yes"]
        volumes:
            - redis_data:/data
        healthcheck:
            test: ["CMD", "valkey-cli", "-a", "<strong-password>", "ping"]
            interval: 10s

volumes:
    redis_data:
```
