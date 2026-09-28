import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
LESSONS=[]
K='https://kubernetes.io/docs/'
def add(id,track,title,domain,summary,understand,deep,case,nodes,lab,verify,fault,answer,refs,kind='flow',mode='Local cluster',code='',prereq='Complete Setup and the starter application lab.'):
 LESSONS.append(dict(id=id,track=track,title=title,domain=domain,summary=summary,understand=understand.split('\n\n'),deep=deep.split('\n\n'),case=case,nodes=[{'title':a,'detail':b} for a,b in nodes],diagramType=kind,lab=lab,verify=verify,fault=fault,question=answer[0],answer=answer[1],refs=[K+u if not u.startswith('http') else u for u in refs],mode=mode,code=code,prereq=prereq))
add('orientation','foundation','Your first mental model','Foundations','Kubernetes keeps a declared workload running across a group of machines.',
'''An application is the software people use. A container packages its program and dependencies. A Pod is the Kubernetes unit that runs one or more closely related containers. A node is a machine; a cluster is a coordinated group of nodes. These are different boundaries, not interchangeable names.

Instead of asking an operator to restart each failed process, you describe a desired state: two copies of the banking information service, using a particular image. Controllers repeatedly compare that intent with observed state. They request changes when the two differ. Kubernetes helps with placement and recovery; it does not invent correct business rules or repair a corrupt database.''',
'''A declaration is stored through the API. Reconciliation is asynchronous: successful submission does not mean the application is ready. Status, Events and an actual request give different evidence. The scheduler chooses a node for an unscheduled Pod; the kubelet on that node asks a runtime to run its containers.

The control plane coordinates. The data plane carries application traffic. Existing containers can continue when the control plane is unavailable, while scheduling, rollout and repair operations may fail. A cluster is therefore not one magical computer with instantaneous state.''',
'Harbour Bank begins with a read-only information page. It contains no accounts or money. Two identical replicas let us study availability before introducing external data and identity.',
[('Intent','Two information-page replicas'),('Reconciliation','Compare desired and observed state'),('Evidence','Ready Pods and a successful HTTP request')],
'Before installing anything, draw a laptop, two worker machines, one API server and two Pods. Place each term from the introduction. Mark where a user request travels and where an operator sends a declaration.',
'Explain why a running container and an accepted YAML file are insufficient evidence that a customer can reach the page.',
'Claim to challenge: Kubernetes automatically makes every application highly available. Identify the single database, single region and bad application code that can still fail.',
('Does Kubernetes understand whether a transfer is financially correct?','No. It manages declared infrastructure and workload state. Financial invariants belong in the application, storage design and tests.'),['concepts/overview/components/','concepts/architecture/controller/'],mode='Offline reasoning',prereq='Ordinary computer familiarity.')
add('terminal','foundation','Terminal, files, HTTP and YAML','Foundations','Learn the small set of command-line and networking ideas used in every lab.',
'''A terminal runs commands. A path identifies a file or directory. A shell expands variables before a program receives them. Copy commands line by line while reading their purpose; angle-bracket placeholders are not literal values. A pipe sends one command’s output to another.

HTTP is a request/response protocol. A hostname must resolve to an address; a connection must reach a listening port; then an HTTP handler responds. A DNS error, connection refusal and HTTP 503 describe different layers. YAML represents maps and lists using indentation; spaces and exact field names matter.''',
'''kubectl turns your request into Kubernetes API operations. The apiVersion and kind select a schema, metadata identifies the object, spec usually expresses intent and status reports observations. Unknown or wrongly indented fields are not harmless formatting changes.

A manifest may parse as YAML but still be invalid for its Kubernetes resource or cluster version. Client-side generation, schema inspection and server-side dry-run answer progressively different questions. None proves runtime connectivity. Learn to preserve stderr, exit codes and the namespace when recording an observation.''',
'A banking page might resolve correctly but return 503 because no ready backend exists. Do not change DNS merely because “the website is down.”',
[('Name','Resolve bank-web to an IP'),('Connection','Connect to the Service port'),('Response','Inspect status and response body')],
'Create a working folder and a text file. Run the commands below. Explain every pipeline stage. Then inspect the supplied starter manifest and identify map keys versus list items.',
'You can distinguish a command failure from a valid empty result and explain why indentation changes object structure.',
'Indent a container image under metadata in a copied file; compare YAML parsing with Kubernetes validation. Restore the original before applying.',
('Is HTTP 404 a DNS failure?','No. An HTTP server answered. Investigate routing/path or the application rather than assuming the hostname failed.'),['reference/kubectl/','concepts/overview/working-with-objects/'],code='pwd\nmkdir -p techknowen-labs\ncd techknowen-labs\nprintf "ready\\n" > observation.txt\ncat observation.txt\nkubectl explain deployment.spec.template.spec.containers',prereq='A terminal; kubectl is installed in the next lesson.')
add('setup','foundation','Set up a disposable learning cluster','Foundations','Use a local container-backed cluster before spending money on cloud infrastructure.',
'''Install a container engine, kubectl and kind using their official platform instructions. On macOS or Windows, the engine runs Linux containers through a virtual machine. On Linux it normally uses the host kernel. Check that the engine is running before asking kind to create nodes.

The course cluster is named techknowen-course. A separate kubeconfig keeps lab access apart from normal work. Every command must target that configuration. The pinned node image below provides a reproducible Kubernetes 1.35 learning baseline corresponding to the researched curriculum; it is not a promise about the version of your future exam.''',
'''A kind node is a container that contains Kubernetes node services; application containers run through containerd inside it. This nested arrangement is convenient for API practice but does not reproduce cloud load balancers, independent physical failure domains or a managed control plane.

Allow approximately 4 CPUs, 6–8 GB RAM and image-download disk space for comfortable practice; this is a planning estimate. Internet is needed for installation and image pulls. The guide itself is offline-readable; a real cluster cannot be simulated merely by opening the HTML. Use the offline reasoning tasks if the runtime is unavailable.''',
'The banking demo needs no GCP project. Local port forwarding exposes the learning page only through the chosen localhost listener.',
[('Laptop','Terminal and dedicated kubeconfig'),('kind node','Disposable Linux node container'),('Workloads','Banking Pods in lab namespaces')],
'Follow the linked installation pages for your operating system. Start the container engine. Run the setup commands; wait until the node reports Ready. Keep this terminal’s KUBECONFIG setting for subsequent labs.',
'kubectl cluster-info names the lab server; get nodes shows Ready; current-context is kind-techknowen-course. Save client/server versions with your evidence.',
'If the Docker socket is unavailable, start the engine rather than changing application YAML. If ImagePullBackOff appears later, check registry access and architecture.',
('Why use a dedicated kubeconfig?','It reduces the chance that a learning command changes an unrelated cluster. Confirm context before every mutating exercise.'),['https://kind.sigs.k8s.io/docs/user/quick-start/','tasks/tools/','https://github.com/kubernetes-sigs/kind/releases/tag/v0.33.0'],kind='architecture',code='mkdir -p techknowen-labs\ncd techknowen-labs\nexport KUBECONFIG="$PWD/kubeconfig"\ndocker info\nkind create cluster --name techknowen-course --kubeconfig "$KUBECONFIG" --image kindest/node:v1.35.8@sha256:07b2536e30b803ed61d1677a79df6115f798ce64c80f9e22f6ed45afd09323c0\nkubectl config current-context\nkubectl get nodes\nkubectl version',prereq='Container engine, kind v0.33.0 and a kubectl client within one minor version of the API server. Use official installation instructions.')
add('api-control-plane','foundation','What happens after kubectl apply?','Foundations','Follow intent through the API, controllers, scheduler and node.',
'''kubectl contacts the API server using the selected context. Authentication identifies the caller. Authorization checks the requested action. Admission can validate or change the object before accepted state is persisted. A Deployment controller and ReplicaSet controller then create the objects needed to reach the desired replica count.

The scheduler does not start a container. It chooses a suitable node and records that assignment. The kubelet observes the assignment, obtains the image through the runtime and reports status. Readiness is a separate signal from process creation.''',
'''Controllers normally watch API changes and use work queues; they do not all write directly to etcd. Each controller must tolerate retries and changes since its last observation. Resource versions help detect conflicting updates. Ownership references associate Pods with ReplicaSets and Deployments, enabling garbage collection.

The request-to-running journey crosses several asynchronous boundaries. A timeout from kubectl does not necessarily prove the server rejected an operation; inspect named state before retrying a create. Conversely, an API success means acceptance, not successful scheduling. Pending, image pull and readiness failures need different evidence.''',
'Ask for two bank-web replicas. Observe a Deployment, its ReplicaSet and two Pods. Deleting one Pod should produce a replacement with a new identity, not revive the deleted object.',
[('API server','Accept and persist desired state'),('Controllers','Create and count owned Pods'),('Scheduler + kubelet','Assign a node; run and report')],
'After the starter lab, inspect ownerReferences and watch the Pod list in a second terminal. Delete exactly one bank-web Pod by its name and compare old/new UIDs.',
'The Deployment returns to two Ready replicas. Record the owner chain and distinguish replacement from a container restart inside the same Pod.',
'If a replacement remains Pending, inspect Events and resource requests before deleting more Pods.',
('Does the scheduler write container processes onto a node?','No. It binds a Pod to a node. The kubelet and container runtime perform execution.'),['concepts/overview/components/','concepts/architecture/controller/','concepts/architecture/garbage-collection/'],kind='sequence',code='kubectl -n tk-bank get deploy,rs,pods\nkubectl -n tk-bank get pods -o custom-columns=NAME:.metadata.name,UID:.metadata.uid,OWNER:.metadata.ownerReferences[0].kind\nkubectl -n tk-bank get events --sort-by=.metadata.creationTimestamp')
add('starter','foundation','Run the Harbour Bank information service','Foundations','Start with a tiny, observable service that every later lesson can change.',
'''This sample serves a static, fictional banking information page. It does not authenticate users, hold balances, transfer money or connect to a bank. We use this small workload to learn deployment mechanics without confusing Kubernetes practice with financial software implementation.

The manifest creates a namespace, ConfigMap, Deployment and ClusterIP Service. Two web containers read a page from the ConfigMap. A Service selects their shared app label. Port forwarding supplies a temporary local route for your browser. No public load balancer is created.''',
'''The Deployment’s selector must match its Pod template labels. The Service’s selector is independent and must also match the intended Pods. A ready Deployment can coexist with a broken Service selector. Test both workload readiness and the request path.

The nginx image is a teaching dependency, not a production image recommendation. Later security labs use a dedicated compatible unprivileged workload rather than blindly applying restrictive settings to an image that expects root-owned paths. A ConfigMap mounted as a directory updates eventually; environment-variable values are captured at container start.''',
'Your acceptance criterion is precise: two Ready bank-web Pods, a Service with usable endpoints, and a localhost HTTP response containing Harbour Bank learning service.',
[('Browser','localhost:8080 via port-forward'),('Service','Select app=bank-web'),('Two Pods','Serve the mounted information page')],
'Save the starter YAML shown below as bank.yaml, apply it, wait for rollout, then run port-forward in a separate terminal. Open http://127.0.0.1:8080. Stop the forward with Ctrl-C when finished.',
'Run curl in another terminal and retain its HTTP response. Inspect EndpointSlices to see the selected Pod addresses. A resource count alone is not the acceptance test.',
'Change the Service selector to app=bank-typo, observe the missing endpoints, then reapply bank.yaml. Do not alter the Deployment selector to fix a Service mistake.',
('Which resource gives the Pods a stable in-cluster access name?','The Service. Pod addresses can change; the Service selects the current eligible endpoints.'),['concepts/workloads/controllers/deployment/','concepts/services-networking/service/'],kind='architecture',code='@lab:bank.yaml',prereq='Setup complete. Save the manifest in your techknowen-labs folder.')
add('objects-contexts','foundation','Names, namespaces, labels and ownership','Foundations','Find the right object before changing it.',
'''A context chooses a cluster, credentials and an optional default namespace. Namespaces organise many namespaced objects; they do not by themselves enforce network isolation. Names are unique within the relevant kind and scope, while UIDs identify a particular object instance.

Labels are queryable key/value groupings. An annotation carries extra metadata that is not intended as a selection mechanism. A selector may return zero, one or many objects. Always inspect a selection before using it in a delete, scale or patch command.''',
'''A Deployment owns ReplicaSets, which own Pods. Deleting a child alone usually triggers replacement while the controller still desires it. A namespace does not scope Nodes, PersistentVolumes, ClusterRoles or CRDs. RBAC Roles can grant namespace-limited operations, but a user may also have broader grants.

Finalizers delay actual deletion until their cleanup conditions are satisfied. Removing one by hand can leave infrastructure or data behind. Examine the responsible controller and its failure before forcing deletion. Prefer declarative changes to the owning workload for lasting effects.''',
'Keep banking exercises in tk-bank and independent tasks in a unique tk-* namespace. Never use an unreviewed all-namespaces deletion as a cleanup shortcut.',
[('Context','Which cluster and identity?'),('Namespace + kind','Which scope and object type?'),('Name or selector','Which exact objects will change?')],
'List contexts without switching to an unknown cluster. Query bank Pods by label. Add an annotation to the Deployment, then compare metadata with the Pod template.',
'The selector lists exactly the intended Pods. You can explain why annotating a Deployment object alone need not annotate its Pods.',
'Run the same read-only query in a namespace with no workload; “No resources found” is not proof that the cluster is empty.',
('Does a namespace automatically block another namespace’s network traffic?','No. Network isolation requires enforced policies or other network controls.'),['concepts/overview/working-with-objects/labels/','concepts/overview/working-with-objects/namespaces/','concepts/overview/working-with-objects/finalizers/'],code='kubectl config get-contexts\nkubectl -n tk-bank get pods -l app=bank-web --show-labels\nkubectl -n tk-bank annotate deployment bank-web learning.techknowen/topic=ownership --overwrite\nkubectl api-resources --namespaced=false')
