# API and schema handoff

**ID:** 20/05_API_AND_SCHEMA_CONTRACTS · **Version:** 0.3 · **Status:** proposed, structurally validated · **Owner:** API/data architects · **Updated:** 2026-11-15

- [OpenAPI 3.1 contract](../10_BACKEND_AND_APIS/11_OPENAPI_SPECIFICATION.yaml): version 0.3.0, 129 operations; [operation index](../10_BACKEND_AND_APIS/12_OPERATION_INDEX.md) gives exact method/path/operation IDs.
- [Lifecycle catalog](../contracts/state-machines.json): 15 mandatory families, 84 guarded transitions; actors, source/destination, atomic effects and test references.
- [Scenario traceability](../contracts/scenario-traceability.json): 120 requirements and acceptance specifications with API/screen/data-family mappings and explicit manual boundaries.
- [Analytics schema](../contracts/workflow-analytics.schema.json): fixed event taxonomy and minimal allowed fields.
- [Field constraints](../09_DATA_ARCHITECTURE/10_FIELD_CONSTRAINTS.md): logical types, nullability conventions, amount bounds, relational checks, revision and allocation invariants.
- [Validation evidence](../review/contract-validation.json): actual document-schema checks, distinct from application tests.

Integration adapters validate provider-specific signatures and convert to the authenticated internal `/integration-events` contract; this endpoint must never be exposed as an unsigned universal webhook. Vendor selection does not invalidate the normalized design, but exact vendor protocol must be recorded and tested before activation. Type schemas cannot prove cross-record ownership, sums, lock ordering or legal enforceability: these remain documented server invariants and release tests.

The expanded interface also specifies anonymous-intake ownership proof, recovery completion, public content/listing/valuation projections, inspection templates/revisions, saved searches and consumer-offer acceptance. [Schema field reference](../10_BACKEND_AND_APIS/13_SCHEMA_FIELD_REFERENCE.md) enumerates all168 current schema definitions; [screen bindings](../05_UX_RESEARCH_AND_INFORMATION_ARCHITECTURE/10_SCREEN_CONTRACT_BINDINGS.md) map48 screens to these operations and controlled manual boundaries.
