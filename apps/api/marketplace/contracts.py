import json
import re
from django.conf import settings
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from .domain import DomainError

ROOT = settings.BASE_DIR
SPEC = json.loads((ROOT / "docs/10_BACKEND_AND_APIS/11_OPENAPI_SPECIFICATION.yaml").read_text())
MACHINES = {
    m["entity"]: m
    for m in json.loads((ROOT / "docs/contracts/state-machines.json").read_text())["machines"]
}
REGISTRY = Registry().with_resource(
    "urn:autolane:api",
    Resource.from_contents({"$schema": "https://json-schema.org/draft/2020-12/schema", **SPEC}),
)
ROUTES = []
for path, methods in SPEC["paths"].items():
    regex = "^" + re.sub(r"\{(\w+)\}", r"(?P<\1>[^/]+)", path.lstrip("/")) + "$"
    for method, op in methods.items():
        if method in ["get", "post", "delete", "patch", "put"]:
            ROUTES.append((re.compile(regex), method.upper(), op))


def validator(schema):
    return Draft202012Validator(
        {"$ref": "urn:autolane:api", **schema} if not schema else schema,
        registry=REGISTRY,
        format_checker=FormatChecker(),
    ).evolve(schema={"$ref": "urn:autolane:api" + schema["$ref"]} if "$ref" in schema else schema)


def validate_input(op, data):
    schema = op.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema")
    if not schema:
        return
    errors = list(validator(schema).iter_errors(data))
    if errors:
        fields = {".".join(str(p) for p in e.path) or "form": e.message[:250] for e in errors[:10]}
        raise DomainError("validation_error", "Review the highlighted fields.", 422, fields)


def route_match(route, method):
    for pattern, verb, op in ROUTES:
        m = pattern.fullmatch(route)
        if m and verb == method:
            return op, m.groupdict()
    raise DomainError("not_found", "This endpoint is not available.", 404)


def project(schema, value):
    if "$ref" in schema:
        obj = SPEC
        for part in schema["$ref"][2:].split("/"):
            obj = obj[part]
        return project(obj, value)
    if isinstance(value, dict) and schema.get("properties"):
        return {
            k: project(schema["properties"].get(k, {}), v)
            for k, v in value.items()
            if schema.get("additionalProperties") is not False or k in schema["properties"]
        }
    if isinstance(value, list):
        return [project(schema.get("items", {}), v) for v in value]
    return value


def project_response(operation, value, status):
    schema = (
        operation.get("responses", {})
        .get(str(status), {})
        .get("content", {})
        .get("application/json", {})
        .get("schema")
    )
    return project(schema, value) if schema else value
