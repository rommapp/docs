---
title: Redis or Valkey
description: Why RomM needs Redis, how it's run, and when to split it out.
---

# Redis or Valkey

RomM needs a Redis-protocol server. It's used for:

- **Session storage**: login sessions, CSRF tokens
- **Background task queue**: scans, metadata syncs, sync operations run through RQ (Redis Queue).
- **Cache**: metadata lookups, heartbeat data, paired-device tokens, rate-limit counters
- **socket.io**: multi-instance pubsub for live updates (only relevant if you're running more than one RomM container)

Both **Redis** and **Valkey** (the open-source Redis fork maintained by the Linux Foundation after Redis Inc.'s license change) are supported. They're interchangeable: Valkey is a drop-in wire-compatible replacement. Pick either.

## Option A: embedded (default)

The default `full-image` container runs a Redis server inside itself. Zero config, fine for single-instance deployments. The `REDIS_HOST` / `REDIS_PORT` defaults (`localhost:6379`) point at the embedded instance, so leave them alone.

**Data** is persisted to `/redis-data` inside the container. In the reference compose, that's mounted to a Docker volume (`romm_redis_data`) so queue state survives restarts. Don't skip the volume, because you'll lose in-flight tasks on every `docker compose up -d`.

## Option B: external Redis container

Better for:

- Any production instance you care about
- Multiple RomM replicas sharing state
- Homelabs that already run a Redis box and want consistency

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
        image: redis:7-alpine
        command:
            [
                "redis-server",
                "--requirepass",
                "<strong-password>",
                "--appendonly",
                "yes",
            ]
        volumes:
            - redis_data:/data
        healthcheck:
            test: ["CMD", "redis-cli", "-a", "<strong-password>", "ping"]
            interval: 10s
            timeout: 3s
            retries: 5

volumes:
    redis_data:
```

### Valkey drop-in

```yaml
romm-redis:
    image: valkey/valkey:7-alpine
    command:
        [
            "valkey-server",
            "--requirepass",
            "<strong-password>",
            "--appendonly",
            "yes",
        ]
    # everything else the same
```

## Option C: external managed Redis

If you've got an AWS ElastiCache / Upstash / Redis Cloud instance, point RomM at it:

```yaml
environment:
    - REDIS_HOST=my-redis.cache.amazonaws.com
    - REDIS_PORT=6379
    - REDIS_USERNAME=romm # omit if your Redis uses legacy auth
    - REDIS_PASSWORD=<managed-pw>
    - REDIS_SSL=true # for managed Redis, almost always yes
    - REDIS_DB=0 # separate RomM from other apps on the same instance
```

The full list of Redis env vars lives in [Environment Variables](../reference/environment-variables.md).

## Tuning

RomM's Redis usage is light: sessions, a queue, a bit of cache. Defaults are fine for anything up to tens of thousands of ROMs and a few dozen users. Things to know:

- **`appendonly yes`** is strongly recommended (what the reference compose uses). Without it, a crash loses any task currently in the queue.
- **RDB snapshotting** is fine on top. `save 60 1` gives you a minutely snapshot.
- **Memory**: RomM doesn't hold large blobs in Redis. A 256 MB `maxmemory` is plenty for most instances.
- **Key eviction**: leave `maxmemory-policy` alone (default: `noeviction`). RomM doesn't tolerate silent key loss: sessions would drop and running tasks would lose state.

## Verifying it works

```sh
docker exec romm redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" -a "$REDIS_PASSWD" ping
# PONG
```

If you see `PONG` from the RomM container, you're good. If not, check:

- That the DNS name in `REDIS_HOST` resolves from the RomM container (use `docker exec romm getent hosts romm-redis`)
- That the password is correct. `redis-cli -a` will say `NOAUTH` if wrong.
- That `REDIS_SSL=true` matches whether the server actually requires TLS

Debugging further: see the Redis line in `docker logs romm` at startup, where RomM logs the connection target.
