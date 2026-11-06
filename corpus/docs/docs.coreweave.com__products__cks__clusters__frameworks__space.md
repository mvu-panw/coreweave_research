# Run SPACE on CKS

Source: https://docs.coreweave.com/products/cks/clusters/frameworks/space

# Run SPACE on CKS

> Deploy SPACE, an open source Firecracker sandbox platform, on CKS CPU Nodes for evaluation

[SPACE](https://github.com/perplexityai/SPACE) (Sandboxed Platform for Agentic Code Execution) is an open source (Apache-2.0) platform from Perplexity that runs code in isolated [Firecracker](https://firecracker-microvm.github.io/) microVMs. Clients create sandboxes from templates and use them through an HTTP API to run commands, stream output, read and write files, and pause, suspend, and resume sandboxes. SPACE also has an [E2B-compatible API](https://space.docs.perplexity.ai/guide/ecw.html), which this guide doesn't set up.

Each sandbox is a Kubernetes Pod with the `space` RuntimeClass. On a Kubernetes Node, containerd is a runtime that runs the Node's containers. On each worker Node, containerd hands the sandbox Pods to SPACE's containerd shim, `containerd-shim-space-v2`. The shim boots a Firecracker microVM instead of a container. Kubernetes schedules and places sandboxes, and SPACE's node services manage the microVM lifecycle.

SPACE's local-development deployment runs on Kind, a tool that runs Kubernetes clusters in containers. This guide reuses several of its scripts and Helm charts, so their paths contain `kind`.

This guide is for cluster operators who want to evaluate SPACE on CoreWeave Kubernetes Service (CKS). It uses SPACE's own charts and scripts, and covers the following:

* Prepare Node Pools and worker Nodes.
* Build the SPACE images.
* Install SPACE's dependencies, its Secrets, and SPACE itself.
* Create a first sandbox.

By the end of this guide, you have an evaluation deployment of SPACE on your cluster and a first sandbox that runs a command.

> [!WARNING]
>
> **This deployment is for evaluation only**
>
> SPACE is a third-party project. Report SPACE issues directly to the [SPACE repository](https://github.com/perplexityai/SPACE/issues).
>
> SPACE's install path for existing clusters is a development and evaluation path, not a production deployment. This guide also uses SPACE's test key broker, which isn't designed to secure encryption keys. Use test data only.
>
> SPACE changes worker Node configuration: you install a containerd shim, edit the containerd configuration, and restart containerd on each worker. SPACE's node services run privileged with host networking. Use worker Nodes that run no workloads other than SPACE.

## Prerequisites

Before you start, you need the following:

* A [CKS cluster](https://docs.coreweave.com/products/cks/clusters/create.md) that uses Cilium as its network plugin.
* The CKS Admin role, and Kubernetes permissions to create privileged Pods and cluster-scoped resources. See [CKS authentication and access](https://docs.coreweave.com/products/cks/auth-access/introduction.md).
* On your workstation: [`kubectl`](https://kubernetes.io/docs/reference/kubectl/) [configured for your cluster](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md), [Helm](https://helm.sh/docs/intro/install/), Bash 4 or later, OpenSSL 3, Python 3.8 or later, `git`, `jq`, and `curl`. macOS includes Bash 3.2, so install a later version, for example with Homebrew.
* An `amd64` Linux build host with Docker.
* A container registry that your cluster's Nodes can pull from.

Run the workstation commands in this guide from a SPACE checkout, in one Bash session. Clone SPACE at the commit that CoreWeave tested this guide with:

```bash theme={"system"}
git clone https://github.com/perplexityai/SPACE.git
cd SPACE
git checkout 8be56e167a33c57d5b8dc9bbd74baf9ed06ddc09
```

## Prepare the cluster

Before you install SPACE, prepare the cluster it runs on. The following sections describe how to create the Node Pools, add a default StorageClass, create the namespaces and RuntimeClass, allow sandbox network traffic, and set up each worker Node.

### Create Node Pools

SPACE uses two [Node Pools](https://docs.coreweave.com/products/cks/nodes/create.md). Set these labels in each pool's `nodeLabels`:

| Pool | Labels | Instances |
| - | - | - |
| Infra | `space.pplx.net/infra: "true"` | Any CPU instance. Runs the API services and SPACE's dependencies. |
| Workers | `space.pplx.net/node-pool: sandbox` and `node.kubernetes.io/space-enabled: "true"` | `amd64` bare-metal [CPU instances](https://docs.coreweave.com/platform/instances/cpu-instances.md) that expose `/dev/kvm`. |

For a small evaluation, one Node Pool can carry all three labels and run both roles.

CoreWeave tested this deployment on one [General Purpose AMD Turin (High Storage)](https://docs.coreweave.com/platform/instances/cpu/turin-gp-l.md) Node, `turin-gp-l`, that runs both roles.

Every sandbox is a Pod, so the kubelet's `maxPods` limit caps sandboxes per Node. The default of 110 allows about 100 sandboxes on a worker of any size. To run more, raise `maxPods` in the cluster's [kubelet configuration](https://docs.coreweave.com/platform/terraform/resources/cks_cluster.md#optional) before you prepare the workers. The change applies to every Node in the cluster and takes effect after a Node reboot, which clears the worker preparation.

### Install a default StorageClass

SPACE's PostgreSQL chart requests a PersistentVolumeClaim from the cluster's default StorageClass. Check whether the cluster has one:

```bash theme={"system"}
kubectl get storageclass
```

If a StorageClass is marked `(default)`, skip to the next section. Otherwise, install [local-path-provisioner](https://github.com/rancher/local-path-provisioner) with its data on each Node's local NVMe disk, and make its `local-path` StorageClass the default:

```bash theme={"system"}
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.37/deploy/local-path-storage.yaml
kubectl -n local-path-storage patch configmap local-path-config --type merge -p \
  '{"data":{"config.json":"{\"nodePathMap\":[{\"node\":\"DEFAULT_PATH_FOR_NON_LISTED_NODES\",\"paths\":[\"/mnt/local/local-path-provisioner\"]}]}"}}'
kubectl -n local-path-storage rollout restart deploy/local-path-provisioner
kubectl patch storageclass local-path \
  -p '{"metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

A local-path volume lives on one Node's local disk, and CKS clears that disk when the Node reboots. The database doesn't survive a reboot of its Node.

### Create namespaces and the RuntimeClass

SPACE runs in the `space` namespace and places sandbox Pods in the `sandboxes` namespace. Create both namespaces and the RuntimeClass that sandbox Pods reference:

```bash theme={"system"}
kubectl create namespace space
kubectl create namespace sandboxes
kubectl apply -f infra/space/kind/manifests/runtimeclass.yaml
```

### Allow sandbox Pods to reach their node services

Each sandbox Pod forwards control traffic to SPACE's node API on its Node, on port `9800`. SPACE's sandbox NetworkPolicy blocks traffic from sandbox Pods to Node addresses, and CKS's network plugin, Cilium, enforces it. Allow that one port with a CiliumNetworkPolicy:

```yaml title="sandbox-node-api.yaml" theme={"system"}
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: space-sandbox-node-api
  namespace: sandboxes
spec:
  endpointSelector:
    matchLabels:
      app.kubernetes.io/name: space-sandbox
  egress:
    - toEntities:
        - host
      toPorts:
        - ports:
            - port: "9800"
              protocol: TCP
```

```bash theme={"system"}
kubectl apply -f sandbox-node-api.yaml
```

Without this policy, requests to create a sandbox time out with `timed out waiting for sandbox pod proxy to become reachable`. The policy also lets code that runs in a sandbox connect to that port on its Node.

### Prepare worker Nodes

SPACE's production node image sets up each worker before any SPACE Pod starts. CKS Nodes don't run that image, so on each worker you run the same setup that SPACE's Kind node image runs.

1. Open a root shell on the worker. Replace `[NODE-NAME]` with the worker's name:

   ```bash theme={"system"}
   kubectl debug node/[NODE-NAME] -it --profile=sysadmin --image=ubuntu:24.04 -- chroot /host bash
   ```

2. In the root shell, clone SPACE onto the Node's local disk at the same commit, and install the Firecracker binaries and guest kernel:

   ```bash theme={"system"}
   git clone https://github.com/perplexityai/SPACE.git /mnt/local/space-src
   cd /mnt/local/space-src
   git checkout 8be56e167a33c57d5b8dc9bbd74baf9ed06ddc09
   SPACE_VENDOR_ROOT=/space/vendor bash infra/space/kind/scripts/install-fc-vendor.sh
   ```

3. Install SPACE's node setup units and start them. They create SPACE's host accounts, the `/space` directory layout, the `space` cgroup, and a btrfs cache filesystem backed by an image file on the local disk. To change the cache image's 40 GiB size, first set `SPACE_CACHE_SIZE_MB` in `/etc/space/kind-node.env`.

   ```bash theme={"system"}
   install -D -m 0755 infra/space/kind/node/space-kind-node.sh /usr/local/lib/space/kind-node/space-kind-node.sh
   install -m 0644 scripts/lib/space-loop-devices.sh infra/space/identity/node-identities.sh /usr/local/lib/space/kind-node/
   install -m 0644 infra/space/kind/node/systemd/space-loop-nodes.service \
     infra/space/kind/node/systemd/space-cgroup.service \
     infra/space/kind/node/systemd/space-layout.service \
     infra/space/kind/node/systemd/space-cache.service /etc/systemd/system/
   mkdir -p /mnt/local/space
   ln -sfn /mnt/local/space/cache.img /var/lib/space-cache.img
   systemctl daemon-reload
   systemctl start space-loop-nodes space-cgroup space-layout space-cache
   ```

   The cache image is a sparse file. The cache unit logs a size warning that reads the link instead of the image. You can ignore this warning.

4. Build the shim with a Go toolchain on the local disk, and install it:

   ```bash theme={"system"}
   curl -fsSL https://go.dev/dl/go1.27.2.linux-amd64.tar.gz | tar -C /mnt/local -xz
   (cd shim && CGO_ENABLED=0 /mnt/local/go/bin/go build -trimpath -o ../containerd-shim-space-v2 .)
   bash infra/space/cluster/install-shim.sh --binary ./containerd-shim-space-v2
   ```

5. Register the `space` runtime with containerd, and restart it:

   ```bash theme={"system"}
   cat >> /etc/containerd/config.toml <<'EOF'

   [plugins."io.containerd.cri.v1.runtime".containerd.runtimes.space]
     runtime_type = "io.containerd.space.v2"
     pod_annotations = ["space.pplx.net/*"]
   EOF
   systemctl restart containerd
   ```

   This is the runtime section that `install-shim.sh` prints when containerd doesn't have one yet.

6. Exit the shell, and delete the debug Pod that `kubectl debug` printed when it started.

CKS clears a Node's root filesystem and its local disk under `/mnt/local` when the Node reboots. Repeat these steps after a worker reboots. Until you do, SPACE's node services on that worker fail to start.

## Build and publish the images

On the build host, clone SPACE at the same commit and build its images with its Kind build script. Then tag and push them. Replace `[REGISTRY]` with your registry and namespace, such as `registry.example.com/space`, and `[TAG]` with an image tag:

```bash theme={"system"}
bash infra/space/kind/scripts/build-images.sh --no-load all
for image in space-api space-data-plane space-cluster-controller space-worker \
    space-kind-key-broker space-seed-publish; do
  docker tag "$image:local" "[REGISTRY]/$image:[TAG]"
  docker push "[REGISTRY]/$image:[TAG]"
done
```

On a 160-core build host, the first build takes about 6 minutes.

The build also creates the SSH key pair that SPACE's seed template trusts, under `~/.space-devbox/kind/ssh/` on the build host. Copy `sandbox_ed25519` and `sandbox_ed25519.pub` from there into the SPACE checkout on your workstation. You need them to [create the sandbox SSH Secret](#create-the-secrets).

SPACE's charts don't set image pull Secrets, so the worker and infra Nodes must be able to pull from `[REGISTRY]` without one.

## Install the dependencies

SPACE needs PostgreSQL, S3-compatible object storage, and a key broker for volume encryption keys. SPACE's install path for existing clusters doesn't install them. For evaluation, install SPACE's own Kind charts for each one. They run on the infra Nodes.

1. Install PostgreSQL. The chart creates the `space-postgres` Secret that SPACE reads:

   ```bash theme={"system"}
   helm install space-postgres infra/space/kind/charts/space-postgres -n space \
     --set credentials.password="$(openssl rand -hex 16)"
   ```

2. Install the object store, with its data on the local disk. The chart creates the `templates` and `snapshots` buckets and the `space-object-store` Secret:

   ```bash theme={"system"}
   helm install space-object-store infra/space/kind/charts/space-object-store -n space \
     --set credentials.secretKey="$(openssl rand -hex 24)" \
     --set dataHostPath=/mnt/local/space-object-store
   ```

3. Install SPACE's test key broker under the names the install path accepts:

   ```bash theme={"system"}
   helm install space-key-broker infra/space/kind/charts/space-kind-key-broker -n space \
     --set image.repository=[REGISTRY]/space-kind-key-broker --set image.tag=[TAG] \
     --set service.name=space-key-broker \
     --set token.secretName=space-key-broker-token \
     --set token.value="$(openssl rand -hex 32)"
   ```

4. SPACE reaches its key broker only over HTTPS with HTTP/2, and the test broker serves plain gRPC. Create a certificate for a TLS proxy in front of it:

   ```bash theme={"system"}
   openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -nodes -days 365 \
     -subj /CN=space-key-broker-tls -keyout key-broker.key -out key-broker.crt \
     -addext "subjectAltName=DNS:space-key-broker-tls.space.svc.cluster.local" \
     -addext "basicConstraints=critical,CA:FALSE" -addext "extendedKeyUsage=serverAuth"
   kubectl -n space create secret tls space-key-broker-tls --cert=key-broker.crt --key=key-broker.key
   kubectl -n space create secret generic space-key-broker-ca --from-file=ca.crt=key-broker.crt
   ```

5. Run NGINX as the TLS proxy:

   ```yaml title="key-broker-tls.yaml" theme={"system"}
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: space-key-broker-tls
     namespace: space
   data:
     nginx.conf: |
       events {}
       http {
         server {
           listen 8443 ssl;
           http2 on;
           ssl_certificate /tls/tls.crt;
           ssl_certificate_key /tls/tls.key;
           location / {
             grpc_pass grpc://space-key-broker:50051;
           }
         }
       }
   ---
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: space-key-broker-tls
     namespace: space
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: space-key-broker-tls
     template:
       metadata:
         labels:
           app: space-key-broker-tls
       spec:
         nodeSelector:
           space.pplx.net/infra: "true"
         containers:
           - name: nginx
             image: nginx:1.29
             ports:
               - containerPort: 8443
             volumeMounts:
               - name: config
                 mountPath: /etc/nginx/nginx.conf
                 subPath: nginx.conf
               - name: tls
                 mountPath: /tls
                 readOnly: true
         volumes:
           - name: config
             configMap:
               name: space-key-broker-tls
           - name: tls
             secret:
               secretName: space-key-broker-tls
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: space-key-broker-tls
     namespace: space
   spec:
     selector:
       app: space-key-broker-tls
     ports:
       - port: 8443
         targetPort: 8443
   ```

   ```bash theme={"system"}
   kubectl apply -f key-broker-tls.yaml
   ```

## Create the Secrets

SPACE's install path checks that every Secret it references exists in the `space` namespace. The [install path README](https://github.com/perplexityai/SPACE/tree/8be56e167a33c57d5b8dc9bbd74baf9ed06ddc09/infra/space/cluster#secrets) lists each Secret and its keys. The dependency charts created some of them. Create the rest:

1. Create the internal tokens and the database role passwords:

   ```bash theme={"system"}
   kubectl -n space create secret generic space-internal \
     --from-literal=SPACE_INTERNAL_TOKEN="$(openssl rand -hex 32)" \
     --from-literal=SPACE_INTERNAL_CONTROL_TOKEN="$(openssl rand -hex 32)" \
     --from-literal=SPACE_PUBLIC_CURSOR_SECRET="$(openssl rand -hex 32)" \
     --from-literal=ecw-credential-key="$(openssl rand -hex 32)"
   kubectl -n space create secret generic space-db-roles \
     --from-literal=SPACE_DB_BOOTSTRAP_SUPERADMIN_PASSWORD="$(openssl rand -hex 16)" \
     --from-literal=SPACE_DB_BOOTSTRAP_USER_PASSWORD="$(openssl rand -hex 16)" \
     --from-literal=SPACE_DB_BOOTSTRAP_RO_PASSWORD="$(openssl rand -hex 16)" \
     --from-literal=SPACE_DB_BOOTSTRAP_MIGRATOR_PASSWORD="$(openssl rand -hex 16)" \
     --from-literal=SPACE_DB_BOOTSTRAP_CREDS_PASSWORD="$(openssl rand -hex 16)"
   ```

2. Create the key that signs sandbox route tokens, and its verification bundle:

   ```bash theme={"system"}
   openssl genpkey -algorithm ed25519 -out route-signing.pem
   openssl pkey -in route-signing.pem -pubout -out route-signing.pub.pem
   jq -n --rawfile pub route-signing.pub.pem \
     '{generation: 1, issuer: "space-route-authority", keys: [{key_id: "space-route-1", public_key_pem: $pub}]}' \
     > verification-bundle.json
   kubectl -n space create secret generic space-route-signing \
     --from-file=signing-key.pem=route-signing.pem \
     --from-literal=SPACE_API_ROUTE_ED25519_SIGNING_KEY_ID=space-route-1 \
     --from-literal=SPACE_API_ROUTE_ED25519_ISSUER=space-route-authority
   kubectl -n space create secret generic space-route-verification --from-file=verification-bundle.json
   ```

3. Create the sandbox SSH Secret from the key pair that the build created:

   ```bash theme={"system"}
   kubectl -n space create secret generic space-sandbox-ssh \
     --from-file=sandbox_ed25519 --from-file=sandbox_ed25519.pub
   ```

4. Issue the internal RPC TLS certificates with SPACE's Kind script. The script targets a kubeconfig context named `kind-[NAME]`, so create one that points at your cluster:

   ```bash theme={"system"}
   kubectl config set-context kind-cks \
     --cluster="$(kubectl config view --minify -o jsonpath='{.contexts[0].context.cluster}')" \
     --user="$(kubectl config view --minify -o jsonpath='{.contexts[0].context.user}')"
   SPACE_KIND_CLUSTER=cks bash infra/space/kind/scripts/internal-rpc-tls.sh
   ```

   The script creates the internal certificate authority and the service certificates in the `space` namespace.

## Install SPACE

With the dependencies and Secrets in place, install SPACE and publish its seed template:

1. Create a values file from SPACE's example. Replace `[SPACE-CLUSTER-NAME]` with a stable name for this SPACE cluster:

   ```bash theme={"system"}
   sed -e 's#registry.example.com/space#[REGISTRY]#g' \
     -e 's#"0.0.0-example"#"[TAG]"#g' \
     -e 's#example-cluster#[SPACE-CLUSTER-NAME]#g' \
     -e 's#environment: example#environment: evaluation#' \
     -e 's#https://object-store.example.com#http://object-store.space.svc.cluster.local:8333#g' \
     -e 's#https://key-broker.example.com:443#https://space-key-broker-tls.space.svc.cluster.local:8443#' \
     -e 's#urn:example:#urn:[SPACE-CLUSTER-NAME]:#g' \
     -e 's#dataPlanePublicUrl: ""#dataPlanePublicUrl: http://127.0.0.1:8090#' \
     infra/space/cluster/values.example.yaml > space-values.yaml
   ```

   The changes point SPACE at your images, the in-cluster object store, and the key broker proxy. SPACE scopes Node identities to the cluster name, so don't change it after you install. `dataPlanePublicUrl` is the data-plane address that clients use. This guide reaches the data plane through a port forward.

2. Install both SPACE releases:

   ```bash theme={"system"}
   infra/space/cluster/install.sh -f space-values.yaml --kube-context "$(kubectl config current-context)"
   ```

   The script checks the namespaces, Secrets, and RuntimeClass, and runs the database migrations. It then installs two Helm releases. The `space` release contains the API services and the worker node services. The `space-builder` release contains the template builder services, which you need only to build custom templates. This guide doesn't cover custom templates, so it creates no Nodes labeled `space.pplx.net/node-pool: builder`, and the `space-builder` release runs no Pods.

3. Publish the seed template. The internal API accepts template publishing only from the `space-template-publish` ServiceAccount, so render the chart with the release name `space`:

   ```bash theme={"system"}
   helm template space infra/space/kind/charts/space-seed-publish -n space \
     --set image.repository=[REGISTRY]/space-seed-publish --set image.tag=[TAG] \
     --set s3.endpoint=http://object-store.space.svc.cluster.local:8333 \
     | kubectl apply -f -
   kubectl -n space wait --for=condition=complete job/space-seed-publish --timeout=10m
   ```

### Verify the deployment

Check that every Pod in the `space` namespace is `Running` and ready, or `Completed`:

```bash theme={"system"}
kubectl -n space get pods
```

Check that each worker advertises sandbox capacity:

```bash theme={"system"}
kubectl get nodes -l space.pplx.net/node-pool=sandbox \
  -o custom-columns='NODE:.metadata.name,SLOTS:.status.allocatable.space\.pplx\.net/network-slots'
```

```text title="Example output" theme={"system"}
NODE               SLOTS
[NODE-NAME]        300
```

If a worker's `SLOTS` column is empty, the worker isn't ready for sandboxes. Check its `space-node-manager` Pod.

## Create a first sandbox

To confirm that SPACE works end to end, sign in to its API from your workstation and run SPACE's first-sandbox example:

1. Set the password of SPACE's `root@local` admin user with SPACE's Kind script, through the `kind-cks` context:

   ```bash theme={"system"}
   openssl rand -hex 16 > admin-password
   SPACE_KIND_CLUSTER=cks SPACE_CONSOLE_PASSWORD="$(cat admin-password)" \
     bash infra/space/kind/scripts/provision-local-console.sh
   ```

2. Forward the API and data-plane ports to your workstation:

   ```bash theme={"system"}
   kubectl -n space port-forward svc/space-api-entry 8080:8080 >/dev/null &
   kubectl -n space port-forward svc/space-data-plane-entry 8090:8090 >/dev/null &
   export SPACE_API_URL=http://127.0.0.1:8080
   export SPACE_DATA_PLANE_URL=http://127.0.0.1:8090
   ```

3. Sign in and save a session token:

   ```bash theme={"system"}
   export SPACE_API_TOKEN=$(jq -n --rawfile password admin-password \
     '{email: "root@local", password: ($password | rtrimstr("\n"))}' \
     | curl -fsS -H 'Content-Type: application/json' --data-binary @- "$SPACE_API_URL/auth/v1/sessions" \
     | jq -r '.token')
   ```

4. Run SPACE's first-sandbox example:

   ```bash theme={"system"}
   python3 examples/first_sandbox.py
   ```

   The example uses only the Python standard library. It creates a sandbox from `seed:latest`, runs a command, and asks whether to delete the sandbox. The output includes `Hello from SPACE` and `Command completed successfully`.

To keep working with the API, see [Your first sandbox](https://space.docs.perplexity.ai/guide/first-sandbox.html) and the rest of the SPACE documentation.

## Limitations

This deployment has the following limitations:

* **Evaluation only.** The test key broker isn't designed to secure encryption keys, and the dependencies run as single replicas.
* **`amd64` workers only.**
* **No state across Node reboots.** CKS clears Node local disks on reboot. After a worker reboots, prepare it again. After an infra Node reboots, the object store loses its data, and so does PostgreSQL on a local-path volume, so [uninstall](#uninstall-space) and reinstall SPACE.
* **In-cluster object storage.** SPACE can't use CoreWeave AI Object Storage, so this deployment uses SPACE's in-cluster object store.
* **No template builds or web console.** This guide publishes only the `seed` template, and SPACE's install path doesn't include its UI.

## Troubleshoot

| Symptom | Cause and fix |
| - | - |
| `space-node-manager` fails with `Unit space-cgroup.service not found`. | The worker wasn't prepared, or it rebooted. [Prepare the worker](#prepare-worker-nodes) again. |
| Requests to create a sandbox time out with `timed out waiting for sandbox pod proxy to become reachable`. | The `space-sandbox-node-api` CiliumNetworkPolicy is missing. [Apply the policy](#allow-sandbox-pods-to-reach-their-node-services). |
| `install.sh` fails with `values are incomplete`. | A required value in `space-values.yaml` still has its example value. The error lists each one. Replace each listed value in `space-values.yaml`. |
| `install.sh` reports a missing Secret. | Create the Secret named in the error, as described in [Create the Secrets](#create-the-secrets). |
| `space-node-manager` logs `default network interface is loopback` every 30 seconds. | Cilium adds a default route through the loopback interface in one of its routing tables, and SPACE reads it. Sandboxes still work, so you can ignore this message. |

For SPACE API errors, see [Troubleshooting](https://space.docs.perplexity.ai/guide/troubleshooting.html) in the SPACE documentation.

## Uninstall SPACE

Delete the SPACE resources:

```bash theme={"system"}
helm -n space uninstall space-builder space space-key-broker space-object-store space-postgres
kubectl delete namespace space sandboxes
kubectl delete runtimeclass space
```

Then [reboot](https://docs.coreweave.com/products/cks/nodes/reboot.md) each worker Node. The reboot removes the shim, the containerd change, the files under `/mnt/local`, and the processes, cgroups, and network namespaces that SPACE leaves on the Node. Without a reboot, a reinstall fails until you remove them manually.

On your workstation, stop the port forwards and remove the kubeconfig context that the SPACE scripts used:

```bash theme={"system"}
pkill -f 'port-forward svc/space-'
kubectl config delete-context kind-cks
```
