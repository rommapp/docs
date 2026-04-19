---
title: Kubernetes
description: Deploy RomM on Kubernetes with manifest examples, required quirks, and community Helm charts.
---

# Kubernetes

There's no official Helm chart for RomM in 5.0. This page walks through a production-grade manifest set and points at the community charts worth looking at.

<!-- prettier-ignore -->
!!! note "Community-maintained charts"
    If you'd rather not hand-author manifests, there are community Helm charts around. Check [ArtifactHub](https://artifacthub.io/packages/search?ts_query_web=romm) and the `#kubernetes` channel in the [RomM Discord](https://discord.gg/P5HtHnhUDH). The RomM team doesn't publish or formally support any chart today, so pick one with active maintenance and recent releases.

## What you need

- A cluster running Kubernetes 1.27+.
- Persistent storage for the DB, cache, and RomM's assets/resources/config (block or RWX, see below).
- An Ingress controller (nginx-ingress, Traefik, etc.) for external access.
- cert-manager or equivalent for HTTPS.

## Required quirk: `enableServiceLinks: false`

Kubernetes injects service addresses as environment variables into every pod (`HOSTNAME_PORT=tcp://<service-ip>:<port>`). nginx inside the RomM image picks these up and tries to bind to the service IP, producing:

```text
invalid host in "tcp://<internal ip>:8080" of the "listen" directive in
/etc/nginx/conf.d/default.conf:7
```

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
            enableServiceLinks: false # ← required
```

Without this, RomM crashloops on startup. This is the single most common Kubernetes gotcha. If you're here because of the error above, add the flag and move on.

## Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
    name: romm
```

## Secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
    name: romm-secrets
    namespace: romm
type: Opaque
stringData:
    ROMM_AUTH_SECRET_KEY: "<openssl rand -hex 32>"
    DB_PASSWD: "<db-password>"
    MARIADB_ROOT_PASSWORD: "<root-password>"
    # Metadata providers: fill in only what you've configured:
    IGDB_CLIENT_ID: ""
    IGDB_CLIENT_SECRET: ""
    SCREENSCRAPER_USER: ""
    SCREENSCRAPER_PASSWORD: ""
    RETROACHIEVEMENTS_API_KEY: ""
    STEAMGRIDDB_API_KEY: ""
```

## MariaDB

A single-replica MariaDB is fine for most RomM deployments. Use a StatefulSet so the PVC survives pod restarts.

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
    name: romm-db
    namespace: romm
spec:
    serviceName: romm-db
    replicas: 1
    selector:
        matchLabels: { app: romm-db }
    template:
        metadata:
            labels: { app: romm-db }
        spec:
            enableServiceLinks: false
            containers:
                - name: mariadb
                  image: mariadb:11
                  env:
                      - { name: MARIADB_DATABASE, value: romm }
                      - { name: MARIADB_USER, value: romm-user }
                      - name: MARIADB_PASSWORD
                        valueFrom:
                            {
                                secretKeyRef:
                                    { name: romm-secrets, key: DB_PASSWD },
                            }
                      - name: MARIADB_ROOT_PASSWORD
                        valueFrom:
                            {
                                secretKeyRef:
                                    {
                                        name: romm-secrets,
                                        key: MARIADB_ROOT_PASSWORD,
                                    },
                            }
                  ports:
                      - { name: mysql, containerPort: 3306 }
                  volumeMounts:
                      - { name: data, mountPath: /var/lib/mysql }
                  readinessProbe:
                      exec:
                          command:
                              [
                                  "healthcheck.sh",
                                  "--connect",
                                  "--innodb_initialized",
                              ]
                      periodSeconds: 10
    volumeClaimTemplates:
        - metadata: { name: data }
          spec:
              accessModes: [ReadWriteOnce]
              resources: { requests: { storage: 10Gi } }
---
apiVersion: v1
kind: Service
metadata:
    name: romm-db
    namespace: romm
spec:
    clusterIP: None
    ports:
        - { name: mysql, port: 3306, targetPort: 3306 }
    selector: { app: romm-db }
```

## RomM

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
    name: romm
    namespace: romm
