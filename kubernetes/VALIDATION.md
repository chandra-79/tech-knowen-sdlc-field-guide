# Validation record — 2026-09-28

## Content and browser

- 71 unique lessons; every lesson has required prose, case, lab, verification, failure, self-check and references.
- 71 basic and 71 distinct detailed diagrams. The diagram skill's accessible-SVG and single-file checks passed on a static rendered collection of all 142 figures.
- Browser sweep: 229 routes, including all three views of every lesson, all tracks, four assessments, glossary, study route and support pages.
- No JavaScript errors, duplicate page IDs, broken lesson links, text outside diagram viewboxes or detailed node boxes, or horizontal page overflow in desktop and 390px-wide checks.
- Functional checks: note persistence, escaped note content, reviewed state, search, timer countdown, code copying, dark mode, mobile navigation and keyboard skip link.
- Offline `file://` test with network disabled: lesson text and SVG visible, search works, no HTTP requests made.
- 186 source URLs reached successfully. This checks availability on the review date, not a guarantee of future link stability or an exhaustive review of every linked page.
- Assessment totals: 100 points each. Domain and glossary links resolve. Displayed shell snippets parse in zsh; this is syntax validation, not cloud execution.

## Local Kubernetes execution

Disposable kind v0.33.0 cluster, Kubernetes v1.35.8, matching kubectl, dedicated kubeconfig. Node image pinned by digest in the setup lesson.

46 recorded operations/assertions passed covering the starter Service HTTP response, init preparation, Job/CronJob execution, dummy Secret mounting without payload logging, Pending diagnosis, RBAC allowed/denied operations, restricted execution, persistent-volume data after Pod replacement, CRD discovery, Kustomize and rollback.

The Helm chart passed lint, installation, upgrade and rollback. Final Helm revision 3 was deployed with two ready replicas, reflecting the rollback to the original replica setting.

The NetworkPolicy, Ingress, HPA and topology-spread Deployment examples passed server-side dry-run checks. This does **not** prove policy enforcement, external routing, metrics-driven scaling or multi-node distribution.

22 non-template YAML files parsed; the Helm template was checked by Helm rendering/lint. Gateway and kubeadm fixtures are environment-specific teaching starting points and were not installed as production components.

## Explicitly not executed

- Linux VM kubeadm installation, HA failure, node upgrade and etcd restore.
- Gateway/Ingress controller routing and enforcing-CNI traffic tests.
- HPA under load or multi-node scheduling resilience.
- Google Cloud resource creation, IAM grants, GKE provisioning, backups or billable services.

Those exercises retain their prerequisites and expected evidence. Offline designs are clearly distinct from observed results. No claim of certification endorsement, comprehensive production validation or guaranteed SME status is made.
