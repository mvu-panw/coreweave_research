# Use sidecar containers with SUNK

Source: https://docs.coreweave.com/products/sunk/manage_sunk/add-sidecars-to-slurm-nodes

# Use sidecar containers with SUNK

> Add sidecar containers to Slurm compute and login node pods

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

You can extend SUNK login and `slurmd` Pods with sidecar containers. This page shows you how to attach sidecars to those Pods so you can run auxiliary services alongside Slurm, such as a local DNS cache or a VPN connector. The walkthrough is for cluster administrators who manage SUNK deployments through the Slurm Helm chart, and it covers both the configuration locations for sidecars and two end-to-end examples you can adapt.

## How to add a sidecar

The following sections describe where to declare sidecars in the Slurm Helm chart values for login and `slurmd` Pods. The chart exposes a `containers` field on both Pod types, along with supporting fields such as `volumes` and `dnsConfig` for further customization. The exact location of these configuration changes differs between login and `slurmd` Pods.

### Add a sidecar to a login Pod

For login Pods, add sidecars under `login.containers`.

The login Pod configuration offers the following options:

```yaml theme={"system"}
login:
  enabled: true
  # ...
  containers: [] # Add sidecar containers here
  volumes: [] # Define volumes needed for the sidecars
  # ... # Additional fields for configuring sidecars may be available
```

### Add a sidecar to a `slurmd` Pod

To add sidecars to a `slurmd` Pod, you must apply the configuration at the node level.

Add sidecars under `compute.nodes.<nodeType>.containers`, where `<nodeType>` represents a custom name assigned to a specific compute type.

```yaml theme={"system"}
compute:
  nodes:
    simple-cpu:
      enabled: true
      replicas: 2 # Adjust to desired amount or scale manually after deploy
      # ...
      containers: [] # Add sidecar containers here
      volumes: [] # Define volumes needed for the sidecars
      dnsPolicy: "..."
      dnsConfig: "..."
      # ... # Other fields may exist to help with sidecar configurations
```

Additional fields are available for configuration. The remaining sections walk through two examples that show how to apply this pattern.

## Sidecar example: Knot Resolver

Knot Resolver is a full caching DNS resolver implementation. You can use it as a proxy to CoreDNS or as a direct replacement. This example shows how to use it as a proxy in a sidecar to improve DNS performance for jobs that involve web scraping. The process involves adding a sidecar container and a corresponding ConfigMap, then deploying both to the Kubernetes namespace.

Follow these steps in order: define the sidecar in the Helm values, create the ConfigMap that backs it, and then deploy the ConfigMap before rolling out the chart changes.

1. To add the Knot Resolver sidecar container, adjust the `containers`, `volumes`, `dnsPolicy`, and `dnsConfig` fields as shown in the following example:

   ```yaml theme={"system"}
   compute:
     ...
     nodes:
       ...
       containers:
       - name: kresd
         image: cznic/knot-resolver:v5.5.3
         command: ["/usr/sbin/kresd", "-c", "/opt/kresd/kresd.conf", "-n"]
         resources:
           limits:
             memory: 64Gi
           requests:
             cpu: 1
             memory: 1Gi
         volumeMounts:
         - name: knot-resolver-conf
           mountPath: /opt/kresd
           readOnly: true
         - name: knot-cache
           mountPath: /var/cache/knot-resolver

       volumes:
       - name: knot-resolver-conf
         configMap:
           name: slurm-knot-resolver-conf
       - name: knot-cache
         emptyDir:
           medium: Memory

       dnsPolicy: "None"
       dnsConfig:
         nameservers:
           - 127.0.0.1 # kresd runs on this address on the node
   ```

