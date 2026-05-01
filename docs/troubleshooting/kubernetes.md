---
title: Kubernetes Troubleshooting
description: Fix Kubernetes-specific RomM issues.
---

# Kubernetes Troubleshooting

## `invalid host in "tcp://<ip>:8080" of the "listen" directive`

The flagship K8s gotcha. Kubernetes auto-injects service addresses as env vars (`SERVICENAME_PORT=tcp://...`), which the nginx then tries to bind to.

Fix: disable service-link env vars on the pod.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
    name: romm
    namespace: romm
spec:
    template:
        spec:
            enableServiceLinks: false # ← this line
```

Covered in full in the [Kubernetes install guide](../install/kubernetes.md#required-quirk-enableservicelinks-false).

## Large uploads rejected with `413 Request Entity Too Large`

The ingress controller is capping request body size. Default for nginx-ingress is 1 MB, which won't survive a single ROM upload.

Add the annotation:

```yaml
metadata:
    annotations:
        nginx.ingress.kubernetes.io/proxy-body-size: "0"
```

Traefik equivalent:

```yaml
metadata:
    annotations:
        traefik.ingress.kubernetes.io/request-maxsize: "0"
```

Cloudflare (when in front of your ingress): check plan limits. Free tier caps uploads at 100 MB regardless of what your cluster allows.

## WebSockets disconnect immediately

Ingress isn't forwarding the WebSocket upgrade.

nginx-ingress:

```yaml
metadata:
    annotations:
        nginx.ingress.kubernetes.io/proxy-read-timeout: "3600"
        nginx.ingress.kubernetes.io/proxy-send-timeout: "3600"
```

## Pod crashes on startup: `permission denied` writing to `/romm/resources`

The container is running as a non-root user but the PVC came up with wrong ownership.

Two fixes:

- **Init container** that chowns the PV on first start:

    ```yaml
    initContainers:
        - name: fix-permissions
          image: busybox
          command:
              [
                  "sh",
                  "-c",
                  "chown -R 1000:1000 /romm/resources /romm/assets /romm/config /redis-data",
              ]
          volumeMounts:
              - { name: resources, mountPath: /romm/resources }
              - { name: assets, mountPath: /romm/assets }
              - { name: config, mountPath: /romm/config }
              - { name: redis-data, mountPath: /redis-data }
          securityContext:
              runAsUser: 0
    ```

- **Storage class that supports `fsGroup`**: add `fsGroup: 1000` to the pod's `securityContext`. Works on most CSI drivers but not all.

## Pod can reach the DB but RomM crashes with `ConnectionRefused`

Startup ordering. RomM starts before the DB is ready, fails, and crashlooped-restarts forever because the restart is too fast for the DB to catch up.

Fix: add an init container that waits, or a `readinessProbe` + generous `startupProbe` on the DB StatefulSet. The [Kubernetes install guide](../install/kubernetes.md#mariadb) has a readiness probe baked in, so check you're using it.

## Scheduler tasks don't run

RomM schedules tasks via RQ. If Redis is an external service and the pod can't reach it, scheduled tasks silently don't fire.

Check:

```sh
kubectl exec -n romm deploy/romm -- redis-cli -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASSWD ping
# should print "PONG"
```

If that fails, network policy is blocking the pod or the Redis service name doesn't resolve.

## `OOMKilled` during large scans

Scans of big libraries with hash calculation spike memory. Default pod memory limits are often too tight.

Raise the limit:

```yaml
resources:
    requests:
        memory: "1Gi"
    limits:
        memory: "4Gi"
```

Or disable hashing on the Scan page to cut memory use by ~80% (you lose RetroAchievements + Hasheous matching, see [Metadata Providers](../administration/metadata-providers.md)).

## Still stuck

- Full install reference: [Kubernetes](../install/kubernetes.md)
- [Discord](https://discord.gg/romm) `#kubernetes` channel
- Include your ingress controller, storage class, and the exact error from `kubectl logs` when asking for help.
