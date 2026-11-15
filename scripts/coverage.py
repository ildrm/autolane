"""Dispatch inventory, deliberately separate from feature/test verification."""

import ast
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def update():
    out = ROOT / "docs/implementation"
    spec = json.loads((ROOT / "docs/10_BACKEND_AND_APIS/11_OPENAPI_SPECIFICATION.yaml").read_text())
    explicit, bases, records = set(), set(), set()
    for path in (ROOT / "apps/api/marketplace").glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if (
                isinstance(node, ast.Compare)
                and isinstance(node.left, ast.Name)
                and node.left.id == "op"
            ):
                explicit.update(
                    v.value
                    for v in ast.walk(node)
                    if isinstance(v, ast.Constant) and isinstance(v.value, str)
                )
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict):
                names = {v.id for v in node.targets if isinstance(v, ast.Name)}
                keys = {
                    v.value
                    for v in node.value.keys
                    if isinstance(v, ast.Constant) and isinstance(v.value, str)
                }
                if names & {"direct", "commands", "creators", "OPERATIONS"}:
                    explicit |= keys
                if names & {"MODEL_KINDS", "RECORD_KINDS"}:
                    bases |= keys
                if "RECORD_KINDS" in names:
                    records |= keys
    rows = []
    for path, methods in spec["paths"].items():
        for method, operation in methods.items():
            if not isinstance(operation, dict) or "operationId" not in operation:
                continue
            oid = operation["operationId"]
            base = path.strip("/")
            base = base.rsplit("/", 1)[0] if "{" in base else base
            generic_transition = (
                oid.startswith("transition") and path.strip("/").split("/")[0] in records
            )
            present = oid in explicit or (method == "get" and base in bases) or generic_transition
            status = "implemented_path_unverified" if present else "not_implemented"
            if present and (
                oid.startswith("transition")
                or oid
                in [
                    "readBidCommand",
                    "listBidCommand",
                    "getMetrics",
                    "actOnCampaign",
                    "createConsumerOffer",
                    "acceptConsumerOffer",
                    "recordSignatureEvidence",
                    "recordDeliveryHandover",
                ]
            ):
                status = "partial_unverified"
            if oid in ["ingestProviderEvent", "createSession", "createFinancingApplication"]:
                status = "external_dependency_or_adapter_incomplete"
            rows.append(
                {
                    "operation_id": oid,
                    "method": method.upper(),
                    "path": path,
                    "status": status,
                    "source": "apps/api/marketplace/",
                    "evidence": [],
                }
            )
    (out / "api-coverage.json").write_text(json.dumps(rows, indent=2) + "\n")
    byid = {r["operation_id"]: r["status"] for r in rows}
    requirements = json.loads((out / "requirements.json").read_text())
    for row in requirements:
        present = any(
            byid.get(op) in ["implemented_path_unverified", "partial_unverified"]
            for op in row["related_api"]
        )
        row["status"] = "In progress" if present else "Not started"
        row["implementation"] = (
            ["apps/api/marketplace/", "apps/web/src/components/"] if present else []
        )
    (out / "requirements.json").write_text(json.dumps(requirements, indent=2) + "\n")
    api_counts = dict(Counter(r["status"] for r in rows))
    req_counts = dict(Counter(r["status"] for r in requirements))
    (out / "REQUIREMENTS_COVERAGE.md").write_text(
        "# Requirement coverage\n\n120 scenario requirements: "
        + json.dumps(req_counts)
        + ". **Full scenarios Verified:0**. Focused tests do not establish all acceptance branches.\n\n129 operation dispatch classifications: "
        + json.dumps(api_counts)
        + ". These classify routing code only. Generic transitions, domain guards, projections and full feature behavior still need verification; a dispatch path is not a completed requirement.\n\nRegenerate using `python3 scripts/coverage.py`. Actual executed checks are in evidence/verification.json.\n"
    )
    print(json.dumps({"requirements": req_counts, "api_dispatch": api_counts}))


if __name__ == "__main__":
    update()
