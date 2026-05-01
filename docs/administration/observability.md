---
title: Observability
description: Logs, error tracking and telemetry
---

# Observability

It's often handy to know what's happening under the hood, especially when debugging a scan or task. the observability stack includes:

- **Container logs**: always available, the first stop
- **`/api/heartbeat`** endpoint: health + config summary for uptime monitors
- **Sentry**: opt-in error tracking with stack traces
- **OpenTelemetry**: opt-in distributed tracing + metrics

## Logs

```yaml
environment:
    - LOG_LEVEL=INFO # DEBUG | INFO | WARNING | ERROR
    - FORCE_COLOR=0 # 1 to force colour even when not a TTY
    - NO_COLOR=1 # 1 to disable colour entirely
```

`INFO` is the default and the sane choice for production. Drop to `DEBUG` only while debugging a specific issue, because `DEBUG` is chatty.

### Reading logs

Log lines are prefixed with module + timestamp:

```text
INFO:     [RomM][scan_handler][2026-04-18 11:37:40]   Identified as PlayStation 🎮
ERROR:    [RomM][ra_handler][2026-04-18 11:48:55]    Invalid RetroAchievements API key
WARNING:  [RomM][config_manager][2026-04-18 12:01:12] config.yml not found, using defaults
```

Some useful grep commands:

```sh
docker logs romm 2>&1 | grep ERROR
docker logs romm 2>&1 | grep -iE 'auth|oidc|oauth'
docker logs romm 2>&1 | grep -iE 'scan_handler.*Identified'
```

## `/api/heartbeat`

A single-request endpoint to fetch health and config information. Works when not logged in, though some fields only appear for authenticated callers.

```http
GET /api/heartbeat
```

Wire this to your uptime monitor. A failure here means that the process is down or the DB/Valkey is unreachable.

```bash
# Basic uptime check
curl -fsS https://demo.romm.app/api/heartbeat > /dev/null \
  && echo "up" \
  || echo "down"
```

Per-metadata provider health:

```http
GET /api/heartbeat/metadata/[igdb/ss/ra/...]
```

Useful when a scan is matching poorly and you want to know whether a provider is down on their side or misconfigured on yours.

## Sentry

Opt-in error tracking:

```yaml
environment:
    - SENTRY_DSN=https://abc123@sentry.example.com/42
```

What's sent:

- Stack traces for unhandled exceptions
- Per-request timing on slow endpoints
- Redacted URL parameters (secrets stripped)

What's not sent: ROM filenames, user credentials, metadata provider API keys. Sensitive parameters are filtered before reporting.

## OpenTelemetry

If you're already using OpenTelemetry with your other apps and want unified observability:

```yaml
environment:
    - OTEL_ENABLED=true
    - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
    - OTEL_SERVICE_NAME=romm
    - OTEL_RESOURCE_ATTRIBUTES=deployment.environment=prod
```

Standard [OTEL env vars](https://opentelemetry.io/docs/specs/otel/protocol/exporter/) apply. The app emits:

- **Traces**: HTTP request spans, DB query spans, RQ job spans
- **Metrics**: request counts, durations, queue depth, scan progress
- **Logs**: structured log correlation with trace IDs

Exporters:

- OTLP gRPC (default, port `4317`)
- OTLP HTTP (port `4318`): set `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf`.

Send to an OpenTelemetry Collector, then fan out to Tempo/Jaeger/Honeycomb/Datadog/Grafana/whatever you run.

## Task status

Live task state is also exposed programmatically:

```http
GET /api/tasks/status
Authorization: Bearer <token-with-tasks.run>
```

Returns an array of every scheduled / manual / watcher task with current status (`idle`, `queued`, `running`, `failed`) and last run time. Scrape this into your monitoring to alert on "Folder Scan hasn't run in 48 hours", which usually means RQ workers are dead.

## Anti-patterns

- **Don't parse unstructured log lines** for metrics (use OTEL instead)
- **Don't log at DEBUG in production** as the volume is real and scans will drown in it
- **Don't scrape HTML pages for health checks**; HTML changes between versions while the API endpoint is stable

## Minimum recommended stack

- Default `INFO` logs into the container logs → forwarded to Loki/Promtail/whatever you already run
- `/api/heartbeat` hit every 60 seconds from Uptime Kuma/Gatus
