# TechKnowen Kubernetes & Cloud

A separate learning programme within the SDLC Field Guide. Original explanations, diagrams and practical tasks use the fictional Harbour Bank information service. The simple application is not a financial system; later architecture designs are explicitly proposed examples.

## Programme

- 6 foundation lessons, 23 CKAD lessons, 19 CKA lessons and 23 GCP lessons.
- Each lesson has Understand, Behind the scenes and Hands-on views, with two distinct diagrams, a worked banking context, a fault exercise, expected evidence, an explained self-check and primary references.
- 23 displayed fixture files, four original independent assessments, a 44-term glossary and a study route with readiness gates.
- Domain mapping for CKAD, CKA, Google Cloud ACE and PCA, using the reviewed official curricula. This is a domain map, not a claim to provide a live lab for every cloud product.
- Search, responsive light/dark themes, local evidence notes and review progress. No download/export controls, backend, trackers or runtime network dependencies.

Read `index.html` directly or open the published `/kubernetes/` route. Installation, image pulls and live labs require the documented environment and network access. The guide never runs its commands for the learner. Google Cloud resources can incur charges.

## Editing

`src/author.py`, `ckad.py`, `cka.py` and `gcp.py` contain the lesson material. `deep-diagrams.json` describes all 71 detailed maps. `labs/` holds original fixtures, including a Helm chart and Kustomize directories. The build embeds all reading content and displayed examples into one HTML file.

Run `python3 build.py` to regenerate `content/course.json` and `index.html`. `--ckad-only` builds the initial foundation/CKAD checkpoint. The normal build requires only Python’s standard library; the optional fixture-generation script uses PyYAML.

See `VALIDATION.md` and the in-app Sources page for the execution boundaries. Local progress is self-reported and not proof of a passed lab or certification.
