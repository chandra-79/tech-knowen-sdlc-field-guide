# SDLC Field Guide · TechKnowen

![TechKnowen](brand/techknowen-logo.svg)

**Understand the software lifecycle through online banking, then choose how deeply to explore.**

[Read the guide](https://chandra-79.github.io/tech-knowen-sdlc-field-guide/) · [Try the banking demo](https://chandra-79.github.io/tech-knowen-sdlc-field-guide/#/demo) · [Choose advanced cases](https://chandra-79.github.io/tech-knowen-sdlc-field-guide/#/advanced/cases) · [Browse worked documents](https://chandra-79.github.io/tech-knowen-sdlc-field-guide/#/documents) · [Suggest an improvement](https://github.com/chandra-79/tech-knowen-sdlc-field-guide/issues)

[![GitHub stars](https://img.shields.io/github/stars/chandra-79/tech-knowen-sdlc-field-guide?style=social)](https://github.com/chandra-79/tech-knowen-sdlc-field-guide/stargazers)

Written for learners from non-technical and technical backgrounds. No programming experience is needed to follow the main learning path.

## Choose your learning depth

| Level | Purpose | Examples and diagrams |
|---|---|---|
| **1 · Core revision** | Understand the central ideas in the familiar sequence: foundations, requirements, design, development, testing, deployment and maintenance. | Banking only. Simple pictures, plain descriptions, introductory document extracts and self-checks. |
| **2 · More detail** | Explore those same concepts more deeply when ready. | Banking only. More detailed models, reasoning, limitations and complete worked records. |
| **3 · Advanced and beyond** | Deliberately choose additional subjects and applications beyond the core learning scope. | Extension topics and the shopping, rental and community repair cases, with their own diagrams, documents and demos. |

Each core topic has a direct **More detail** choice and a way back to the simple explanation. Search stays within the selected level. Legacy links to other cases present an explicit advanced-entry choice.

## What is included

- **114 core concept guides**, each with separate Core and More views.
- **68 named subtopics** explaining patterns, architecture styles, diagram types, testing approaches, engineering principles and development tools through banking.
- **46 additional topics** in Advanced and beyond.
- **27 introductory banking documents** in Core and **32 complete banking records** in More. Each explains what, why, who, when, where, which related information and how.
- **184 worked documents overall:** 46 per case, with specialist banking records and all three other case libraries in Advanced.
- **47 optional comparisons and applications** in the advanced area.
- **48 original scenario self-checks:** 31 available in Core, 37 in More (including the Core questions), and 11 separate advanced questions.
- **Four interactive demos:** banking in the main learning path; shopping, rentals and repair in Advanced.
- Local search, responsive diagrams, light/dark modes, source references and cross-linked examples.

The complete application is self-contained in `index.html`. It has no runtime packages, trackers, remote fonts, backend or required network calls. The public site provides in-page reading, without document download/export controls. Optional reference, sharing and GitHub links need internet access.

## Read a visual example

- [Banking HLD](https://chandra-79.github.io/tech-knowen-sdlc-field-guide/#/doc/hld): actual browser responsibilities and proposed service boundaries.
- [Banking LLD](https://chandra-79.github.io/tech-knowen-sdlc-field-guide/#/doc/lld): transfer sequence, balance conservation and state transitions.
- [Rental LLD](https://chandra-79.github.io/tech-knowen-sdlc-field-guide/#/advanced/case/rentals/doc/lld): interval overlap, booking states and replay.
- [Testing methods](https://chandra-79.github.io/tech-knowen-sdlc-field-guide/#/concept/test-functions-and-quality-characteristics?level=2): levels, techniques, evidence and trade-offs.

Diagrams use original local SVG or semantic HTML with captions and descriptive text. Simple Core pictures stack on small screens; wide detailed diagrams can be panned. No external diagram service is required.

## A practical learning path

1. Read **Start here** and the **Banking case study**.
2. Log into the demo using the public training values shown on its screen.
3. Transfer SGD 200.00 from current to savings.
4. Open **More detail** to follow **FR-06** through the complete FRD, detailed design, traceability matrix and test cases.
5. Compare normal behaviour with cancellation, insufficient funds and an ended session.
6. Explain what the local prototype demonstrates and what a real service still needs.
7. Choose **Advanced and beyond** only when you want additional topics or another business case.

## Document library

| Area | Examples |
|---|---|
| Requirements | Stakeholders, BRD, MRD, PRD, CRD, SRS, FRD, QRD, TRD, user stories |
| Design | HLD, LLD, data dictionary, API contract, UIRD, architecture decision, threat assessment |
| Development | Work plan, review/Definition of Done, build record |
| Testing | Test plan, test cases, defect report, test summary, UAT, RTM |
| Delivery and operation | Deployment/rollback, release notes, user guide, operations runbook, disaster recovery |
| Maintenance | Change request, incident learning review, maintenance plan |

## One core case, three optional advanced cases

| Case | Main questions |
|---|---|
| Harbour Bank · Core and More | How do account access, review, transfers and exact money rules fit together? |
| Market Lane · Advanced | When is stock held, consumed or restored, and how are repeat actions handled? |
| Open Road · Advanced | Which date intervals overlap, and how do cancellations and maintenance blocks affect availability? |
| Second Spark · Advanced | Which technician and part fit a job, and which transitions require approval? |

The three advanced cases reuse the six-stage and seven-question document patterns to help learners compare domains after choosing to extend their learning.

## Simulation boundaries

Harbour Bank is fictional. All accounts, credentials and transactions are teaching data. Deposits and withdrawals represent simplified completed cash events. Transfers occur only between two owned accounts. The demo does not implement real authentication, durable ledger storage, multi-user concurrency, real payments or production banking security.

Balances, stock, bookings, jobs and session state are held in the current tab and reset on reload. The additional cases use simulated payments, a fictional scheduling period and illustrative repair workflows; they do not provide real transaction or repair services. Real-system controls are discussed separately in the architecture and security documents. Worked sample reports are explicitly labelled; they are not evidence of actual banking approvals or certifications.

## Sources and attribution

The site includes references to NASA requirements guidance, ISTQB, the Scrum Guide, OWASP, PostgreSQL, Kubernetes, AWS and SWEBOK where relevant. Explanations, questions and worked case documents are authored for this standalone guide. Public sources are cited for technical background and further reading. No endorsement or accreditation by the referenced organisations is implied.

## Help the guide reach more learners

- **Star this repository** if it is useful to you.
- Share the live guide with learners and colleagues.
- Open an issue with a clear example of a confusing explanation, incorrect rule or broken interaction.
- Suggest improvements that preserve plain language and consistency across all four cases.

See [CONTRIBUTING.md](CONTRIBUTING.md) for useful issue and contribution guidance.

Created by [chandra-79](https://github.com/chandra-79) · **TechKnowen** · [Ajna Consulting Services](https://ajnacs.com/)
