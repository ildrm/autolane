# Tech Stack Decisions

| Metadata | Value |
|---|---|
| ID / version | 08/02_TECH_STACK_DECISIONS / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Tech Stack Decisions; jurisdiction-dependent policy decisions remain open. |

## Decision and alternatives
**PROPOSED, reversible until ADR approval:** TypeScript/React and a current supported Next.js release for public SSR and responsive authenticated applications; a modular Python/Django REST Framework backend, PostgreSQL as authoritative store, managed object storage, Redis for non-authoritative cache/fanout, and durable outbox/worker. Pin supported versions at delivery time after security review; this document makes no claim about the reference company's current stack.

| Option | Strength | Cost / decision |
|---|---|---|
| Modular monolith | Local transactions, simplest operation and delivery | Starts here; enforce boundaries by tests and module ownership. |
| Service-oriented / microservices | Independent scale and fault boundaries | Network failure, distributed ownership and on-call complexity; split only with sustained proven bottleneck, stable contract, independent deployment team and measurable SLO benefit. |
| Event-driven / hybrid | Durable decoupled notifications and projections | Asynchronous lag and duplicate messages; hybrid adjunct, not substitute for auction consistency. |
| Django/DRF | Familiar data modeling, admin ecosystem and rapid operations | Python concurrency and hiring must be benchmarked; select provisionally. |
| NestJS | One language end to end and structured modules | Node event-loop workload isolation needed; viable alternate if team capability dominates. |
| Go | Small resource footprint and concurrency | Slower business-feature iteration and different skills; candidate for measured fan-out bottleneck only. |
| PostgreSQL / Redis | Transactional authority / low-latency cache | Cache must not authorize bids or balances; validate failover and recovery. |
| OpenSearch / Elasticsearch | Rich faceting and relevance | Optional when PostgreSQL search fails measured requirements; rebuildable projection, review license and operating cost. |
| Queue / event stream | Broker for retries; stream for multiple replaying consumers | Begin transactional outbox plus durable queue; stream only with replay/throughput case. |
| WebSocket / SSE | Bidirectional live feed / simpler server push | WebSocket for dealer feed with HTTP commands; SSE valid fallback if read-only push suffices. |
| Responsive web / PWA / React Native / Flutter / native | One install-free codebase; optional caching; dedicated native device access | Start responsive web; evaluate PWA push/offline limits per device, native only when research justifies cost. Never accept offline bids. |

**Acceptance:** benchmark representative concurrency, operability, staffing and security before final approval. Object storage retains evidence; search and warehouse are projections, never money or bid authorities.
