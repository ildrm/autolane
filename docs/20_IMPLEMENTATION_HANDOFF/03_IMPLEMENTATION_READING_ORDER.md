# Implementation Reading Order

| Metadata | Value |
|---|---|
| ID / version | 20/03_IMPLEMENTATION_READING_ORDER / 0.1 |
| Status | Proposed handoff; implementation not approved |
| Owner / reviewers | Documentation architect / product, operations, legal, finance, engineering, security and QA |
| Updated | 2026-11-15 |
| Purpose and scope | Implementation Reading Order for future review and implementation planning. |

## Recommended reading sequence
1. [Master discovery and decision register](../00_MASTER_INDEX.md) and [evidence](../00_RESEARCH_EVIDENCE.md): distinguish verified reference statements, proposals and open decisions.
2. [Business model and operations](../01_BUSINESS_MODEL_AND_OPERATIONS.md), [product inventory](../02_PRODUCT_AND_PANEL_INVENTORY.md), and [initial requirements traceability](../00_GOVERNANCE/07_REQUIREMENTS_TRACEABILITY.md), [critical-loop crosswalk](../TRACEABILITY_CROSSWALK.md) and [proposed measurable NFRs](../NFR_MEASURABLE_BASELINE.md): understand intended actors, outcomes and current trace gaps.
3. [Scenarios and state machines](../03_USER_JOURNEYS_AND_SCENARIOS/05_STATE_MACHINE_CATALOG.md), [role matrix](../04_ROLES_AND_PANELS/02_ROLE_PERMISSION_MATRIX.md), and [screen inventory](../05_UX_RESEARCH_AND_INFORMATION_ARCHITECTURE/04_SCREEN_INVENTORY.md): inspect task paths, permissions and screen states.
4. [Creative direction](../06_VISUAL_DESIGN_SYSTEM/01_CREATIVE_DIRECTION.md), [tokens](../06_VISUAL_DESIGN_SYSTEM/03_DESIGN_TOKENS.md), and [motion inventory](../07_ANIMATION_3D_AND_GRAPHICS/02_ANIMATION_INVENTORY.md): inspect original, proposed design and accessibility fallbacks.
5. [Architecture](../08_SOFTWARE_ARCHITECTURE/01_ARCHITECTURE_OVERVIEW.md), [data model](../09_DATA_ARCHITECTURE/01_DATA_MODEL.md), [API catalog](../10_BACKEND_AND_APIS/02_API_CATALOG.md), [OpenAPI](../10_BACKEND_AND_APIS/11_OPENAPI_SPECIFICATION.yaml), [frontend architecture](../11_FRONTEND_ENGINEERING/01_FRONTEND_ARCHITECTURE.md), and [auction concurrency](../12_AUCTION_AND_TRANSACTION_SYSTEMS/03_AUCTION_CONCURRENCY.md): inspect authoritative state and technical contracts.
6. [Operations](../13_OPERATIONAL_SYSTEMS/01_BRANCH_OPERATIONS.md), [security](../14_SECURITY_AND_COMPLIANCE/01_SECURITY_ARCHITECTURE.md), [quality](../15_QUALITY_ASSURANCE/01_MASTER_TEST_STRATEGY.md), [SEO](../16_SEO_AND_CONTENT/01_SEO_STRATEGY.md), analytics and infrastructure sections: integrate cross-cutting constraints.
7. [Delivery roadmap](../19_DELIVERY_AND_ORGANIZATION/06_FULL_PRODUCT_ROADMAP.md), [readiness](01_IMPLEMENTATION_READINESS.md), [configuration](07_CONFIGURATION_CATALOG.md) and [unresolved decisions](09_UNRESOLVED_DECISIONS.md): prepare an evidence-based go/no-go.

Resolve conflicts by approved business/legal decisions first, then canonical domain specification and its version, not by guessing which later filename is more authoritative. When two draft artifacts disagree, log the conflict and seek the accountable owner; do not silently infer a policy or implement the more convenient interpretation.

## Revision 0.3 source of truth

The [current audit](../FINAL_COMPLETENESS_AUDIT.md), [policy baseline](../POLICY_BASELINE.md), [scenario acceptance mappings](../SCENARIO_TRACEABILITY.md) and [API/schema handoff](05_API_AND_SCHEMA_CONTRACTS.md) supersede earlier limited-coverage counts and validation status. Real stakeholder approval, provider evidence and runtime testing are still not claimed.
