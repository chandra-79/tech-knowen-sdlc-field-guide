from author import *
add('images','ckad','Build and inspect container images','Design and build','Make a reproducible artifact before asking Kubernetes to run it.',
'''An image is a read-only filesystem and execution configuration. A running container adds a writable layer and processes. An image tag is a movable name; a digest identifies content. A Dockerfile describes a build, while a Kubernetes manifest describes how an image runs.

Use a small build context, exclude credentials with .dockerignore, and separate build tools from runtime files when appropriate. Never put a real secret in a build argument or image layer and assume deleting it in a later layer erases history.''',
'''The image architecture must match the node or support that platform through a multi-platform manifest. A local image exists in the laptop engine, not automatically in kind’s inner container runtime. kind load docker-image copies it into the cluster nodes; a remote registry is another distribution path.

Kubernetes uses imagePullPolicy to decide when to resolve or pull. Changing the policy does not repair a nonexistent image name, denied registry credentials or incompatible CPU architecture. For production, rebuild patched dependencies, scan the artifact and promote an immutable digest. A scan is evidence about known issues, not proof that code is safe.''',
'Package the bank information page as tk-bank-web:1. Replace the page with a clear version marker so a rollout can be observed without a real transaction.',
[('Source','HTML and Dockerfile'),('Build artifact','Image with a content identity'),('Node runtime','Pull or load, then execute')],
'Create index.html containing a fictional bank heading and use the Dockerfile below. Run docker build -t tk-bank-web:1 ., inspect the image, and run kind load docker-image tk-bank-web:1 --name techknowen-course. Deploy it in a separate namespace; the starter bank ConfigMap would otherwise hide the image’s page.',
'Fetch the page from the separate workload and compare the visible marker. Inspect imageID in Pod status and distinguish it from the desired image tag.',
'Use a missing tag and inspect ImagePullBackOff and Events. Restore the real image; avoid repeatedly deleting the Pod without fixing the image reference.',
('Does changing a tag in a registry necessarily restart existing Pods?','No. Running Pods are not automatically replaced merely because the tag points elsewhere. Roll out an explicit immutable version.'),['concepts/containers/images/','https://docs.docker.com/build/concepts/dockerfile/'],code='FROM nginx:1.27-alpine\nCOPY index.html /usr/share/nginx/html/index.html\nEXPOSE 80',prereq='Setup complete; a separate image-lab namespace. Dockerfile is not Kubernetes YAML.')
add('pod-design','ckad','Pods, commands and container lifecycle','Design and build','Choose what must live together and what should scale separately.',
'''Containers in a Pod share its network namespace and can communicate over localhost. They share files only through explicitly mounted volumes. A Pod is scheduled as a unit; adding containers is not a way to create independently scalable services.

Kubernetes command and args override image execution defaults. Shell operators such as pipes require an explicit shell; an exec-form command is not automatically interpreted as shell syntax. A process should handle termination and write useful output to stdout/stderr.''',
'''Pod phase, container state and readiness are different. Running can contain an unhealthy or restarting container. CrashLoopBackOff describes restart backoff shown by tooling, not a Pod phase. The same Pod may restart a container, while a controller can create a different Pod after deletion.

During termination, graceful shutdown and traffic draining must work together. A preStop hook consumes the termination grace period; it does not provide extra time beyond it. An application must stop accepting new work and complete or safely retry in-flight work. A forced kill can interrupt processing despite a healthy-looking deployment history.''',
'A future bank API and its separate notification service should not share one Pod merely because both belong to banking. A tightly coupled file-transform helper may be a reasonable Pod companion.',
[('Pod boundary','Shared network and scheduling fate'),('Main process','Handle requests and termination'),('Mounted volume','Explicitly share selected files')],
'Create a short-lived busybox Pod with --restart=Never and a command that prints a marker. Inspect its phase, exit code and logs. Compare it with the long-running bank-web Pod.',
'The short task reaches Succeeded after exit code 0. You can identify which command was run and why it should not be deployed as an endlessly restarted server.',
'Change exit 0 to exit 7 in a new Pod. Inspect terminated state instead of treating every non-running Pod as a network issue.',
('Is CrashLoopBackOff one of the official Pod phases?','No. It is a waiting reason/backoff symptom. Inspect container state, last termination and logs to find the underlying cause.'),['concepts/workloads/pods/','concepts/workloads/pods/pod-lifecycle/','concepts/containers/container-lifecycle-hooks/'],code='kubectl -n tk-bank run one-task --image=busybox:1.37 --restart=Never -- sh -c "echo bank-check; exit 0"\nkubectl -n tk-bank logs one-task\nkubectl -n tk-bank get pod one-task -o yaml\nkubectl -n tk-bank delete pod one-task')
add('init-sidecars','ckad','Init containers and native sidecars','Design and build','Give preparation and continuous support different lifecycle rules.',
'''A regular init container completes before the main application starts. It can create a file or wait for a prerequisite, but a permanently failing init prevents startup. A sidecar provides continuing support, such as a local proxy or file consumer.

Native sidecars are expressed as initContainers with restartPolicy: Always. They start in init ordering but continue alongside application containers. Do not confuse this with an ordinary init container or with a second app container in the containers list.''',
'''A startup probe on a native sidecar can gate progression through startup. A readiness probe can affect the readiness of the whole Pod. Native sidecars have lifecycle handling designed for orderly startup/shutdown and do not keep a Job from completing after its main containers finish.

Shared emptyDir data lasts for the Pod lifetime, not forever. Retrying an init must be safe: writing a file atomically is easier to reason about than applying a non-idempotent database migration on every restart. For migrations, use a deliberately coordinated process with locking and rollback planning.''',
'A bank information Pod receives a generated learning page from an init container. A later experiment adds a support container that reads the same shared volume.',
[('Init','Generate a page, then exit'),('Application','Serve the prepared file'),('Sidecar','Continue support alongside the app')],
'Apply init.yaml from the manifest library. Inspect initContainerStatuses, then fetch the page. Change the init command to exit 1 in a copied manifest and observe that the application cannot start; restore the successful command.',
'The init exits 0 before nginx serves the file. Explain which volume makes the file visible to both containers and what deletion of the Pod loses.',
'A helper runs forever as a regular init container. Correct the lifecycle design rather than lengthening a readiness timeout.',
('Why can an ordinary long-running init block the main container?','The kubelet waits for regular init containers to complete successfully before starting the application containers.'),['concepts/workloads/pods/init-containers/','concepts/workloads/pods/sidecar-containers/'],code='@lab:init.yaml')
add('workload-choice','ckad','Choose Deployment, DaemonSet or StatefulSet','Design and build','The controller should express the workload’s actual identity and placement needs.',
'''A Deployment manages interchangeable replicas. A DaemonSet places a Pod on eligible nodes, making it useful for node-local agents. A StatefulSet gives stable ordered identities and can connect each replica with its own persistent claim.

Stable identity does not implement database replication. A StatefulSet can preserve a name while the application still needs quorum, backup, leader election or recovery logic. Choose the simplest resource that satisfies the real workload.''',
'''Deployments use ReplicaSets to manage revisions and counts. DaemonSet eligibility depends on node selection and scheduling constraints; it is not a promise of exactly one Pod on every possible machine. StatefulSets normally use a headless Service for stable network identity and have different update and ordering controls.

Deleting a Pod is a useful failure experiment, but deleting storage is a different, potentially destructive operation. Claims and volumes have their own lifecycle. Read retention and reclaim settings before attempting cleanup. Separate disposable lab records from a real database before experimenting.''',
'bank-web is stateless and fits a Deployment. A node log collector fits a DaemonSet. A replicated database requires a deliberate stateful design and may be managed outside the cluster.',
[('Interchangeable web','Deployment replicas'),('Node-local collector','DaemonSet placement'),('Stable replica identity','StatefulSet plus storage design')],
'Inspect the running bank Deployment and the kube-system DaemonSets using read-only commands. Record desired/current/ready counts and explain which nodes are eligible. Design a three-replica database identity table without claiming that three Pods equal a functioning database.',
'You can justify each controller and identify the additional application-level replication requirement for a database.',
'A team uses three independent database Pods behind a Service without replication. Explain why requests could observe unrelated datasets.',
('Does StatefulSet make a database highly available by itself?','No. It supplies workload identity and ordering primitives. The database must implement and be configured for replication and failure handling.'),['concepts/workloads/controllers/deployment/','concepts/workloads/controllers/daemonset/','concepts/workloads/controllers/statefulset/'],kind='architecture',code='kubectl -n tk-bank describe deployment bank-web\nkubectl -n kube-system get daemonsets\nkubectl explain statefulset.spec.volumeClaimTemplates')
add('jobs','ckad','Jobs and CronJobs without duplicate surprises','Design and build','Completion-based work needs explicit retry and concurrency rules.',
'''A Job manages work that should finish. A CronJob creates Jobs on a schedule. A schedule is not a guarantee of precisely one business execution at a precise instant. Restarts, retries and controller conditions can cause missed or repeated work.

Set a retry budget and consider a deadline. Forbid on a CronJob avoids overlapping Jobs from that same CronJob, but it is not a global lock across other producers. Keep successful and failed history small enough to inspect without accumulating forever.''',
'''backoffLimit limits failed Job attempts; activeDeadlineSeconds limits elapsed execution time. completions and parallelism answer different questions: how much successful work is required versus how many Pods may work simultaneously. Work partitioning still belongs to your application.

For a financial reconciliation job, record a business operation key and make repeat processing harmless. An HTTP timeout might occur after the downstream write committed. Blindly retrying a transfer could duplicate an effect even if the Kubernetes Job eventually shows Complete.''',
'The course reconciliation Job prints a fictional total and exits. A real reconciliation design would compare immutable records and record which reporting period was processed.',
[('Schedule','CronJob creates an execution'),('Job','Retry within a defined budget'),('Business record','Deduplicate the reporting period')],
'Apply jobs.yaml. Wait for the one-off Job to complete and inspect its logs. Create an immediate Job from the CronJob, rather than waiting for its schedule, then compare Job ownership and results.',
'Both tasks finish and log the expected marker. Explain why two successful logs are not proof of exactly-once financial processing.',
'Make a copied Job exit 1 with backoffLimit: 1. Inspect the failed Pods and final condition, then delete that named experiment.',
('Does concurrencyPolicy: Forbid prevent all duplicate business processing?','No. It limits overlap for that CronJob. Application-level deduplication remains necessary.'),['concepts/workloads/controllers/job/','concepts/workloads/controllers/cron-jobs/'],code='@lab:jobs.yaml')
add('configuration','ckad','ConfigMaps and configuration rollout','Environment and security','Keep environment-specific values separate from the image.',
'''A ConfigMap carries non-secret configuration. A container can consume values as environment variables, arguments or mounted files. The application must know how to read them; Kubernetes does not automatically change application behaviour merely because a key exists.

A mounted directory can receive eventual updates, but a process may cache what it read. Environment variables do not change in a running process. A subPath mount does not receive the normal projected-volume updates. Choose a reload or rollout strategy deliberately.''',
'''The bank page is projected from a ConfigMap directory. An updated key can become visible without rebuilding nginx. A deployment that reads a database host once during startup may instead require replacement Pods. Use versioned configuration names or a Pod-template checksum when you need a reviewable rollout trigger.

Configuration should be validated before release. A syntactically valid URL can still target the wrong environment. Record the intended config version alongside the image version and keep a compatible rollback combination. Reverting only the image may not restore previous behaviour.''',
'Change the learning page’s heading in bank.yaml. Observe file projection separately from Pod restart; record both the response and Pod UID.',
[('ConfigMap','Non-secret values'),('Delivery choice','Environment or mounted files'),('Application','Reload or restart deliberately')],
'Edit only index.html in the starter ConfigMap and reapply bank.yaml. Repeatedly fetch the page until it changes. Then inspect the container environment and explain why projected files and environment variables differ.',
'The page eventually changes while the Pod identity can remain the same. Do not claim an immediate update deadline from this one observation.',
'Reference a missing ConfigMap key in a copied Pod. Diagnose the configuration error from Events instead of changing the Service.',
('Will an updated ConfigMap automatically rewrite an existing process environment?','No. Environment variables are set when the container starts; replace or restart through the workload strategy.'),['concepts/configuration/configmap/','tasks/configure-pod-container/configure-pod-configmap/'],code='kubectl -n tk-bank get configmap bank-page -o yaml\nkubectl apply -f bank.yaml\nkubectl -n tk-bank get pods -l app=bank-web -o wide')
add('secrets','ckad','Secrets, identity and credential boundaries','Environment and security','Encoding is not encryption, and reading permission is security-sensitive.',
'''A Secret is an API object for sensitive values. Base64 encodes bytes for representation; anyone who can read the encoded value can decode it. Protect API access, storage encryption, audit exposure and the application’s handling of credentials.

Use fictional values in labs. Avoid placing real credentials in committed manifests, terminal history, screenshots or logs. A Secret mounted in a Pod becomes accessible to the processes that can read that mount; the object type alone does not make the process trustworthy.''',
'''Secret changes delivered through mounted volumes are eventual and still require application reload behaviour. Environment-based consumption requires a new process. imagePullSecrets authenticate image pulls, while a ServiceAccount identifies an application to the Kubernetes API; neither is a universal application login.

Short-lived workload identity reduces reliance on long-lived keys in cloud environments. In GKE, Workload Identity Federation connects Kubernetes workload identity to Google Cloud authorization. That relationship does not replace Kubernetes RBAC or automatically grant database-level access.''',
'A fictional report worker reads a dummy token from a mounted file. Its check prints only the file’s byte count, never the token value.',
[('Secret object','Restrict API access'),('Projected file','Mount only where needed'),('Application','Avoid logging the value')],
'Create a dummy Secret and apply secret-reader.yaml. Inspect logs to verify the file exists without printing its contents. Review who can get Secrets with kubectl auth can-i.',
'The worker prints a positive byte count. Explain why this demonstrates mounting, not encryption at rest or proper production access control.',
'Change the Secret name in the Pod to a nonexistent name; inspect the mount/configuration event and restore it.',
('Does base64 protect a leaked Secret from a reader?','No. Base64 is reversible encoding. Access controls and encryption address different parts of the exposure.'),['concepts/configuration/secret/','concepts/security/secrets-good-practices/'],code='@lab:secret-reader.yaml')
add('resources','ckad','Requests, limits, quotas and OOM','Environment and security','Separate scheduling promises from runtime constraints.',
'''Requests inform scheduling and resource sharing; limits constrain runtime consumption where supported. CPU is compressible: a CPU limit can throttle execution. Exceeding a memory limit can lead to an OOM kill. A request is not an instruction to continuously consume that quantity.

ResourceQuota limits aggregate namespace usage or object counts. LimitRange can supply defaults and validate per-object values. A rejected API request, a Pending Pod and a killed container indicate different enforcement points.''',
'''100m CPU is one tenth of a CPU unit. 128Mi is a binary memory quantity. Read units carefully: confusing memory suffixes can produce absurdly small or large requests. Scheduling uses requests and placement constraints, not simply the current output of top.

A large request can leave a Pod Pending on a mostly idle cluster because the scheduler reserves capacity against declared requests. A tiny memory limit may start successfully and fail only under traffic. Measure representative startup and steady-state behaviour before selecting settings; limits are neither capacity planning nor protection against all noisy-neighbour effects.''',
'bank-web starts with modest explicit requests and limits. A controlled copy requests 100 CPUs to make the scheduling failure obvious without allocating them.',
[('Admission','Quota and limit validation'),('Scheduler','Place using requests'),('Runtime','CPU throttling or memory enforcement')],
'Inspect requests and limits in bank.yaml. Create pending.yaml from the library; describe it and read the FailedScheduling event. Delete only the pending experiment afterward.',
'The oversized Pod stays Pending with an insufficient CPU explanation. No successful application process should be inferred from API acceptance.',
'A container reports OOMKilled. Compare lastState, limits and application memory evidence before merely raising the limit.',
('Why can a Pod remain Pending while top shows idle CPUs?','Placement is based on requests and constraints, not just instantaneous measured utilization.'),['concepts/configuration/manage-resources-containers/','concepts/policy/resource-quotas/','concepts/policy/limit-range/'],code='@lab:pending.yaml')
add('identity-rbac','ckad','Authentication, RBAC and ServiceAccounts','Environment and security','Identify a caller, authorize an action, then evaluate admission rules.',
'''Authentication answers who the caller is. Authorization asks whether that identity may perform a verb on a resource in a scope. Admission evaluates an authorized request before accepting certain changes. A valid identity can still receive Forbidden.

A ServiceAccount is a Kubernetes workload identity. A Role defines permissions in a namespace; a RoleBinding grants permissions to a subject. A ClusterRole can describe broader permissions and can also be bound within a namespace. Avoid using cluster-admin as a generic application fix.''',
'''RBAC grants are additive: an extra broad binding can allow an operation despite a carefully narrow Role elsewhere. There is no ordinary RBAC deny rule that subtracts that grant. Inspect effective permissions rather than only one YAML file.

A mounted projected ServiceAccount token is not a user password or Google Cloud service-account key. Disable automatic token mounting for workloads that do not need API access. Admission security policies can still reject a Pod even when a caller is allowed to create Pods. Keep identity, API permission and workload security diagnosis separate.''',
'A bank status reader needs get/list/watch on Pods in tk-bank, not permission to read customer credentials or alter all namespaces.',
[('Authenticate','Which identity called?'),('Authorize','Can it get Pods here?'),('Admit','Does this change satisfy policies?')],
'Apply rbac.yaml. Use auth can-i with the supplied ServiceAccount identity to test get Pods and get Secrets. Impersonation for this local test requires the lab administrator context; a normal learner may not have that right.',
'Pod read is yes; Secret read is no. Explain why a RoleBinding subject namespace and the resource namespace are distinct fields.',
'Bind the Role to the wrong ServiceAccount name in a copy. Diagnose Forbidden by inspecting subjects and roleRef rather than granting cluster-admin.',
('Can a RoleBinding itself contain permission rules?','No. It associates subjects with a referenced Role or ClusterRole; the referenced role contains the rules.'),['reference/access-authn-authz/rbac/','concepts/security/service-accounts/','reference/access-authn-authz/admission-controllers/'],code='@lab:rbac.yaml')
add('security-context','ckad','Run with a deliberate security context','Environment and security','Reduce process privilege while preserving the files and ports the app needs.',
'''A securityContext controls aspects of a Pod or container’s execution. Running as a non-root user, preventing privilege escalation and dropping capabilities limit what a compromised process can do. A read-only root filesystem blocks writes there, but applications may still need explicitly mounted writable directories.

Pod Security Admission evaluates workload settings against policy levels. It is an admission mechanism, not an antivirus or runtime network firewall. Security settings must be compatible with the image and its expected UID, paths and port.''',
'''Capabilities split some privileged operations into specific permissions. Adding all capabilities defeats a narrow design. allowPrivilegeEscalation: false prevents gaining more privileges through mechanisms such as setuid; it does not revoke privileges already granted. seccompProfile: RuntimeDefault requests the runtime’s default syscall filter.

An application can be non-root and still read every credential mounted into its filesystem. Reduce identity permissions and mounts too. A failing read-only-root experiment should lead to inspection of writable paths, not immediate removal of every security setting.''',
'The security demonstration is a small busybox process that writes only to /work on emptyDir, rather than forcing the original nginx image into incompatible settings.',
[('Admission policy','Check acceptable Pod settings'),('Container identity','UID, capabilities and seccomp'),('Filesystem','Read-only root; explicit /work volume')],
'Apply security.yaml, inspect the process identity and the successful /work output in logs. Attempt a write to an unmounted root path using a copied command and record the permission failure.',
'The container uses the declared nonzero UID and writes only to its mounted writable path. Keep the restrictive settings in the corrected configuration.',
'runAsNonRoot is set but the image defaults to UID 0. Choose a compatible image or explicit valid UID; do not call the rejection a scheduling failure.',
('Does non-root execution remove the need for least-privilege API access?','No. Process privilege and API authorization protect different boundaries.'),['tasks/configure-pod-container/security-context/','concepts/security/pod-security-standards/','concepts/security/pod-security-admission/'],code='@lab:security.yaml')
add('storage','ckad','Volumes, PVCs and persistence','Design and build','Know which deletion or restart destroys which data.',
'''A container writable layer is ephemeral. emptyDir survives a container restart inside a Pod but is deleted with the Pod. A PersistentVolumeClaim asks for storage with a size, access mode and optionally a StorageClass. A PersistentVolume represents the supplied storage resource.

A PVC is not a backup. A bound claim does not prove that application data is consistent or recoverable. Storage access modes describe supported mounting constraints, not database transaction isolation or filesystem permissions.''',
'''Dynamic provisioning uses a StorageClass and its provisioner. WaitForFirstConsumer delays binding/provisioning until scheduling context is known, which matters for zonal storage. An immediate expectation that every new PVC must already be Bound can therefore misdiagnose healthy behaviour.

ReadWriteOnce means read/write mounting by one node, not universally one Pod. ReadWriteOncePod has a different single-Pod intent and requires compatible CSI support. A Delete reclaim policy can remove backing storage when a claim is removed. Inspect lifecycle settings before deleting a stateful lab.''',
'Write a harmless learning marker to a PVC, delete only the consumer Pod, and recreate it against the same claim. The marker should survive that specific event.',
[('PVC','Request capacity and access mode'),('PV / provisioner','Bind a suitable backing volume'),('Pod mount','Read and write the persistent path')],
'Apply storage.yaml. Write a marker, delete the named consumer Pod and reapply the file. Read the marker from the replacement. Keep the PVC until the observation is complete.',
'The new Pod has a different UID while the marker remains. Record StorageClass and reclaim policy; do not extrapolate this into a tested disaster-recovery guarantee.',
'If Pending, check whether a default class/provisioner exists and whether binding waits for a consumer. Investigate node/zone constraints before replacing data.',
('Does a surviving PVC prove a backup can be restored?','No. Persistence through Pod replacement and independently verified backup recovery are different properties.'),['concepts/storage/volumes/','concepts/storage/persistent-volumes/','concepts/storage/storage-classes/'],code='@lab:storage.yaml')
add('probes','ckad','Startup, readiness and liveness probes','Observability and maintenance','Ask three different health questions instead of using one endpoint for everything.',
'''Startup asks whether initialization has completed. While a startup probe has not succeeded, liveness and readiness probes are held back. Readiness controls eligibility for normal Service traffic. Liveness can trigger a container restart after repeated failures.

A dependency outage is not always a reason to restart your application. If every instance restarts because a shared database is briefly unavailable, you may amplify the incident. Choose endpoints and thresholds based on what corrective action is useful.''',
'''The probe target runs from the node’s perspective for HTTP/TCP probes; reaching localhost from your browser proves a different route. Named ports and application listen addresses must agree. A probe may succeed while a business endpoint fails, so end-to-end tests remain necessary.

For approximate startup tolerance, reason from periodSeconds and failureThreshold, then account for probe timing rather than treating their product as a precise SLA. Readiness recovery is asynchronous through endpoint updates and traffic paths. It is not an instantaneous global traffic switch.''',
'bank-web readiness checks the served page and liveness checks nginx. A copied Deployment with a nonexistent readiness path becomes unready while its process continues running.',
[('Startup','Has initialization finished?'),('Readiness','Should this replica receive traffic?'),('Liveness','Would restarting this process help?')],
'Inspect the starter probes. In a separate copied workload, set readiness path to /missing. Observe Running with Ready false, then correct it. Do not intentionally break the primary bank service while other labs depend on it.',
'The container can be Running while the Pod is unready. Inspect EndpointSlice readiness and explain the different effects of failing liveness versus readiness.',
'A slow-starting service is killed repeatedly by an aggressive liveness probe. Add a justified startup probe and verify startup behaviour rather than simply disabling health checks.',
('Does a readiness failure automatically restart the container?','No. It marks readiness false. Liveness/startup failure thresholds can cause restarts.'),['tasks/configure-pod-container/configure-liveness-readiness-startup-probes/','concepts/workloads/pods/pod-lifecycle/'],code='kubectl -n tk-bank get pods\nkubectl -n tk-bank describe deployment bank-web\nkubectl -n tk-bank get endpointslices -l kubernetes.io/service-name=bank-web -o yaml')
add('debugging','ckad','Debug from symptoms to evidence','Observability and maintenance','Use status, Events, logs and a request test in a repeatable order.',
'''Start by naming the symptom: not scheduled, image not pulled, process exits, unready, or unreachable through a Service. Each symptom points to a different layer. get gives a summary; describe supplies conditions and Events; logs exposes process output; exec tests inside a running container.

Use logs --previous when the prior container instance crashed. Select the container with -c when a Pod has several. A missing shell in a minimal image is expected and does not prove the application is broken.''',
'''Ephemeral debug containers can help when a production image lacks tools, subject to permissions and runtime support. They alter the Pod’s diagnostic state and should be used deliberately. Debug access may expose memory, mounted secrets or network access, so it is a privileged operational capability.

Events are temporary observations, not a durable audit history. Standard output is not automatically retained after every deletion. Production logging needs collection, retention and access controls. Record timestamps, object UID, recent changes and the smallest reproduction before changing multiple variables.''',
'Inject a wrong Service selector, a nonexistent image and a wrong readiness path in separate disposable experiments. Each should produce a different diagnosis and repair.',
[('Symptom','Pending, crashing, unready or unreachable?'),('Evidence','Conditions, Events, logs and endpoints'),('Repair','Change one cause, then repeat the request')],
'Use the provided triage commands against bank-web. Then create a new busybox Pod that exits 7. Find its exit code and logs. Explain how the evidence differs from an image pull failure.',
'Your incident note includes a symptom, evidence, causal hypothesis, one correction and a repeated acceptance check.',
'A page is unreachable but Pods are Ready. Inspect Service selector, ports, EndpointSlices and client path before restarting every Pod.',
('What does logs --previous retrieve?','The previous terminated container instance’s logs when available, not a complete historical archive of all deleted Pods.'),['tasks/debug/debug-application/','tasks/debug/debug-application/debug-running-pod/','concepts/cluster-administration/logging/'],code='kubectl -n tk-bank get pods -o wide\nkubectl -n tk-bank get events --sort-by=.metadata.creationTimestamp\nkubectl -n tk-bank logs deployment/bank-web --tail=30\nkubectl -n tk-bank get service,endpointslices\nkubectl -n tk-bank describe deployment bank-web')
add('services-dns','ckad','Services, DNS and the packet path','Services and networking','A stable name selects changing endpoints; it is not the application itself.',
'''A ClusterIP Service provides stable in-cluster access to selected endpoints. port is the Service-facing port; targetPort is the backend port. containerPort documents a container port but does not make a process listen or expose it externally.

DNS normally resolves a Service name inside the cluster. A short name uses the caller’s namespace search path. bank-web.tk-bank.svc.cluster.local is a typical fully qualified name when the cluster domain is cluster.local; clusters can choose a different domain.''',
'''EndpointSlices represent backend addresses and conditions. kube-proxy or an alternative data plane programs forwarding; the Service is not necessarily a standalone proxy process. Implementations may use iptables, IPVS or eBPF mechanisms. Avoid drawing the API server in every customer request path.

NodePort exposes a port through node networking; LoadBalancer asks an integration to provide external load balancing. A local kind cluster does not automatically supply a cloud load balancer. A pending external address may reflect missing integration rather than a failed Pod. Port-forward is a development access mechanism, not proof of production ingress.''',
'A client Pod reaches bank-web through cluster DNS while your laptop uses port-forward. Compare the two paths rather than assuming they test identical networking.',
[('Client Pod','Resolve Service DNS'),('Service routing','Select ready EndpointSlice backends'),('Web Pod','Listen on targetPort 80')],
'Run a disposable busybox client to fetch http://bank-web.tk-bank.svc.cluster.local. Inspect Service ports and EndpointSlices. Then deliberately change a copied Service targetPort and compare the resulting connection failure.',
'The client receives the page through Service DNS. The selected addresses match the intended Pods, and the backend port matches the application listener.',
'Correct DNS but no response: inspect endpoints and targetPort before editing CoreDNS. No endpoints: inspect selector and readiness first.',
('Does declaring containerPort: 80 start an HTTP server?','No. The process in the image must actually listen. The declaration alone neither starts it nor exposes it outside the Pod.'),['concepts/services-networking/service/','concepts/services-networking/dns-pod-service/','concepts/services-networking/endpoint-slices/'],kind='architecture',code='kubectl -n tk-bank run client --image=busybox:1.37 --restart=Never -- wget -qO- http://bank-web.tk-bank.svc.cluster.local\nkubectl -n tk-bank logs client\nkubectl -n tk-bank delete pod client\nkubectl -n tk-bank get service bank-web -o yaml')
add('network-policy','ckad','NetworkPolicy and explicit reachability tests','Services and networking','A policy document is effective only when the network implementation enforces it.',
'''NetworkPolicy selects Pods and allows specified ingress or egress traffic. Policies are additive. Once a Pod is isolated for a direction, the permitted traffic is the union of applicable allow rules. Source egress and destination ingress must both allow a connection when both ends are isolated.

A namespaceSelector and podSelector in one peer entry combine conditions. Separate peer entries are alternatives. Empty selectors and empty rule lists have different meanings; read the YAML structure carefully.''',
'''DNS is often the first dependency accidentally blocked by default-deny egress. Permit the correct DNS destination and protocols for your cluster, then test name resolution separately from application access. A policy can select Pods by namespace labels without making namespace names a built-in security boundary.

The basic kind setup’s default networking is not a NetworkPolicy enforcement lab. Use a documented compatible CNI such as Calico or Cilium in a separate policy-capable cluster. An API server accepting the object is not evidence of enforcement. Record allowed and denied requests from distinct clients, and check plugin-specific behaviour.''',
'Only a labelled bank frontend should reach the backend’s web port; an unlabelled diagnostic client should be denied. The outcome must be tested in an enforcing environment.',
[('Client egress','Source must permit the destination'),('Policy boundary','Match namespace, labels and port'),('Server ingress','Destination must permit the source')],
'Inspect policy.yaml and predict the result for a labelled and an unlabelled client. In a policy-enforcing cluster, apply it and run both request tests with timeouts. In basic kind, stop at schema inspection and record enforcement as not tested.',
'Collect one allowed request and one denied request plus CNI identity. API creation alone does not satisfy this lab.',
'A default-deny egress policy breaks every hostname. Test DNS and add the narrowly required DNS allowance instead of allowing all egress indiscriminately.',
('Is successful kubectl apply proof that a NetworkPolicy blocks traffic?','No. Enforcement requires a supporting network plugin and observed traffic tests.'),['concepts/services-networking/network-policies/','tasks/administer-cluster/network-policy-provider/'],code='@lab:policy.yaml',mode='Policy-capable cluster',prereq='Networking lesson; a separate cluster with a verified NetworkPolicy-enforcing CNI for traffic tests.')
add('ingress','ckad','Ingress rules and the controller behind them','Services and networking','The route object and the traffic-handling implementation are separate.',
'''An Ingress describes HTTP/HTTPS routing to Services. An Ingress controller interprets that declaration and configures a traffic-handling implementation. Creating an Ingress without a matching controller does not create a reachable website.

Hosts, paths, pathType and backend Service ports must fit together. An IngressClass selects or describes the responsible implementation. TLS needs a certificate and private key in the expected Secret format, plus a hostname that the certificate covers.''',
'''Ingress is a stable but frozen API; Gateway API is the extensible successor discussed in CKA and deeper networking lessons. Controller-specific annotations are not portable Kubernetes behaviour. Check the chosen controller’s maintained installation and compatibility guidance rather than pasting an obsolete quickstart.

External DNS, load-balancer health checks, the controller route and backend readiness are different dependencies. A Host header can select a route during local testing even before public DNS is configured. A TLS handshake can succeed while the backend returns 503; that proves different portions of the path.''',
'bank.example.test routes / to bank-web on port 80. The fictional hostname is a lab input, not a public DNS record or a real bank domain.',
[('Host + path','bank.example.test /'),('Ingress controller','Resolve route and TLS configuration'),('Service backend','bank-web port 80')],
'Read ingress.yaml and validate it against the API. In a cluster with an installed, maintained controller, set the correct ingressClassName and use its documented local access path. Send a request with the matching Host header; record the controller and version.',
'An end-to-end request reaches the bank page. Without a controller, record only schema validation and explain the missing execution component.',
'An Ingress exists but no traffic arrives. Check class/controller reconciliation, address and route events before changing the application.',
('Why can an Ingress exist without serving any requests?','It is desired routing configuration. A compatible controller and reachable data plane must implement it.'),['concepts/services-networking/ingress/','concepts/services-networking/ingress-controllers/'],kind='architecture',code='@lab:ingress.yaml',mode='Ingress-capable cluster',prereq='Services lesson plus an installed maintained Ingress controller for live routing.')
add('rollouts','ckad','Rolling updates and honest rollback','Application deployment','Observe availability while replacing a version, not only after it finishes.',
'''A Deployment rollout creates a new ReplicaSet when its Pod template changes. maxSurge allows extra Pods during replacement; maxUnavailable allows a bounded reduction in available replicas. Percentages and rounding matter for small replica counts.

Readiness determines when new replicas can serve. A rollout can stall even though Pods exist. Inspect rollout status, conditions and Events, and retain the previous known-good version. An automatic restart of unhealthy containers is not the same as a rollback of the Deployment.''',
'''With two replicas, maxUnavailable: 0 and maxSurge: 1, a new ready replica is needed before an old one can be removed. This needs spare schedulable capacity. If a quota or resource shortage blocks the surge, rollout may not progress even though the existing version is healthy.

rollout undo restores a prior Pod template revision. It does not reverse a database migration, external message or independently changed ConfigMap. Design backward-compatible data transitions and record configuration alongside image versions. A successful rollback command is only the beginning of recovery verification.''',
'Change the bank Deployment image to an intentionally nonexistent tag to observe a stalled replacement while old ready replicas continue serving; then undo the Pod-template change.',
[('Old ReplicaSet','Keep available capacity'),('New ReplicaSet','Start, probe and become ready'),('Traffic + evidence','Verify the new response before completion')],
'Run the commands below on the disposable starter Deployment. rollout status is expected to time out for the bad image. Inspect the state, undo, then wait for successful rollout and fetch the page.',
'Old ready replicas preserve service in the specified strategy, and rollback restores a healthy Deployment. Record actual observed counts and image references.',
'Undo succeeds but the page remains incorrect because configuration changed independently. Restore a compatible configuration and retest.',
('Does rollout undo undo a schema migration?','No. It restores Deployment revision state, not external database operations.'),['concepts/workloads/controllers/deployment/'],code='kubectl -n tk-bank set image deployment/bank-web web=nginx:techknowen-does-not-exist\nkubectl -n tk-bank rollout status deployment/bank-web --timeout=30s\nkubectl -n tk-bank get pods\nkubectl -n tk-bank rollout undo deployment/bank-web\nkubectl -n tk-bank rollout status deployment/bank-web --timeout=120s')
add('release-strategies','ckad','Blue/green and canary with Kubernetes primitives','Application deployment','Choose how traffic reaches versions and define the evidence for promotion.',
'''Blue/green keeps two versions available and switches the active route or selector. Canary exposes a limited share of traffic to the candidate while observing errors and latency. Both require a promotion decision and a recovery route.

A Service selecting one old Pod and one new Pod is not a guarantee of exactly 50% user traffic. Connection reuse, session behaviour and implementation details can make counts uneven. Accurate weighted routing requires a capable traffic layer and measurement.''',
'''Label versions explicitly so a route can choose the intended candidate. Reusing identical broad selectors can mix versions unintentionally. A shared database must remain compatible with both versions during the transition; otherwise traffic switching can expose data incompatibility.

Promotion criteria should include a baseline, minimum observation volume, error thresholds and business correctness. A low-error five-request test is weak evidence. Long-lived connections and caches may keep traffic on old code after a selector change, so define what rollback actually guarantees.''',
'Create bank-blue and bank-green pages with visible version markers. A stable bank-active Service selects one colour. Verify the marker before and after the selector change.',
[('Blue','Known-good version remains available'),('Routing decision','Select active version deliberately'),('Green','Candidate validated before promotion')],
'Copy the starter into a separate namespace with two Deployments labelled release=blue and release=green and two distinct page ConfigMaps. Point one Service at blue, fetch it, switch only its selector to green, then switch back.',
'Requests return the selected version marker. Record the observed transition and explain why the experiment does not test database rollback or exact traffic weighting.',
'The candidate is unhealthy yet the Service is switched anyway. Add readiness verification and a rollback condition to the release checklist.',
('Do replica ratios guarantee exact canary traffic percentages?','No. They can approximate distribution under some conditions. Use a suitable routing layer and measured request data for controlled weights.'),['concepts/workloads/controllers/deployment/','concepts/services-networking/service/'],kind='architecture',code='kubectl -n tk-release patch service bank-active -p \'{"spec":{"selector":{"app":"bank-web","release":"green"}}}\'\nkubectl -n tk-release get endpointslices -l kubernetes.io/service-name=bank-active',prereq='Build the separate blue/green exercise described here before executing the selector change.')
add('helm','ckad','Helm: inspect, install, upgrade and recover','Application deployment','Treat a chart as a package that renders Kubernetes resources.',
'''A chart packages templates and default values. A release is an installed instance of that chart. Values customise the rendered objects; the resulting YAML still needs to be valid and appropriate for the cluster. Chart version and application image version are different identifiers.

Inspect an unfamiliar chart before installing it. It may create cluster-scoped permissions, webhooks, storage or external services. A package manager is not a trust decision. Prefer a maintained source, an explicit version and a review of rendered manifests.''',
'''helm template renders locally but cannot prove that all server capabilities, admission rules or runtime dependencies will accept the result. Upgrade and rollback manage release revisions, but hooks and external effects complicate reversibility. Persistent data may outlive a release or be affected by its cleanup policies.

A value named replicas has no universal meaning unless the chart uses it. Verify the rendered Deployment rather than assuming an override worked. Quote values with ambiguous types when necessary and keep reviewed values in a file instead of a long, unrepeatable command.''',
'The supplied small bank-info chart creates a two-replica nginx Deployment and a Service in its release namespace. It avoids cluster-wide permissions and external load balancers.',
[('Chart + values','Reviewed package and overrides'),('Rendered objects','Inspect image, replicas and permissions'),('Release','Install, observe, upgrade and rollback')],
'Create the chart files from the manifest library. Run helm lint and helm template before install. Install into tk-helm, upgrade replicaCount to 3, inspect history, then rollback to revision 1 and verify two replicas.',
'Observed Deployment replicas follow rendered values. Record Helm release history and verify service reachability rather than relying only on a successful Helm exit.',
'Change an unused value and observe no manifest difference. Find the template key actually used instead of assuming every value is automatically interpreted.',
('Is a Helm release the same as a chart version?','No. A release is an installed instance with its own revision history. The chart is the versioned package.'),['https://helm.sh/docs/intro/using_helm/','https://helm.sh/docs/chart_template_guide/getting_started/'],code='helm lint ./bank-info\nhelm template bank-info ./bank-info --namespace tk-helm\nhelm upgrade --install bank-info ./bank-info -n tk-helm --create-namespace --wait\nhelm upgrade bank-info ./bank-info -n tk-helm --set replicaCount=3 --wait\nhelm history bank-info -n tk-helm\nhelm rollback bank-info 1 -n tk-helm --wait',prereq='Install Helm using its official instructions. Create the supplied bank-info chart files first.')
add('kustomize','ckad','Kustomize: reusable bases and explicit overlays','Application deployment','Change declared YAML without embedding a programming template language.',
'''A Kustomize base contains reusable resources. An overlay references a base and supplies environment-specific patches or transformations. kubectl includes Kustomize through -k. Render first so changes in names, namespaces, labels and images are visible before apply.

A patch must target the intended kind/name and path. An overlay is not a replacement for understanding the underlying Kubernetes resource. Incorrect label transformations can alter selection and ownership in ways that surprise learners.''',
'''Generated ConfigMaps and Secrets can use content-derived name suffixes. References in supported fields are updated during rendering, making configuration changes produce new names and potentially a Pod-template change. Disabling the suffix changes that rollout story.

Do not mix imperative edits and declarative ownership casually. A later apply may overwrite a manual change. Inspect the rendered objects and compare live state, then reconcile the intended source. Server-side apply field ownership can surface conflicts that should be understood rather than forcibly discarded.''',
'The base bank Deployment has two replicas. A practice overlay changes only its replica count and namespace; the rendered output should make that difference obvious.',
[('Base','Reusable workload YAML'),('Overlay','Targeted environment changes'),('Rendered result','Review exact objects before apply')],
'Create the kustomize files from the library. Run kubectl kustomize kustomize/overlays/practice, inspect the output, apply it and confirm three replicas in tk-kustomize.',
'The output has the expected namespace and replica count. Explain why reviewing the source patch alone is less conclusive than inspecting the full render.',
'A patch target name is wrong. Correct the target or rendered naming transformation instead of editing the live object as the permanent fix.',
('What should you inspect before applying an overlay?','The complete rendered manifests, including selectors, namespace, images and generated resource references.'),['tasks/manage-kubernetes-objects/kustomization/','reference/using-api/server-side-apply/'],code='kubectl kustomize kustomize/overlays/practice\nkubectl apply -k kustomize/overlays/practice\nkubectl -n tk-kustomize rollout status deployment/bank-overlay\nkubectl -n tk-kustomize get deployment bank-overlay',prereq='Create the supplied base and overlay files before running these commands.')
add('extensions','ckad','CRDs and Operators: schema versus behaviour','Environment and security','A new API type needs a controller if it is meant to operate something.',
'''A CustomResourceDefinition adds a resource type to the Kubernetes API. A custom resource is one instance of that type. A controller can watch those instances and act on them. An Operator combines domain knowledge with controller behaviour for an application or platform capability.

A CRD alone does not create databases, backups or certificates. It provides an API schema and storage for declared objects. The responsible controller, permissions and dependencies must be present for reconciliation.''',
'''Schema validation rejects some malformed custom resources before a controller sees them. Status conditions should communicate accepted intent and observed progress, with a distinction between an admitted object and a ready managed service. Finalizers often coordinate cleanup of external resources.

Installing an Operator can introduce broad permissions, admission webhooks and upgrade responsibilities. Review its CRDs, compatibility and uninstall behaviour. A removed controller with remaining finalizers can leave resources terminating indefinitely. Never clear finalizers merely to make the display look tidy without understanding orphaned effects.''',
'The fictional BankReport custom resource records a desired reporting period. In the schema-only exercise, it deliberately does not generate a report because no report controller is installed.',
[('CRD','Register a validated resource shape'),('Custom resource','Request a BankReport period'),('Controller','Optional implementation performs the work')],
'Apply reports-crd.yaml and a BankReport instance. Discover it with api-resources and get it. Change the required period to an invalid type and observe validation rejection. Identify the absent controller explicitly.',
'The valid object is stored; no report output is claimed. You can explain what additional reconciler and permissions would be needed.',
'A team says the Operator works because kubectl get shows a custom resource. Ask for status conditions, controller logs and the actual managed result.',
('What does registering a CRD execute?','It extends the API schema. It does not, by itself, execute application reconciliation logic.'),['concepts/extend-kubernetes/api-extension/custom-resources/','concepts/extend-kubernetes/operator/'],kind='architecture',code='@lab:reports-crd.yaml')
add('api-versions','ckad','API discovery and deprecation-safe changes','Observability and maintenance','Match manifests to the cluster’s supported API rather than memorising old examples.',
'''apiVersion identifies an API group/version, not the kubectl binary version. Different resource kinds can use different API versions within the same cluster. Use api-resources and explain to discover supported shapes and fields.

A removed API version can make an old manifest fail before any Pod is created. A version change may also require field changes; replacing only the apiVersion line is not a complete migration strategy.''',
'''Storage versions and served versions are related but distinct. API conversion and CRD conversion webhooks become important when custom types evolve. Upgrade planning should inventory deprecated APIs, chart outputs, controllers and admission integrations—not just application images.

kubectl client/server skew has support limits. The course lab uses Kubernetes 1.35; use a client within the documented one-minor-version range. Read current exam instructions before scheduling because the published documentation site, practice cluster and examination environment can differ.''',
'Confirm that bank Deployment uses apps/v1 and its Service uses v1. Explain why those two values do not conflict.',
[('Discover','List served resources and versions'),('Validate','Check fields and server acceptance'),('Migrate','Test behaviour before upgrading production')],
'Run API discovery and explain for Deployment, Ingress and CronJob. Use server-side dry-run on supplied manifests. Compare an old Ingress example with the current schema without applying obsolete objects.',
'You identify both the resource’s served version and its required backend field structure. Runtime behaviour remains a separate check.',
'No matches for kind: distinguish an absent CRD from a removed built-in API version and from a typo.',
('Does changing apiVersion always migrate an old object specification correctly?','No. Required fields and semantics can change too. Consult the migration guidance and validate the resulting object.'),['reference/using-api/deprecation-guide/','reference/version-skew-policy/'],code='kubectl api-resources\nkubectl api-versions\nkubectl explain ingress.spec.rules.http.paths.backend\nkubectl apply --dry-run=server -f bank.yaml')
add('ckad-capstone','ckad','CKAD capstone and timed readiness','Certification practice','Demonstrate independent application delivery, then practise under a time budget.',
'''Use the lessons to build a small bank information service in a fresh namespace without copying a complete solution blindly. The target includes two replicas, configuration, probes, requests/limits, a Service, a completion-based reporting task and a restricted read-only ServiceAccount.

Work through one feature at a time: declare, inspect, exercise and record. Do not mark a task complete merely because apply returned success. Capture object state and the behaviour the requirement asked for.''',
'''The practice assessment is original and is not an exam dump. Use a two-hour rehearsal as a training exercise, checking current official exam duration, environment, permitted resources and candidate rules separately. Do not assume that tools available in this guide are allowed during an exam.

Readiness has two dimensions: fast accurate use of primitives and sound diagnosis when something fails. Repeat a scenario with a changed namespace, image or label so success depends on understanding. Maintain a mistake log: symptom, false assumption, correcting evidence and a faster verification command.''',
'The bank information service release must remain reachable during a failed candidate rollout. Its report Job finishes once per intended business operation in the design, while the demo prints only a marker.',
[('Build','Create the required objects'),('Break and repair','Selector, image or readiness fault'),('Prove','Request test, state evidence and explanation')],
'Use the assessment page’s CKAD task set. Complete a guided attempt, then a timed independent attempt in a fresh namespace. Score observable outcomes using the supplied rubric; do not count reading completion as a passed practical task.',
'All five CKAD domains have associated lesson/lab evidence. Repeat weak tasks with changed conditions and explain the limits of each observation.',
'A learner is fast at YAML generation but never checks namespace or endpoints. Include both in the final verification sequence for every relevant task.',
('Does finishing this reading path establish certification or SME status?','No. It supports preparation. Independent practical evidence, ongoing operations experience and the official exam are separate outcomes.'),['https://github.com/cncf/curriculum/blob/master/CKAD_Curriculum_v1.35.pdf','https://training.linuxfoundation.org/certification/certified-kubernetes-application-developer-ckad/','https://docs.linuxfoundation.org/tc-docs/certification/important-instructions-cka-ckad-cks'],mode='Timed local practice',code='kubectl config current-context\nkubectl create namespace tk-ckad-attempt\nkubectl -n tk-ckad-attempt get all\n# Build and verify the task set in this namespace.\n# Cleanup only after saving the evidence you need:\nkubectl delete namespace tk-ckad-attempt')
