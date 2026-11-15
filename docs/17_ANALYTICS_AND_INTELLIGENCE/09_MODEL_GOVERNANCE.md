# Model governance

**ID:** 17/09_MODEL_GOVERNANCE · **Version:** 0.1 · **Status:** PROPOSED, subject to privacy, finance and product approval · **Owner:** Head of data · **Reviewers:** Analytics, security, legal, finance, product · **Updated:** 2026-11-15

## Scope and approvals
This plan applies to any automated valuation or prediction, including third-party systems. A model is not approved merely because a technical evaluation succeeds. Product owns intended use, pricing owns economic validity, data science owns evaluation, privacy/security review data and misuse, operations owns override, and an independent reviewer approves deployment. Current launch jurisdiction, data rights, fair-use requirements and any automated-decision restrictions remain **DECISION REQUIRED**.

## Lifecycle and model card
1. Proposal: state intended users, decision supported, prohibited uses, expected benefit, affected groups and human override; identify lawful data sources and retention.
2. Data: document consent or legal basis, provenance, label definitions, date range, coverage, missingness, train/test leakage controls, currency and cohort selection. Do not use sensitive identity or protected characteristics without explicit legal review.
3. Evaluation: use out-of-time holdout, predeclared baseline and segment error/coverage, robustness to missing data, calibration and uncertainty; assess sample size and outcome selection bias. Preserve model version and evaluation artifact.
4. Shadow: generate nonbinding estimates alongside current approved method, compare errors and operational burden; no customer-impacting automation before approval.
5. Approval/release: require signed model card, risk assessment, reproducible artifact and rollback, support explanation, change control, privacy and security gates.
6. Monitor: track quality, drift, data freshness, abstentions, manual overrides and complaints; assign alert thresholds after baseline, review regularly and whenever data/policy shifts.
7. Respond/retire: route low confidence or drift to manual review, suspend harmful model, revert to approved rules, preserve audit and notify affected owners according to incident plan.

## Acceptance and unresolved items
Every output identifies model/rule revision, input/source times, as-of time, confidence and limitations. User-facing copy calls the output an estimate. A human can review and explain adjustments; neither a model nor dashboard authorizes finance, settlement or transaction completion. Backtests must report coverage and uncertainty, and training data must be legally usable. No model, tested accuracy, fairness result or production monitoring is implied by this document.
