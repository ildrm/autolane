# C4 Diagrams

| Metadata | Value |
|---|---|
| ID / version | 08/03_C4_DIAGRAMS / 0.3 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | C4 Diagrams; jurisdiction-dependent policy decisions remain open. |

## C4 context
```mermaid
flowchart LR
 Seller --> Platform[Managed marketplace]
 Dealer --> Platform
 Staff --> Platform
 Platform --> Identity[Identity provider]
 Platform --> Communications[Email and SMS providers]
 Platform --> External[Legal, transfer and payment counterparties]
```
## Containers and trust
```mermaid
flowchart TD
 Browser[Public / dealer / staff browsers] --> Edge[WAF and routing]
 Edge --> App[Web presentation]
 Edge --> API[API and modular application]
 Browser --> RT[Realtime gateway]
 API --> SQL[(Transactional database)]
 API --> Obj[(Private object store)]
 SQL --> Relay[Outbox relay and workers]
 Relay --> RT
 Relay --> Ext[Approved integrations]
```
## Auction components
```mermaid
sequenceDiagram
 participant D as Dealer
 participant A as API and auction module
 participant P as PostgreSQL
 participant O as Outbox relay
 participant G as Gateway
 D->>A: authenticated bid + idempotency key
 A->>P: lock auction, validate clock and policy, persist bid/result + outbox
 P-->>A: commit
 A-->>D: accepted/rejected canonical result
 O->>P: read committed outbox
 O->>G: publish versioned update (at least once)
 G-->>D: snapshot version / update
```
Inferred infrastructure is not a reference-business observation. Browser, external provider and storage are separate trust boundaries. Gateway is not an authority. Lost notifications are recovered by the snapshot and revision protocol. The following additional sequences define the identity, inspection, contract, payment and delivery boundaries; no diagram implies money or vehicle custody.

## Deployment and failure domains (proposed)

```mermaid
flowchart TB
    Users[Browser clients] --> Edge[Public edge and WAF]
    Edge --> Web[Web rendering replicas]
    Edge --> API[API replicas in separate failure zones]
    Users --> Gateway[Authorized realtime gateways]
    API --> DB[(Primary transaction store)]
    DB --> Sync[(Synchronous durable replica / approved fault boundary)]
    API --> Private[(Quarantine and private evidence store)]
    Private --> Scanner[Restricted malware and format scanner]
    DB --> Workers[Outbox relay and domain workers]
    Workers --> Gateway
    Workers --> Adapters[Outbound provider adapters]
    Adapters --> Provider[Contracted external services]
    DB --> Backup[(Isolated encrypted recovery store)]
    Private --> Backup
```

Only edge, presentation and explicitly approved provider ingress are externally reachable. Database, workers, storage and scanning run on restricted networks and service identities. Region, provider, availability zones and data residency are deployment decisions tied to market approval; this diagram commits to isolation/durability behavior, not a vendor. A read replica may serve lag-tolerant analytics but not bid admission or seller acceptance.

## Intake identity and booking

```mermaid
sequenceDiagram
    participant U as Seller
    participant I as Identity / intake
    participant S as Scheduling
    participant D as Database
    participant N as Notification worker
    U->>I: Save anonymous draft and request claim challenge
    I-->>U: Uniform challenge response
    U->>I: Authenticated verified contact + one-time proof
    I->>D: Bind unclaimed draft to verified principal
    U->>S: Book server-issued slot + intent key
    S->>D: Lock capacity, check eligibility, insert appointment + outbox
    D-->>S: Commit or conflict
    S-->>U: Canonical booking or alternative slots
    N->>D: Consume committed notification intent
    N-->>U: Booking confirmation (delivery independent)
```

## Inspection publication and correction

```mermaid
sequenceDiagram
    participant I as Assigned inspector
    participant R as Independent reviewer
    participant A as Inspection application
    participant D as Database / evidence metadata
    participant Q as Auction safety workflow
    I->>A: Template-pinned findings and clean evidence IDs
    A->>D: Save versioned revision and audit
    R->>A: Review exact revision, publish with ETag
    A->>D: Check author differs, completeness, checksum; publish + outbox
    D-->>R: Published immutable revision
    R->>A: Material correction with reason
    A->>D: Preserve original, create successor and set auction safety hold atomically
    A->>Q: Committed correction event
    Q->>D: Read committed hold and coordinate authorized resolution
```

Publication must not race with a material correction and bid admission. The auction stores a safety-hold/valid-report guard checked under its lock; correction marks affected auction hold atomically within the same modular database transaction before acknowledging a material correction. The asynchronous event distributes the fact but is not the sole safety barrier. If cross-service extraction later prevents this transaction, a new reviewed consistency protocol is required before enabling that architecture.

## Transaction coordination without implied custody

```mermaid
sequenceDiagram
    participant P as Authorized participant
    participant T as Transaction coordinator
    participant C as Contract / signature adapter
    participant F as Finance evidence reviewer
    participant L as Legal title reviewer
    participant H as Logistics
    P->>T: Accept current authorized offer
    T->>T: Atomically create origin-linked case
    C-->>T: Verified exact-version signatures
    F-->>T: Independently reconciled required obligations
    L-->>T: Verified external title evidence
    H-->>T: Signed physical handover evidence
    T->>T: Recheck all current milestones and exceptions
    T-->>P: Closure only when approved policy is satisfied
```

## Data flow and disclosure boundaries

```mermaid
flowchart LR
    Private[Private domain records] --> Projection[Field and purpose authorization]
    Projection --> Customer[Own-case customer DTO]
    Projection --> Dealer[Eligible auction DTO]
    Projection --> Staff[Assigned staff DTO]
    Private --> Outbox[Minimal internal outbox]
    Outbox --> Search[Approved-public search projection]
    Outbox --> BI[Purpose-limited analytics projection]
    Private --> Audit[Restricted immutable audit]
    Audit --> Security[Audited security review]
```

Search and analytics apply their own explicit allowlists and deletion/tombstone propagation. Neither projection is used to authorize a bid, claim funds, confirm title or close a transaction. Every arrow crossing a trust boundary has a scoped identity, schema, timeout and observable failure owner.
