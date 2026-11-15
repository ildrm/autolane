# Infrastructure cost model

| Metadata | Value |
|---|---|
| Document ID | 18/09_INFRASTRUCTURE_COSTS |
| Version / status | 0.1 / proposed, not deployed |
| Owner | Cloud Cost Lead |
| Reviewers | Architecture, Security, Finance, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Infrastructure cost model for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [recovery plan](07_BACKUP_AND_RECOVERY.md). |

## Illustrative model

Costs are scenarios, not vendor quotations or financial forecasts. The monthly total is compute + database + storage and backup + CDN egress + networking + queue/search + observability + security + support. Illustrative **USD** planning example: compute 1,500; managed database and replicas 1,200; storage/backups 350; CDN/egress 600; queue/search 450; observability/security 500; networking and other 400 = **USD 5,000/month**. Currency here is a comparison unit, not a target market assumption. Taxes, committed-use discounts, labor, provider transaction fees and regional differences are excluded. Obtain current provider quotes before budget approval.

Sensitivity: a 2× gallery-delivery scenario changes only the assumed CDN/egress line from 600 to 1,200, yielding 5,600/month, all else equal; simultaneous compute and storage growth would increase this further. If observability doubles from 500 to 1,000, the base becomes 5,500. Treat numbers independently rather than adding overlapping scenarios. Attribute costs to environment and service with tags, and distinguish fixed baseline from per-transaction costs.

## Controls and acceptance

Set budget alerts and anomaly detection by environment, region and service; alert on egress, log volume and unused nonproduction capacity. Reduce image sizes or sampling only when quality, retention, audit and security needs remain intact. Monthly review shows assumptions, usage, actual bill, unit cost per completed transaction and variance; do not divide by zero or imply a contribution margin from infrastructure cost alone.