2. Create the corresponding ConfigMap YAML file `knot-resolver-configmap.yaml` with the following contents:

   ```yaml theme={"system"}
   kind: ConfigMap
   metadata:
     name: slurm-knot-resolver-conf
   apiVersion: v1
   data:
     kresd.conf: |
       -- Network interface configuration
       net.listen('127.0.0.1', 53, { kind = 'dns' })
       net.listen('127.0.0.1', 853, { kind = 'tls' })
       net.listen('127.0.0.1', 443, { kind = 'doh2' })

       net.listen(net.lo, 8053, { kind = 'webmgmt' })

       modules = {
               'http',
       }

       -- Refer to manual for optimal cache size
       cache.size = 8 * GB

       internalDomains = policy.todnames({'cluster.local'}) # define additional internal networks here
       policy.add(policy.suffix(policy.FLAGS({'NO_CACHE'}), internalDomains)) # let CoreDNS deal with the internal cluster
       policy.add(policy.suffix(policy.STUB({'10.96.0.10'}), internalDomains)) # forward internal traffic to K8s CoreDNS (the default set address is 10.96.0.10)
       policy.add(policy.all(policy.FORWARD({'1.1.1.1', '4.4.4.4', '8.8.8.8'})))
   ```

   For more `kresd.conf` configuration examples, see the [Knot Resolver GitHub repository](https://github.com/CZ-NIC/knot-resolver/tree/master/etc/config).

3. Deploy the ConfigMap into the `slurm` namespace before deploying changes for the sidecars, as in the following example. The sidecar container mounts this ConfigMap on startup, so it must exist in the namespace before the `slurmd` Pods are rolled out.

   ```bash theme={"system"}
   kubectl apply -f knot-resolver-configmap.yaml -n slurm
   ```

   If a ConfigMap with the same name already exists in the specified Kubernetes namespace, the `apply` command updates the existing file with the new configuration. If no such file exists, `apply` creates one.

   The `-f` flag specifies the file name to create or update. In this example, the file to create or update is `knot-resolver-configmap.yaml`.

   The `-n` flag specifies the Kubernetes namespace to create or update the file.

### Test the Knot Resolver sidecar

With the sidecar container and its ConfigMap deployed, the next step is to confirm that the resolver is reachable from inside a `slurmd` Pod and that Slurm itself is still healthy. To test if the DNS server is up and running, run the `dig` command within a Slurm compute node.

First, open a shell in a worker node in the `slurmd` container. In this example, the worker node is `slurm-cpu-epyc-000-002`.

To update the local package list and install the `dnsutils` package, which includes the `dig` command, run:

```bash theme={"system"}
root@slurm-cpu-epyc-000-002:/# apt update && apt install -y dnsutils
```

To check if the DNS resolver is functioning correctly, use the `dig` command:

```bash theme={"system"}
root@slurm-cpu-epyc-000-002:/# dig @127.0.0.1 example.com
```

If `kresd` is working, the result resembles the following:

```text title="Example dig response" theme={"system"}

; <<>> DiG 9.16.50-Debian <<>> @127.0.0.1 example.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 28153
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;example.com.                   IN      A

;; ANSWER SECTION:
example.com.            942     IN      A       93.184.215.14

;; Query time: 2019 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Thu Oct 17 09:23:40 UTC 2024
;; MSG SIZE  rcvd: 56
```

To check that Slurm communications are still working between the controller and compute node, run `scontrol ping`:

```text theme={"system"}
root@slurm-cpu-epyc-000-002:/# scontrol ping
Slurmctld(primary) at slurm-controller is UP
```

## Sidecar example: Tailscale

Tailscale is a VPN service that makes your devices and applications reachable across networks. In this example, you attach your Slurm login node to your Tailscale network through a userspace sidecar so you can reach it from any device on that network. The procedure creates a Tailscale auth key, stores it as a Kubernetes Secret, configures the RBAC the sidecar needs to read that Secret, and registers the sidecar on the login Pod through the Helm chart.

> [!TIP]
>
> This example is also available in [Tailscale's documentation](https://tailscale.com/docs/kubernetes). Clone the [Tailscale GitHub repository](https://github.com/tailscale/tailscale) to get most of the necessary YAML manifests for this example.

1. Log in to [Tailscale's admin console](https://login.tailscale.com/admin/settings/keys) to create a reusable, ephemeral [auth key](https://tailscale.com/docs/features/access-control/auth-keys) for the machine. You use this auth key to authenticate the login node against the Tailscale network.

2. Create a Secret for the `TS_AUTHKEY` through a YAML manifest, for example `ts-secret.yaml`. Replace `[TS-AUTH-KEY]` with the auth key you generated in the previous step.

   ```yaml theme={"system"}
   apiVersion: v1
   kind: Secret
   metadata:
     name: tailscale-auth
   stringData:
     TS_AUTHKEY: [TS-AUTH-KEY]
   ```

3. Add the Secret to the `slurm` namespace with the following command:

   ```bash theme={"system"}
   kubectl apply -f ts-secret.yaml -n slurm
   ```

4. Configure the RBAC surrounding the Secret to allow the sidecar to obtain the Secret. This requires you to edit three files: `rolebinding.yaml`, `role.yaml`, and `sa.yaml`. If you cloned the Tailscale repository, you can find these files under `tailscale/docs/k8s`. Adjust the values in the files to match the following configuration:

   `sa.yaml`:

   ```yaml title="sa.yaml" theme={"system"}
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: tailscale
   ```

   `role.yaml`:

   ```yaml title="role.yaml" theme={"system"}
   apiVersion: rbac.authorization.k8s.io/v1
   kind: Role
   metadata:
     name: tailscale
   rules:
   - apiGroups: [""] # "" indicates the core API group
     resources: ["secrets"]
     # Create can not be restricted to a resource name.
     verbs: ["create"]
   - apiGroups: [""] # "" indicates the core API group
     resourceNames: ["tailscale-auth"]
     resources: ["secrets"]
     verbs: ["get", "update", "patch"]
   ```

   `rolebinding.yaml`:

   ```yaml title="rolebinding.yaml" theme={"system"}
   apiVersion: rbac.authorization.k8s.io/v1
   kind: RoleBinding
   metadata:
     name: tailscale
   subjects:
   - kind: ServiceAccount
     name: tailscale
   roleRef:
     kind: Role
     name: tailscale
     apiGroup: rbac.authorization.k8s.io
   ```

5. Deploy these manifests into the `slurm` namespace by running the following command:

   ```bash theme={"system"}
   make rbac | kubectl apply -f- -n slurm
   ```

6. Edit the login node's `containers` field to include the Tailscale sidecar. Set the `serviceAccountName` to `tailscale`, and `automountServiceAccountToken` to `true`.

   The following example shows these edits in the `charts/slurm/values.yaml` manifest:

   ```yaml title="charts/slurm/values.yaml" theme={"system"}
   login:
     enabled: true
     ...
     serviceAccountName: tailscale
     automountServiceAccountToken: true
     containers:
       - name: nginx # for testing
         image: nginx
       - name: ts-sidecar
         imagePullPolicy: Always
         image: "ghcr.io/tailscale/tailscale:latest"
         securityContext:
           runAsUser: 1000
           runAsGroup: 1000
         env:
           # Store the state in a k8s secret
         - name: TS_KUBE_SECRET
           value: tailscale-auth
         - name: TS_USERSPACE
           value: "true"
         - name: TS_AUTHKEY
           valueFrom:
             secretKeyRef:
               name: tailscale-auth
               key: TS_AUTHKEY
               optional: true
   ```

7. Deploy the sidecar.

### Test the Tailscale sidecar

After you deploy the sidecar, the login node should appear in your Tailscale network and be reachable from any other device on that network. From a machine connected to the Tailscale network, you can check that the Slurm login node is now connected and present:

```bash theme={"system"}
my_machine@abcdef:~/$ tailscale status
100.103.123.42  my_machine           Myself123@    linux   -
100.95.67.54    slurm-login-0        Myself123@    linux   idle, tx 1540 rx 2908
```

Because you added nginx as a machine to test with, you can also run the following from another machine connected to the same Tailscale network:

```html title="Test with curl" theme={"system"}
my_machine@abcdef:~/$ curl http://slurm-login-0
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

If you have `ssh` configured, you can test that with the following command:

```bash theme={"system"}
my_machine@abcdef:~/$ ssh user1@slurm-login-0 -t exec bash -l
user1@slurm-login-0:~$
```
