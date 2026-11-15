# Configuration Catalog

| Metadata | Value |
|---|---|
| ID / version | 20/07_CONFIGURATION_CATALOG / 0.1 |
| Status | Proposed handoff; implementation not approved |
| Owner / reviewers | Documentation architect / product, operations, legal, finance, engineering, security and QA |
| Updated | 2026-11-15 |
| Purpose and scope | Configuration Catalog for future review and implementation planning. |

## Versioned policy and configuration
Configuration values are **proposed categories**, not approved business rules. A jurisdiction-specific policy must have ID, owner, effective interval, approver, schema/version, audit history and safe default. Pin the applicable version to every transaction or auction; changing a setting does not rewrite existing obligations or accepted bids.

| Category | Representative keys / data | Change owner and controls |
|---|---|---|
| Market | jurisdiction, contracting entity, languages, branch coverage | Legal/product approve activation and legal applicability. |
| Currency and tax | allowed ISO currency, minor-unit exponent, rounding mode, tax jurisdiction and rate source | Finance/legal approve version; exact integer amounts, no floating point. |
| Time and schedules | branch IANA timezone, calendar, holiday, slot length/capacity | Operations authorizes changes; store UTC instant, display local time. |
| Auction | eligibility, opening/closing, bid increment, reserve disclosure, tie, cancellation, seller response and optional extension | DEC-04; legal/commercial approval and pinned version; default optional mechanisms off. |
| Inspection | jurisdiction template, required checks, accepted evidence and correction process | Inspection lead/legal approve version; publication immutable. |
| Dealer access | verification requirements, membership roles, suspension and appeal | Security/commercial jointly approve; active user alone does not grant bidding. |
| Finance | party roles, fee rules, obligation, evidence, provider, reconciliation and refund policies | DEC-02/03; financial dual approval and no default custody. |
| Legal/privacy | contract template version, signature requirements, consent text/version, retention and legal hold | Legal/privacy approve; no universal retention guessed. |
| Notifications | templates, channel, transactional/marketing classification, quiet hours, provider retries | Communications/privacy approve; provider secrets stay in secret manager. |
| Platform | environment, resource limits, timeouts, alerts, feature flags, recovery targets | SRE/security approve; no secret values in repository. |
| SEO/analytics | indexability, canonicals, consent rules, event schema, experiment toggles | SEO/privacy review; private pages remain access-controlled. |

Risky changes require reason, validation, independent approval, scheduled activation, audit and rollback where legally possible. An unset mandatory policy prevents the binding operation; do not fill it from a default meant for a different jurisdiction. Test historical version consistency, time boundaries and unauthorized configuration edits.

## Expanded contract baseline — revision 0.3

[Policy baseline](../POLICY_BASELINE.md) now supplies explicit reversible engineering defaults, validation rules, activation gates and immutable transaction policy pinning.

## Revision 0.3 source of truth

The [current audit](../FINAL_COMPLETENESS_AUDIT.md), [policy baseline](../POLICY_BASELINE.md), [scenario acceptance mappings](../SCENARIO_TRACEABILITY.md) and [API/schema handoff](05_API_AND_SCHEMA_CONTRACTS.md) supersede earlier limited-coverage counts and validation status. Real stakeholder approval, provider evidence and runtime testing are still not claimed.
