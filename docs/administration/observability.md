---
title: Observability
description: Logs, Sentry error tracking, OpenTelemetry, and the /heartbeat endpoint.
---

# Observability

Four ways to know what RomM is doing:

- **Container logs**: always available, the first stop.
- **`/api/heartbeat`**: health + config summary for uptime monitors.
- **Sentry**: opt-in error tracking with stack traces.
- **OpenTelemetry**: opt-in distributed tracing + metrics.

## Logs

### Log levels

```yaml
environment:
    - LOG_LEVEL=INFO # DEBUG | INFO | WARNING | ERROR
    - FORCE_COLOR=0 # 1 to force colour even when not a TTY
    - NO_COLOR=1 # 1 to disable colour entirely
```

`INFO` is the default and sane for production. Drop to `DEBUG` only while debugging a specific issue, because RomM is chatty on DEBUG.

### Reading logs

Log lines are prefixed with module + timestamp:

```text
INFO:     [RomM][scan_handler][2026-04-18 11:37:40]   Identified as PlayStation 🎮
ERROR:    [RomM][ra_handler][2026-04-18 11:48:55]    Invalid RetroAchievements API key
WARNING:  [RomM][config_manager][2026-04-18 12:01:12] config.yml not found, using defaults
```

Useful greps:

```sh
docker logs romm 2>&1 | grep ERROR
docker logs romm 2>&1 | grep -iE 'auth|oidc|oauth'
docker logs romm 2>&1 | grep -iE 'scan_handler.*Identified'
```

Deployment-specific log commands are in [Miscellaneous Troubleshooting → Viewing RomM logs](../troubleshooting/miscellaneous.md#viewing-romm-logs).

## `/api/heartbeat`

A single-request health + config endpoint. Safe to hit anonymously (though some fields only appear for authenticated callers).

```http
GET /api/heartbeat
```

Returns:

- RomM version.
- Whether the Setup Wizard is still pending.
- Which metadata providers are enabled.
- Which platforms have data.
- OIDC config (redacted credentials).
- Scheduled-task schedule summary.
- Watcher status.

Wire this to your uptime monitor. A failure here is real: the process is down or the DB/Valkey is unreachable.

```bash
# Basic uptime check
curl -fsS https://romm.example.com/api/heartbeat > /dev/null \
  && echo "up" \
  || echo "down"
```

Per-metadata-provider health:

```http
GET /api/heartbeat/metadata/igdb
GET /api/heartbeat/metadata/ss
GET /api/heartbeat/metadata/ra
...
```

Useful when a scan is matching poorly and you want to know whether a provider is down on their side or misconfigured on yours.

## Sentry

Opt-in error tracking: nothing is sent without a DSN.

```yaml
environment:
    - SENTRY_DSN=https://abc123@sentry.example.com/42
```

What's sent:

- Stack traces for unhandled exceptions.
- Per-request timing on slow endpoints.
- Redacted URL parameters (secrets stripped).

What's not sent: ROM filenames, user credentials, metadata provider API keys. RomM filters sensitive parameters before reporting.

Suitable for self-hosted Sentry or [sentry.io](https://sentry.io/); drop the DSN to stop reporting.

## OpenTelemetry

Opt-in distributed tracing and metrics. Useful if you run RomM alongside other services and want unified observability.

```yaml
environment:
    - OTEL_ENABLED=true
    - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
    - OTEL_SERVICE_NAME=romm
    - OTEL_RESOURCE_ATTRIBUTES=deployment.environment=prod
```

Standard [OTEL env vars](https://opentelemetry.io/docs/specs/otel/protocol/exporter/) apply. RomM emits:

- **Traces**: HTTP request spans, DB query spans, RQ job spans.
- **Metrics**: request counts, durations, queue depth, scan progress.
- **Logs**: structured log correlation with trace IDs.

Exporters:

- OTLP gRPC (default, port `4317`).
- OTLP HTTP (port `4318`): set `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf`.

Send to an OpenTelemetry Collector, then fan out to Tempo / Jaeger / Honeycomb / Datadog / Grafana Cloud / whatever you run.

## Task status

Live task state is also exposed programmatically:

```http
GET /api/tasks/status
Authorization: Bearer <token-with-tasks.run>
```

Returns an array of every scheduled / manual / watcher task with current status (`idle`, `queued`, `running`, `failed`) and last run time. Scrape this into your monitoring to alert on "Folder Scan hasn't run in 48 hours", which usually means RQ workers are dead.

## Anti-patterns

- **Don't parse unstructured log lines** for metrics. Use OTEL or `/api/tasks/status`.
- **Don't log at DEBUG in production.** The volume is real and scans will drown in it.
- **Don't scrape HTML pages for health checks.** `/api/heartbeat` is the contract. HTML changes between versions, the API endpoint is stable.

## Minimum recommended stack

For a homelab instance:

- Default `INFO` logs into the container logs → forwarded to Loki / Promtail / whatever you already run.
- `/api/heartbeat` hit every 60 seconds from Uptime Kuma / Gatus.

For a serious deployment:

- Above, plus Sentry DSN configured.
- Plus OpenTelemetry to the collector you already have.
- Alert on: heartbeat failure, task stuck > 1 h, `ERROR`-level log spikes.
