---
title: Kubernetes Troubleshooting
description: Troubleshooting Kubernetes issues
---

### Error: `invalid host in "tcp://<internal ip>:8080" of the "listen" directive in /etc/nginx/conf.d/default.conf:7`

By default, Kubernetes will grab information about the service object linked to a pod and inject it as an environment variable into the pod. In RomM, this leads to the pod attempting to bind to the service IP address, leading to the above fatal error.

To resolve thes error, this default Kubernetes behaviour needs to be disabled by setting the `enableServiceLinks` value in the pod spec to `false`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: romm
  namespace: romm
  ...
spec:
  ...
  template:
    ...
    spec:
      enableServiceLinks: false
      ...
```