spec:
    replicas: 1
    selector:
        matchLabels: { app: romm }
    template:
        metadata:
            labels: { app: romm }
        spec:
            enableServiceLinks: false # ← required, see top of page
            containers:
                - name: romm
                  image: rommapp/romm:5.0.0
                  env:
                      - { name: DB_HOST, value: romm-db }
                      - { name: DB_NAME, value: romm }
                      - { name: DB_USER, value: romm-user }
                      - name: DB_PASSWD
                        valueFrom:
                            {
                                secretKeyRef:
                                    { name: romm-secrets, key: DB_PASSWD },
                            }
                      - name: ROMM_AUTH_SECRET_KEY
                        valueFrom:
                            {
                                secretKeyRef:
                                    {
                                        name: romm-secrets,
                                        key: ROMM_AUTH_SECRET_KEY,
                                    },
                            }
                      - {
                            name: ROMM_BASE_URL,
                            value: "https://romm.example.com",
                        }
                      - { name: HASHEOUS_API_ENABLED, value: "true" }
                      # ... other metadata provider vars from the secret
                  envFrom:
                      - secretRef: { name: romm-secrets }
                  ports:
                      - { name: http, containerPort: 8080 }
                  volumeMounts:
                      - {
                            name: library,
                            mountPath: /romm/library,
                            readOnly: true,
                        }
                      - { name: assets, mountPath: /romm/assets }
                      - { name: resources, mountPath: /romm/resources }
                      - { name: config, mountPath: /romm/config }
                      - { name: redis-data, mountPath: /redis-data }
                  readinessProbe:
                      httpGet: { path: /api/heartbeat, port: http }
                      initialDelaySeconds: 30
                      periodSeconds: 10
            volumes:
                - name: library
                  persistentVolumeClaim: { claimName: romm-library }
                - name: assets
                  persistentVolumeClaim: { claimName: romm-assets }
                - name: resources
                  persistentVolumeClaim: { claimName: romm-resources }
                - name: config
                  persistentVolumeClaim: { claimName: romm-config }
                - name: redis-data
                  persistentVolumeClaim: { claimName: romm-redis-data }
---
apiVersion: v1
kind: Service
metadata:
    name: romm
    namespace: romm
spec:
    ports:
        - { name: http, port: 80, targetPort: 8080 }
    selector: { app: romm }
```

## Persistent Volume Claims

One PVC per volume. Sizes are rough, so tune to your library.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata: { name: romm-library, namespace: romm }
spec:
    accessModes: [ReadOnlyMany] # your ROM store, typically an RWX mount
    resources: { requests: { storage: 500Gi } }
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata: { name: romm-assets, namespace: romm }
spec:
    accessModes: [ReadWriteOnce]
    resources: { requests: { storage: 20Gi } }
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata: { name: romm-resources, namespace: romm }
spec:
    accessModes: [ReadWriteOnce]
    resources: { requests: { storage: 50Gi } }
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata: { name: romm-config, namespace: romm }
spec:
    accessModes: [ReadWriteOnce]
    resources: { requests: { storage: 1Gi } }
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata: { name: romm-redis-data, namespace: romm }
spec:
    accessModes: [ReadWriteOnce]
    resources: { requests: { storage: 5Gi } }
```

For shared library access (multiple RomM replicas, or CI jobs that bulk-import), use RWX on the library PVC (NFS, CephFS, Longhorn-RWX). Assets must also be RWX if you ever run more than one RomM replica.

## Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
    name: romm
    namespace: romm
    annotations:
        cert-manager.io/cluster-issuer: letsencrypt-prod
        # Crucial: allow large uploads + websockets
        nginx.ingress.kubernetes.io/proxy-body-size: "0"
        nginx.ingress.kubernetes.io/proxy-read-timeout: "3600"
        nginx.ingress.kubernetes.io/proxy-send-timeout: "3600"
spec:
    ingressClassName: nginx
    tls:
        - hosts: [romm.example.com]
          secretName: romm-tls
    rules:
        - host: romm.example.com
          http:
              paths:
                  - path: /
                    pathType: Prefix
                    backend:
                        service:
                            name: romm
                            port: { number: 80 }
```

`proxy-body-size: "0"` is important, because the default is 1 MB and will reject every ROM upload with HTTP 413.

## Scaling notes

- **One RomM replica** is the simple path. The scan runs as a single worker, which prefers a single replica.
- **Multiple replicas** work but you need RWX for `/romm/assets` and `/romm/resources` and an external Redis (set `REDIS_HOST` to a shared service). See [Redis or Valkey](redis-or-valkey.md).
- **No HPA** (horizontal pod autoscaler) on RomM: CPU spikes during scans are normal and not a scaling signal.

## Updating

```sh
kubectl set image -n romm deployment/romm romm=rommapp/romm:5.0.1
```

Alembic runs on startup, so migrations happen automatically. Before major-version upgrades, read the release notes and take a backup (see [Backup & Restore](backup-and-restore.md)).

## Troubleshooting

Common Kubernetes-specific issues: [Kubernetes Troubleshooting](../troubleshooting/kubernetes.md).
