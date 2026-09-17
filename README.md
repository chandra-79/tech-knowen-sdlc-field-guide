# SDLC Field Guide · TechKnowen

![TechKnowen](brand/techknowen-logo.svg)

**Understand the software lifecycle through four complete, fictional business cases.**

[Read the guide](https://chandra-79.github.io/tech-knowen-sdlc-field-guide/) · [Try the banking demo](https://chandra-79.github.io/tech-knowen-sdlc-field-guide/#/demo) · [Explore four cases](https://chandra-79.github.io/tech-knowen-sdlc-field-guide/#/cases) · [Browse worked documents](https://chandra-79.github.io/tech-knowen-sdlc-field-guide/#/documents) · [Suggest an improvement](https://github.com/chandra-79/tech-knowen-sdlc-field-guide/issues)

[![GitHub stars](https://img.shields.io/github/stars/chandra-79/tech-knowen-sdlc-field-guide?style=social)](https://github.com/chandra-79/tech-knowen-sdlc-field-guide/stargazers)

Written for learners from non-technical and technical backgrounds. No programming experience is needed to follow the main learning path.

## What is included

- **Six lifecycle stages:** requirements, design, development, testing, deployment and maintenance.
- **184 worked documents (46 per case):** every document explains what, why, who, when, where, which related documents and how to prepare it.
- **160 newly authored concept notes**, a plain-language glossary and **48 original scenario self-checks** with explanations.
- **72 planned test cases** across banking, shopping, rentals and repair, plus guided exercises.
- **Four interactive demos:** a fictional bank, online shop, car-rental desk and community repair hub. Each exposes its important rules, review steps and failure paths.
- Local search, responsive layout, light/dark modes, source references and cross-linked examples.

The complete application is self-contained in `index.html`. It has no runtime packages, trackers, remote fonts, backend or required network calls. The public site provides in-page reading, without document download/export controls. Optional reference, sharing and GitHub links need internet access.

## A practical learning path

1. Read **Start here** and the **Banking case study**.
2. Log into the demo using the public training values shown on its screen.
3. Transfer SGD 200.00 from current to savings.
4. Follow **FR-06** through the FRD, detailed design, traceability matrix and test cases.
5. Compare normal behaviour with cancellation, insufficient funds and an ended session.
6. Explain what the local prototype demonstrates and what a real service still needs.

## Document library

| Area | Examples |
|---|---|
| Requirements | Stakeholders, BRD, MRD, PRD, CRD, SRS, FRD, QRD, TRD, user stories |
| Design | HLD, LLD, data dictionary, API contract, UIRD, architecture decision, threat assessment |
| Development | Work plan, review/Definition of Done, build record |
| Testing | Test plan, test cases, defect report, test summary, UAT, RTM |
| Delivery and operation | Deployment/rollback, release notes, user guide, operations runbook, disaster recovery |
| Maintenance | Change request, incident learning review, maintenance plan |

## Four cases, one learning sequence

| Case | Main questions |
|---|---|
| Harbour Bank | How do account access, review, transfers and exact money rules fit together? |
| Market Lane | When is stock held, consumed or restored, and how are repeat actions handled? |
| Open Road | Which date intervals overlap, and how do cancellations and maintenance blocks affect availability? |
| Second Spark | Which technician and part fit a job, and which transitions require approval? |

Each case follows requirements, design, development, testing, deployment and maintenance, with the same seven-question document pattern.

## Simulation boundaries

Harbour Bank is fictional. All accounts, credentials and transactions are teaching data. Deposits and withdrawals represent simplified completed cash events. Transfers occur only between two owned accounts. The demo does not implement real authentication, durable ledger storage, multi-user concurrency, real payments or production banking security.

Balances, stock, bookings, jobs and session state are held in the current tab and reset on reload. The additional cases use simulated payments, a fictional scheduling period and illustrative repair workflows; they do not provide real transaction or repair services. Real-system controls are discussed separately in the architecture and security documents. Worked sample reports are explicitly labelled; they are not evidence of actual banking approvals or certifications.

## Sources and attribution

The site includes references to NASA requirements guidance, ISTQB, the Scrum Guide, OWASP, PostgreSQL, Kubernetes, AWS and SWEBOK where relevant. Explanations, questions and worked case documents are authored for this standalone guide. Public sources are cited for technical background and further reading. No endorsement or accreditation by the referenced organisations is implied.

## Help the guide reach more learners

- **Star this repository** if it is useful to you.
- Share the live guide with learners and colleagues.
- Open an issue with a clear example of a confusing explanation, incorrect rule or broken interaction.
- Suggest improvements that preserve plain language and the coherent banking case.

See [CONTRIBUTING.md](CONTRIBUTING.md) for useful issue and contribution guidance.

Created by [chandra-79](https://github.com/chandra-79) · **TechKnowen** · [Ajna Consulting Services](https://ajnacs.com/)
