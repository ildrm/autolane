# API schema and field reference

**ID:** API-SCHEMA-REFERENCE · **Version:** 0.3 · **Status:** generated proposed interface reference · **Owner:** API/data architecture · **Updated:** 2026-11-15

Generated from all168 components.schemas in [OpenAPI](11_OPENAPI_SPECIFICATION.yaml), the authoritative interface source. Required presence differs from nullable value. Field formats are validated; cross-record ownership, exact currency, range comparisons, sequence, independent reviewer and business guards require domain logic in addition. Transport projections are not database migrations.

## BidRequest

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `amount_minor` | Required | `{"type":"integer","format":"int64","minimum":1,"maximum":9007199254740991}` |
| `currency` | Required | `{"type":"string","pattern":"^[A-Z]{3}$","description":"Uppercase ISO 4217 currency code; pattern checks syntax only, service must validate the applicable code and currency exponent."}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## AcceptedBid

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `bid_id` | Required | `{"type":"string","format":"uuid"}` |
| `auction_id` | Required | `{"type":"string","format":"uuid"}` |
| `amount_minor` | Required | `{"type":"integer","format":"int64","minimum":1,"maximum":9007199254740991}` |
| `currency` | Required | `{"type":"string","pattern":"^[A-Z]{3}$","description":"Uppercase ISO 4217 currency code; pattern checks syntax only, service must validate the applicable code and currency exponent."}` |
| `sequence` | Required | `{"type":"integer","minimum":1}` |
| `accepted_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$","description":"RFC 3339 UTC instant with Z suffix."}` |
| `status` | Required | `{"type":"string","const":"accepted"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## AuctionSnapshot

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"type":"string","enum":["cancelled","closed","draft","open","paused","scheduled"]}` |
| `currency` | Required | `{"type":"string","pattern":"^[A-Z]{3}$","description":"Uppercase ISO 4217 currency code; pattern checks syntax only, service must validate the applicable code and currency exponent."}` |
| `current_bid_minor` | Required | `{"type":["integer","null"],"format":"int64","minimum":1,"maximum":9007199254740991}` |
| `sequence` | Required | `{"type":"integer","minimum":0}` |
| `server_time` | Required | `{"type":"string","format":"date-time","pattern":"Z$","description":"RFC 3339 UTC instant with Z suffix."}` |
| `closes_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$","description":"RFC 3339 UTC instant with Z suffix."}` |
| `report_revision_id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `minimum_next_bid_minor` | Required | `{"type":["integer","null"],"minimum":1,"maximum":9007199254740991,"description":"Null when bidding is unavailable or no representable permitted increment remains; client cannot infer availability from amount alone."}` |
| `increment_minor` | Required | `{"type":"integer","minimum":1,"maximum":9007199254740991}` |
| `vehicle` | Required | `{"$ref":"#/components/schemas/PublicVehicle"}` |
| `public_media` | Required | `{"type":"array","maxItems":40,"items":{"$ref":"#/components/schemas/PublishedMedia"}}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## Error

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `error` | Required | `{"type":"object","required":["code","message","retryable","correlation_id"],"properties":{"code":{"type":"string","pattern":"^[A-Z][A-Z0-9_]*$"},"message":{"type":"string"},"retryable":{"type":"boolean"},"correlation_id":{"type":"string"},"field_errors":{"type":"object","additionalProperties":{"type":"string"}}},"additionalProperties":false}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## VehicleInput

Validate year against actual model/catalog and no later than configured market model-year policy; schema 2100 is only a structural bound, not permission to accept an implausible year.

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `make_id` | Required | `{"type":"string","format":"uuid"}` |
| `model_id` | Required | `{"type":"string","format":"uuid"}` |
| `year` | Required | `{"type":"integer","minimum":1886,"maximum":2100}` |
| `mileage` | Required | `{"type":"integer","minimum":0,"maximum":10000000}` |
| `mileage_unit` | Required | `{"type":"string","enum":["km","mi"]}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ContactInput

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `name` | Required | `{"type":"string","minLength":1,"maxLength":500}` |
| `phone` | Required | `{"type":"string","minLength":5,"maxLength":32}` |
| `email` | Optional | `{"type":"string","format":"email","maxLength":254}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ConsentEvidence

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `notice_version` | Required | `{"type":"string","minLength":1,"maxLength":500}` |
| `purpose` | Required | `{"type":"string","minLength":1,"maxLength":500}` |
| `accepted` | Required | `{"type":"boolean","const":true}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## LeadCreate

Authenticated lead submission or anonymous intake bound to a server-managed short-lived draft session. Verified contact and explicit claim establish ownership; knowing lead UUID or a matching email is not sufficient. No existing private lead is disclosed to an unverified contact.

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `vehicle` | Required | `{"$ref":"#/components/schemas/VehicleInput"}` |
| `contact` | Required | `{"$ref":"#/components/schemas/ContactInput"}` |
| `consent` | Required | `{"$ref":"#/components/schemas/ConsentEvidence"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## Lead

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"enum":["draft","submitted","review","eligible","in_progress","closed","cancelled","rejected"]}` |
| `version` | Required | `{"type":"integer","minimum":1}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## Branch

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `name` | Required | `{"type":"string","minLength":1,"maxLength":500}` |
| `city` | Required | `{"type":"string","minLength":1,"maxLength":500}` |
| `timezone` | Required | `{"type":"string","maxLength":64}` |
| `slug` | Optional | `{"type":"string","minLength":1,"maxLength":120}` |
| `address` | Optional | `{"type":"string","minLength":1,"maxLength":500}` |
| `accessibility_summary` | Optional | `{"type":"string","minLength":1,"maxLength":1000}` |
| `public_phone` | Optional | `{"type":"string","pattern":"^\\+[1-9][0-9]{6,14}$"}` |
| `service_status` | Optional | `{"enum":["open","temporarily_closed","appointment_only"]}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## BranchList

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","items":{"$ref":"#/components/schemas/Branch"},"maxItems":100}` |
| `next_cursor` | Required | `{"type":["string","null"]}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## AppointmentCreate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `lead_id` | Required | `{"type":"string","format":"uuid"}` |
| `branch_id` | Required | `{"type":"string","format":"uuid"}` |
| `slot_id` | Required | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## Appointment

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `lead_id` | Required | `{"type":"string","format":"uuid"}` |
| `branch_id` | Required | `{"type":"string","format":"uuid"}` |
| `starts_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$","description":"RFC 3339 UTC instant with Z suffix."}` |
| `timezone` | Required | `{"type":"string","minLength":1,"maxLength":500}` |
| `status` | Required | `{"type":"string","enum":["cancelled","checked_in","completed","confirmed","no_show"]}` |
| `version` | Required | `{"type":"integer","minimum":1}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## Finding

Unknown records an unexamined item, never a pass. Publication must satisfy the approved checklist and review policy.

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `point_id` | Required | `{"type":"string","format":"uuid"}` |
| `result` | Required | `{"type":"string","enum":["pass","defect","not_applicable","unknown"]}` |
| `severity` | Optional | `{"type":["string","null"],"enum":["minor","major","critical",null]}` |
| `comment` | Optional | `{"type":"string","maxLength":2000,"minLength":1}` |
| `evidence_ids` | Optional | `{"type":"array","items":{"type":"string","format":"uuid"},"maxItems":100}` |

Additional schema rules:

```json
{
  "additionalProperties": false,
  "allOf": [
    {
      "if": {
        "properties": {
          "result": {
            "enum": [
              "unknown",
              "not_applicable"
            ]
          }
        },
        "required": [
          "result"
        ]
      },
      "then": {
        "required": [
          "comment"
        ]
      }
    },
    {
      "if": {
        "properties": {
          "result": {
            "const": "defect"
          }
        },
        "required": [
          "result"
        ]
      },
      "then": {
        "required": [
          "severity"
        ],
        "properties": {
          "severity": {
            "enum": [
              "minor",
              "major",
              "critical"
            ]
          }
        }
      }
    }
  ]
}
```

## RevisionCreate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `template_version_id` | Required | `{"type":"string","format":"uuid"}` |
| `findings` | Required | `{"type":"array","items":{"$ref":"#/components/schemas/Finding"},"minItems":1,"maxItems":500}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## Revision

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `inspection_id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"type":"string","enum":["draft","returned","submitted","published","superseded","cancelled"]}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `template_version_id` | Required | `{"type":"string","format":"uuid"}` |
| `findings` | Required | `{"type":"array","minItems":1,"maxItems":500,"items":{"$ref":"#/components/schemas/Finding"}}` |
| `checksum` | Optional | `{"type":"string","pattern":"^[a-f0-9]{64}$"}` |
| `published_at` | Optional | `{"type":"string","format":"date-time","pattern":"Z$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PublishReport

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `revision_id` | Required | `{"type":"string","format":"uuid"}` |
| `reason` | Optional | `{"type":"string","maxLength":1000}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ValuationCreate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `vehicle_id` | Required | `{"type":"string","format":"uuid"}` |
| `report_revision_id` | Required | `{"type":"string","format":"uuid"}` |
| `policy_version_id` | Required | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## Valuation

Indicative estimate; pending review or rejection may omit a range when data is insufficient. All range and currency fields must be present together when a range is provided; an approved valuation requires them. Service validates low_minor <= high_minor and ISO 4217 code.

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"type":"string","enum":["pending_review","approved","rejected"]}` |
| `low_minor` | Optional | `{"type":"integer","format":"int64","minimum":1,"maximum":9007199254740991}` |
| `high_minor` | Optional | `{"type":"integer","format":"int64","minimum":1,"maximum":9007199254740991}` |
| `currency` | Optional | `{"type":"string","pattern":"^[A-Z]{3}$","description":"Uppercase ISO 4217 currency code; pattern checks syntax only, service must validate the applicable code and currency exponent."}` |
| `policy_version_id` | Required | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false,
  "dependentRequired": {
    "low_minor": [
      "high_minor",
      "currency"
    ],
    "high_minor": [
      "low_minor",
      "currency"
    ],
    "currency": [
      "low_minor",
      "high_minor"
    ]
  },
  "allOf": [
    {
      "if": {
        "properties": {
          "status": {
            "const": "approved"
          }
        },
        "required": [
          "status"
        ]
      },
      "then": {
        "required": [
          "low_minor",
          "high_minor",
          "currency"
        ]
      }
    }
  ]
}
```

## AuctionCreate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `vehicle_id` | Required | `{"type":"string","format":"uuid"}` |
| `report_revision_id` | Required | `{"type":"string","format":"uuid"}` |
| `policy_version_id` | Required | `{"type":"string","format":"uuid"}` |
| `starts_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$","description":"RFC 3339 UTC instant with Z suffix."}` |
| `closes_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$","description":"RFC 3339 UTC instant with Z suffix."}` |
| `currency` | Required | `{"type":"string","pattern":"^[A-Z]{3}$","description":"Uppercase ISO 4217 currency code; pattern checks syntax only, service must validate the applicable code and currency exponent."}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## AuctionDraft

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"type":"string","const":"draft"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## CloseRequest

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `reason` | Optional | `{"type":"string","maxLength":1000}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## AuctionResult

Outcome is not seller acceptance, a signed contract, verified settlement or title transfer. Reserve and disqualification handling require approved policy.

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `auction_id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"type":"string","enum":["no_bid","pending_seller_decision","cancelled","no_qualifying_bid","pending_review"]}` |
| `winning_bid_id` | Required | `{"type":["string","null"],"format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |

Additional schema rules:

```json
{
  "additionalProperties": false,
  "allOf": [
    {
      "if": {
        "properties": {
          "status": {
            "const": "pending_seller_decision"
          }
        },
        "required": [
          "status"
        ]
      },
      "then": {
        "properties": {
          "winning_bid_id": {
            "type": "string",
            "format": "uuid"
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "status": {
            "enum": [
              "no_bid",
              "no_qualifying_bid",
              "cancelled"
            ]
          }
        },
        "required": [
          "status"
        ]
      },
      "then": {
        "properties": {
          "winning_bid_id": {
            "type": "null"
          }
        }
      }
    }
  ]
}
```

## SellerDecision

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `decision` | Required | `{"type":"string","enum":["accept","reject"]}` |
| `offer_version` | Required | `{"type":"integer","minimum":1}` |
| `acknowledged` | Required | `{"type":"boolean","const":true}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## DecisionResult

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"type":"string","enum":["accepted","rejected"]}` |
| `recorded_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$","description":"RFC 3339 UTC instant with Z suffix."}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `transaction_id` | Optional | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false,
  "allOf": [
    {
      "if": {
        "properties": {
          "status": {
            "const": "accepted"
          }
        },
        "required": [
          "status"
        ]
      },
      "then": {
        "required": [
          "transaction_id"
        ]
      }
    }
  ]
}
```

## VerificationDecision

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `decision` | Required | `{"type":"string","enum":["approve","reject"]}` |
| `reason` | Required | `{"type":"string","minLength":1,"maxLength":1000}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## VerificationResult

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"type":"string","enum":["approved","needs_evidence","rejected","submitted","suspended","withdrawn"]}` |
| `version` | Required | `{"type":"integer","minimum":1}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## Listing

Approved public projection only. No VIN, contact, exact private location, reserve or draft findings. Sold/unavailable retains truthful status; withdrawn returns generic 404 or approved SEO tombstone. Media URLs belong only to approved public renditions.

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `title` | Required | `{"type":"string","minLength":1,"maxLength":500}` |
| `price_minor` | Required | `{"type":"integer","format":"int64","minimum":1,"maximum":9007199254740991}` |
| `currency` | Required | `{"type":"string","pattern":"^[A-Z]{3}$","description":"Uppercase ISO 4217 currency code; pattern checks syntax only, service must validate the applicable code and currency exponent."}` |
| `status` | Required | `{"enum":["available","unavailable","sold"]}` |
| `slug` | Required | `{"type":"string","pattern":"^[a-z0-9]+(-[a-z0-9]+)*$","maxLength":120}` |
| `revision` | Required | `{"type":"integer","minimum":1}` |
| `vehicle` | Required | `{"$ref":"#/components/schemas/PublicVehicle"}` |
| `media` | Required | `{"type":"array","maxItems":40,"items":{"$ref":"#/components/schemas/PublishedMedia"}}` |
| `region_name` | Required | `{"type":"string","minLength":1,"maxLength":100}` |
| `condition_summary` | Required | `{"type":"string","minLength":1,"maxLength":3000}` |
| `published_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ListingList

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","items":{"$ref":"#/components/schemas/Listing"},"maxItems":100}` |
| `next_cursor` | Required | `{"type":["string","null"]}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PurchaseRequest

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `listing_id` | Required | `{"type":"string","format":"uuid"}` |
| `contact` | Required | `{"$ref":"#/components/schemas/ContactInput"}` |
| `consent` | Required | `{"$ref":"#/components/schemas/ConsentEvidence"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PurchaseRequestResult

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"type":"string","const":"submitted"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## SignatureEvidence

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `document_version_id` | Required | `{"type":"string","format":"uuid"}` |
| `evidence_id` | Required | `{"type":"string","format":"uuid"}` |
| `signer_id` | Required | `{"type":"string","format":"uuid"}` |
| `signed_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$","description":"RFC 3339 UTC instant with Z suffix."}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ContractStatus

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"type":"string","enum":["draft","issued","partially_signed","reviewed","signed","superseded","voided"]}` |
| `version` | Required | `{"type":"integer","minimum":1}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PaymentEvidence

Claimed evidence only; compare parties, amount, currency and independently authenticated provider or bank source before reconciliation. Submission neither moves funds nor confirms settlement.

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `evidence_id` | Required | `{"type":"string","format":"uuid"}` |
| `amount_minor` | Required | `{"type":"integer","format":"int64","minimum":1,"maximum":9007199254740991}` |
| `currency` | Required | `{"type":"string","pattern":"^[A-Z]{3}$","description":"Uppercase ISO 4217 currency code; pattern checks syntax only, service must validate the applicable code and currency exponent."}` |
| `external_reference` | Required | `{"type":"string","maxLength":200,"minLength":1}` |
| `payer_party_id` | Required | `{"type":"string","format":"uuid"}` |
| `payee_party_id` | Required | `{"type":"string","format":"uuid"}` |
| `source_id` | Optional | `{"type":"string","format":"uuid","description":"Provider or bank identity, when recorded; the same external reference is unique within its authoritative source."}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## EvidenceResult

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"type":"string","const":"pending_review"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ReconciliationApprove

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `evidence_ids` | Required | `{"type":"array","minItems":1,"items":{"type":"string","format":"uuid"},"maxItems":100}` |
| `reason` | Required | `{"type":"string","minLength":1,"maxLength":500}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ReconciliationResult

Approval requires independently verified matching evidence and a different authorized approver; it does not by itself prove a legal ownership transfer.

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"type":"string","const":"reconciled"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## Handover

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `condition` | Required | `{"type":"string","maxLength":2000,"minLength":1}` |
| `evidence_ids` | Required | `{"type":"array","minItems":1,"items":{"type":"string","format":"uuid"},"maxItems":100}` |
| `occurred_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$","description":"RFC 3339 UTC instant with Z suffix."}` |
| `kind` | Required | `{"enum":["pickup","delivery"]}` |
| `from_party_id` | Required | `{"type":"string","format":"uuid"}` |
| `to_party_id` | Required | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## DeliveryStatus

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"type":"string","enum":["assigned","cancelled","collected","delivered","exception","in_transit","scheduled"]}` |
| `version` | Required | `{"type":"integer","minimum":1}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## TicketCreate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `case_id` | Optional | `{"type":"string","format":"uuid"}` |
| `subject` | Required | `{"type":"string","minLength":1,"maxLength":500}` |
| `description` | Required | `{"type":"string","minLength":1,"maxLength":5000}` |
| `evidence_ids` | Optional | `{"type":"array","items":{"type":"string","format":"uuid"},"maxItems":100}` |
| `category` | Required | `{"enum":["transaction","inspection","privacy","security","general"]}` |

Additional schema rules:

```json
{
  "additionalProperties": false,
  "allOf": [
    {
      "if": {
        "properties": {
          "category": {
            "enum": [
              "transaction",
              "inspection"
            ]
          }
        }
      },
      "then": {
        "required": [
          "case_id"
        ]
      }
    }
  ]
}
```

## Ticket

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"type":"string","enum":["assigned","awaiting_customer","closed","investigating","open","resolved"]}` |
| `version` | Required | `{"type":"integer","minimum":1}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PolicyDraft

Only these policy types are supported by this command version. Additional policy categories require their own reviewed schema and are rejected rather than accepted as arbitrary JSON. Legal approval remains required before activation.

Additional schema rules:

```json
{
  "oneOf": [
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "type": {
          "const": "auction"
        },
        "content": {
          "$ref": "#/components/schemas/AuctionPolicy"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        }
      },
      "required": [
        "type",
        "content",
        "reason"
      ]
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "type": {
          "const": "finance"
        },
        "content": {
          "$ref": "#/components/schemas/FinancePolicy"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        }
      },
      "required": [
        "type",
        "content",
        "reason"
      ]
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "type": {
          "const": "retention"
        },
        "content": {
          "$ref": "#/components/schemas/RetentionPolicy"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        }
      },
      "required": [
        "type",
        "content",
        "reason"
      ]
    }
  ]
}
```

## PolicyVersion

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"type":"string","const":"pending_approval"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## MetricList

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","items":{"type":"object","additionalProperties":false,"properties":{"name":{"type":"string","minLength":1,"maxLength":500},"value":{"type":"number"},"period_start":{"type":"string","format":"date-time","pattern":"Z$","description":"RFC 3339 UTC instant with Z suffix."},"period_end":{"type":"string","format":"date-time","pattern":"Z$","description":"RFC 3339 UTC instant with Z suffix."},"definition_version":{"type":"string","minLength":1,"maxLength":500}},"required":["name","value","period_start","period_end","definition_version"]},"maxItems":100}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## SessionCreate

Identity assertion must be issuer/audience/nonce verified by backend; opaque provider assertion alone is never trusted from a client.

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `provider_assertion` | Required | `{"type":"string","minLength":1,"maxLength":8192}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## SessionResult

If mfa_required is true this is a pending authentication context, not an authorized session. expires_at then denotes the pending context expiry; the MFA challenge contract is not specified here.

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `user_id` | Required | `{"type":"string","format":"uuid"}` |
| `expires_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$","description":"RFC 3339 UTC instant with Z suffix."}` |
| `mfa_required` | Required | `{"type":"boolean"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## SellerLeadRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"type":"string","enum":["cancelled","closed","draft","eligible","in_progress","rejected","review","submitted"]}` |
| `seller_id` | Optional | `{"type":"string","format":"uuid"}` |
| `vehicle_id` | Optional | `{"type":"string","format":"uuid"}` |
| `notice_version` | Optional | `{"type":"string","minLength":1,"maxLength":200}` |
| `assigned_to` | Optional | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## SellerLeadPage

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/SellerLeadRecord"}}` |
| `next_cursor` | Required | `{"type":["string","null"],"maxLength":1024}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## SellerLeadTransition

Additional schema rules:

```json
{
  "oneOf": [
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "submit"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-01-01 \u2014 ROLE-002; Verified contact, supported taxonomy, service notice acknowledged. Freeze intake revision; enqueue qualification",
      "x-transition-id": "SM-01-01"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "qualify"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-01-02 \u2014 ROLE-011; Authority and eligibility evidence checked under pinned policy. Record reviewer and eligibility reasons",
      "x-transition-id": "SM-01-02"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "request-review"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-01-03 \u2014 ROLE-011; Duplicate or authority conflict documented. Prevent booking/publication until resolved",
      "x-transition-id": "SM-01-03"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "start-case"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-01-04 \u2014 ROLE-006; Confirmed appointment and verified seller scope. Link appointment and inspection work to the SellerLead; no TransactionCase exists until a current offer is accepted",
      "x-transition-id": "SM-01-04"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "reject"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-01-05 \u2014 ROLE-011; Reason and support route supplied. Notify owner without exposing duplicate identities",
      "x-transition-id": "SM-01-05"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "cancel"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-01-06 \u2014 ROLE-002; Own case and no live binding obligation. Release future booking through idempotent scheduling command",
      "x-transition-id": "SM-01-06"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "close"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-01-07 \u2014 ROLE-006; Verified completed transaction outcome or explicit unsuccessful/withdrawn selling outcome with no unresolved obligation. Record outcome, never infer financial success",
      "x-transition-id": "SM-01-07"
    }
  ]
}
```

## AppointmentRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"type":"string","enum":["cancelled","checked_in","completed","confirmed","no_show"]}` |
| `lead_id` | Optional | `{"type":"string","format":"uuid"}` |
| `branch_id` | Optional | `{"type":"string","format":"uuid"}` |
| `slot_id` | Optional | `{"type":"string","format":"uuid"}` |
| `starts_at` | Optional | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `ends_at` | Optional | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `timezone` | Optional | `{"type":"string","minLength":1,"maxLength":200}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## AppointmentPage

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/AppointmentRecord"}}` |
| `next_cursor` | Required | `{"type":["string","null"],"maxLength":1024}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## AppointmentTransition

Additional schema rules:

```json
{
  "oneOf": [
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "reschedule"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "slot_id": {
          "type": "string",
          "format": "uuid"
        }
      },
      "required": [
        "action",
        "reason",
        "slot_id"
      ],
      "description": "SM-02-01 \u2014 ROLE-002; Own case, new slot valid, capacity and notice policy checked. Lock old/new slots in sorted ID order and move reservation atomically",
      "x-transition-id": "SM-02-01"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "cancel"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-02-02 \u2014 ROLE-002; Own case and cancellation policy allows action. Release reservation exactly once; create notification intent",
      "x-transition-id": "SM-02-02"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "check-in"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-02-03 \u2014 ROLE-006; Assigned branch verifies booking, vehicle and arrival. Record check-in instant and queue position",
      "x-transition-id": "SM-02-03"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "mark-no-show"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-02-04 \u2014 ROLE-006; Grace interval elapsed in branch calendar, branch was open. Record no-show reason; capacity/history retained",
      "x-transition-id": "SM-02-04"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "complete"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-02-05 \u2014 ROLE-006; Inspection handoff recorded. Complete visit without asserting sale or report approval",
      "x-transition-id": "SM-02-05"
    }
  ]
}
```

## InspectionRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"type":"string","enum":["cancelled","draft","published","returned","submitted"]}` |
| `vehicle_id` | Optional | `{"type":"string","format":"uuid"}` |
| `branch_id` | Optional | `{"type":"string","format":"uuid"}` |
| `inspector_id` | Optional | `{"type":"string","format":"uuid"}` |
| `template_version_id` | Optional | `{"type":"string","format":"uuid"}` |
| `current_revision_id` | Optional | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## InspectionPage

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/InspectionRecord"}}` |
| `next_cursor` | Required | `{"type":["string","null"],"maxLength":1024}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## InspectionTransition

Additional schema rules:

```json
{
  "oneOf": [
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "submit"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "revision_id": {
          "type": "string",
          "format": "uuid"
        }
      },
      "required": [
        "action",
        "reason",
        "revision_id"
      ],
      "description": "SM-03-01 \u2014 ROLE-007; All required points explicitly answered; unknown and N/A have reasons; clean evidence. Freeze submitted revision and assign independent reviewer",
      "x-transition-id": "SM-03-01"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "return"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-03-02 \u2014 ROLE-008; Reviewer differs from author and provides point-level reasons. Create correction task; no published content changes",
      "x-transition-id": "SM-03-02"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "publish"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "revision_id": {
          "type": "string",
          "format": "uuid"
        }
      },
      "required": [
        "action",
        "reason",
        "revision_id"
      ],
      "description": "SM-03-03 \u2014 ROLE-008; Mandatory coverage passes template; reviewer independent; clean immutable evidence. Publish revision and emit inspection.report_published",
      "x-transition-id": "SM-03-03"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "correct"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "revision_id": {
          "type": "string",
          "format": "uuid"
        }
      },
      "required": [
        "action",
        "reason",
        "revision_id"
      ],
      "description": "SM-03-04 \u2014 ROLE-008; Reason, materiality and new revision recorded; existing report retained. Create successor revision; material change sets linked auction safety hold",
      "x-transition-id": "SM-03-04"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "cancel"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-03-05 \u2014 ROLE-008; No active auction relies on draft; reason recorded. Retain audit and prevent publication",
      "x-transition-id": "SM-03-05"
    }
  ]
}
```

## VehicleListingRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"type":"string","enum":["available","draft","review","sold","unavailable","withdrawn"]}` |
| `vehicle_id` | Optional | `{"type":"string","format":"uuid"}` |
| `title` | Optional | `{"type":"string","minLength":1,"maxLength":200}` |
| `price_minor` | Optional | `{"type":"integer","minimum":0,"maximum":9007199254740991}` |
| `currency` | Optional | `{"type":"string","pattern":"^[A-Z]{3}$"}` |
| `published_revision_id` | Optional | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## VehicleListingPage

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/VehicleListingRecord"}}` |
| `next_cursor` | Required | `{"type":["string","null"],"maxLength":1024}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## VehicleListingTransition

Additional schema rules:

```json
{
  "oneOf": [
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "submit"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-04-01 \u2014 ROLE-021; Seller authority, rights-cleared media, condition and price fields complete. Freeze publication candidate separate from dealer report",
      "x-transition-id": "SM-04-01"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "publish"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-04-02 \u2014 ROLE-021; Publication grant; no active dealer-auction channel conflict. Publish only approved projection and invalidate search",
      "x-transition-id": "SM-04-02"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "suspend"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-04-03 \u2014 ROLE-021; Ownership, condition or availability question documented. Remove from active search; preserve buyer inquiries",
      "x-transition-id": "SM-04-03"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "restore"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-04-04 \u2014 ROLE-021; Blocking issue resolved and authority still valid. Refresh public revision and searchable availability",
      "x-transition-id": "SM-04-04"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "mark-sold"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-04-05 \u2014 ROLE-021; Completed transaction or independently verified external disposition. Display sold status; remove inquiry CTA",
      "x-transition-id": "SM-04-05"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "withdraw"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-04-06 \u2014 ROLE-021; Authorized owner request or legal reason. Unpublish with lifecycle SEO policy; retain audit",
      "x-transition-id": "SM-04-06"
    }
  ]
}
```

## ValuationRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"type":"string","enum":["approved","pending_review","rejected"]}` |
| `vehicle_id` | Optional | `{"type":"string","format":"uuid"}` |
| `report_revision_id` | Optional | `{"type":"string","format":"uuid"}` |
| `policy_version_id` | Optional | `{"type":"string","format":"uuid"}` |
| `currency` | Optional | `{"type":"string","pattern":"^[A-Z]{3}$"}` |
| `low_minor` | Optional | `{"type":"integer","minimum":0,"maximum":9007199254740991}` |
| `high_minor` | Optional | `{"type":"integer","minimum":0,"maximum":9007199254740991}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ValuationPage

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/ValuationRecord"}}` |
| `next_cursor` | Required | `{"type":["string","null"],"maxLength":1024}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ValuationTransition

Additional schema rules:

```json
{
  "oneOf": [
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "approve"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-05-01 \u2014 ROLE-009; Approved source rights, currency-consistent range, sufficient data and independent override reviewer. Pin input/report/rule versions and explanation",
      "x-transition-id": "SM-05-01"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "reject"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-05-02 \u2014 ROLE-009; Insufficient comparables or invalid inputs with reason. Publish abstention, never fabricate zero price",
      "x-transition-id": "SM-05-02"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "revise"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-05-03 \u2014 ROLE-009; New report/comparables or override reason; retain earlier valuation. Create successor valuation revision; active auctions unchanged",
      "x-transition-id": "SM-05-03"
    }
  ]
}
```

## AuctionRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"type":"string","enum":["cancelled","closed","draft","open","paused","scheduled"]}` |
| `vehicle_id` | Optional | `{"type":"string","format":"uuid"}` |
| `report_revision_id` | Optional | `{"type":"string","format":"uuid"}` |
| `policy_version_id` | Optional | `{"type":"string","format":"uuid"}` |
| `starts_at` | Optional | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `closes_at` | Optional | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `currency` | Optional | `{"type":"string","pattern":"^[A-Z]{3}$"}` |
| `current_bid_minor` | Optional | `{"type":["integer","null"],"minimum":1,"maximum":9007199254740991}` |
| `sequence` | Optional | `{"type":"integer","minimum":0}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## AuctionPage

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/AuctionRecord"}}` |
| `next_cursor` | Required | `{"type":["string","null"],"maxLength":1024}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## AuctionTransition

Additional schema rules:

```json
{
  "oneOf": [
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "schedule"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "starts_at": {
          "type": "string",
          "format": "date-time",
          "pattern": "Z$"
        },
        "closes_at": {
          "type": "string",
          "format": "date-time",
          "pattern": "Z$"
        },
        "policy_version_id": {
          "type": "string",
          "format": "uuid"
        }
      },
      "required": [
        "action",
        "reason",
        "starts_at",
        "closes_at",
        "policy_version_id"
      ],
      "description": "SM-06-01 \u2014 ROLE-010; Published report, seller authority, approved pinned rules, valid time interval, exclusive vehicle channel. Freeze schedule/rules/report snapshot and audience",
      "x-transition-id": "SM-06-01"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "open"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-06-02 \u2014 SYSTEM-AUCTION; Trusted DB time reaches starts_at; report, vehicle and policy still valid. Emit auction.opened after commit",
      "x-transition-id": "SM-06-02"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "pause"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-06-03 \u2014 ROLE-010; Material safety issue or incident; recorded reason and case. Reject new bids, preserve deadline and bid history",
      "x-transition-id": "SM-06-03"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "resume"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-06-04 \u2014 ROLE-010; Safety issue resolved, prepublished policy allows resume and original deadline not passed. Record review, never reset or extend deadline silently",
      "x-transition-id": "SM-06-04"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "close"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-06-05 \u2014 SYSTEM-AUCTION; DB time reaches deadline; same auction lock; paused/uncertain case yields pending_review result. Insert unique result and auction.closed atomically",
      "x-transition-id": "SM-06-05"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "cancel"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-06-06 \u2014 ROLE-010; Authorized reason and approvals per pinned policy. Preserve all bids, cancel without automatic financial penalty",
      "x-transition-id": "SM-06-06"
    }
  ]
}
```

## BidCommandRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"type":"string","enum":["accepted","received","rejected"]}` |
| `auction_id` | Optional | `{"type":"string","format":"uuid"}` |
| `actor_id` | Optional | `{"type":"string","format":"uuid"}` |
| `decision_code` | Optional | `{"type":"string","minLength":1,"maxLength":200}` |
| `bid_id` | Optional | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## BidCommandPage

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/BidCommandRecord"}}` |
| `next_cursor` | Required | `{"type":["string","null"],"maxLength":1024}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## DealerVerificationRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"type":"string","enum":["approved","needs_evidence","rejected","submitted","suspended"]}` |
| `organization_id` | Optional | `{"type":"string","format":"uuid"}` |
| `reviewer_id` | Optional | `{"type":"string","format":"uuid"}` |
| `evidence_ids` | Optional | `{"type":"array","items":{"type":"string","format":"uuid"},"minItems":1,"maxItems":100,"uniqueItems":true}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## DealerVerificationPage

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/DealerVerificationRecord"}}` |
| `next_cursor` | Required | `{"type":["string","null"],"maxLength":1024}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## DealerVerificationTransition

Additional schema rules:

```json
{
  "oneOf": [
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "request-evidence"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-08-01 \u2014 ROLE-019; Missing verification item specified. Notify applicant, preserve received evidence",
      "x-transition-id": "SM-08-01"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "resubmit"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-08-02 \u2014 ROLE-005; Authorized organization representative; clean evidence. Version submission and reset review assignment",
      "x-transition-id": "SM-08-02"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "approve"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-08-03 \u2014 ROLE-019; Independent reviewer verifies business and representative authority. Activate dealer account; do not grant every member bid authority",
      "x-transition-id": "SM-08-03"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "reject"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-08-04 \u2014 ROLE-019; Evidence-based reason and appeal instructions. Disable auction access, retain decision",
      "x-transition-id": "SM-08-04"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "suspend"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-08-05 \u2014 ROLE-019; Risk/contract reason and case; step-up required. Lock same eligibility record used by bidding; revoke active feed subscriptions",
      "x-transition-id": "SM-08-05"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "reinstate"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-08-06 \u2014 ROLE-019; Independent risk review clears restriction. Restore eligible access prospectively; retain old decisions",
      "x-transition-id": "SM-08-06"
    }
  ]
}
```

## PurchaseRequestRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"type":"string","enum":["assigned","cancelled","closed","coordinating","qualified","submitted"]}` |
| `buyer_id` | Optional | `{"type":"string","format":"uuid"}` |
| `listing_id` | Optional | `{"type":"string","format":"uuid"}` |
| `advisor_id` | Optional | `{"type":"string","format":"uuid"}` |
| `transaction_id` | Optional | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PurchaseRequestPage

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/PurchaseRequestRecord"}}` |
| `next_cursor` | Required | `{"type":["string","null"],"maxLength":1024}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PurchaseRequestTransition

Additional schema rules:

```json
{
  "oneOf": [
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "assign"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "assignee_id": {
          "type": "string",
          "format": "uuid"
        }
      },
      "required": [
        "action",
        "reason",
        "assignee_id"
      ],
      "description": "SM-09-01 \u2014 ROLE-011; Available scoped advisor and authoritative listing check. Set owner and next contact due time",
      "x-transition-id": "SM-09-01"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "qualify"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-09-02 \u2014 ROLE-011; Buyer needs and availability confirmed. Record requirements and next action; no reservation implied",
      "x-transition-id": "SM-09-02"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "coordinate"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-09-03 \u2014 ROLE-011; Buyer selects vehicle and appropriate contract path. Link transaction case; separate consumer/dealer paths",
      "x-transition-id": "SM-09-03"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "cancel"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-09-04 \u2014 ROLE-003; Own request and obligations handled by legal case if necessary. Stop further optional sourcing; retain lawful evidence",
      "x-transition-id": "SM-09-04"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "close"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-09-05 \u2014 ROLE-011; Transaction outcome or explicit unsuccessful disposition recorded. Record closure category; notify buyer",
      "x-transition-id": "SM-09-05"
    }
  ]
}
```

## FinancingApplicationRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"type":"string","enum":["approved","draft","expired","funded","rejected","submitted","withdrawn"]}` |
| `party_id` | Optional | `{"type":"string","format":"uuid"}` |
| `provider_id` | Optional | `{"type":"string","format":"uuid"}` |
| `consent_id` | Optional | `{"type":"string","format":"uuid"}` |
| `provider_reference` | Optional | `{"type":"string","minLength":1,"maxLength":200}` |
| `expires_at` | Optional | `{"type":"string","format":"date-time","pattern":"Z$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## FinancingApplicationPage

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/FinancingApplicationRecord"}}` |
| `next_cursor` | Required | `{"type":["string","null"],"maxLength":1024}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## FinancingApplicationTransition

Additional schema rules:

```json
{
  "oneOf": [
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "submit"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-10-01 \u2014 ROLE-003; Approved lender, explicit sharing basis and required application fields. Create provider intent, not credit approval",
      "x-transition-id": "SM-10-01"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "withdraw"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-10-06 \u2014 ROLE-003; Applicant request; contracted obligations escalated if already binding. Stop future optional sharing; retain required evidence",
      "x-transition-id": "SM-10-06"
    }
  ]
}
```

## ContractRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"type":"string","enum":["draft","issued","partially_signed","reviewed","signed","superseded","voided"]}` |
| `transaction_id` | Optional | `{"type":"string","format":"uuid"}` |
| `template_version_id` | Optional | `{"type":"string","format":"uuid"}` |
| `document_revision_id` | Optional | `{"type":"string","format":"uuid"}` |
| `document_hash` | Optional | `{"type":"string","pattern":"^[a-f0-9]{64}$"}` |
| `required_signer_ids` | Optional | `{"type":"array","items":{"type":"string","format":"uuid"},"minItems":1,"maxItems":100,"uniqueItems":true}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ContractPage

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/ContractRecord"}}` |
| `next_cursor` | Required | `{"type":["string","null"],"maxLength":1024}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ContractTransition

Additional schema rules:

```json
{
  "oneOf": [
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "review"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "document_revision_id": {
          "type": "string",
          "format": "uuid"
        }
      },
      "required": [
        "action",
        "reason",
        "document_revision_id"
      ],
      "description": "SM-11-01 \u2014 ROLE-012; Approved jurisdiction template, parties, amounts, fees and title process. Pin reviewed document checksum",
      "x-transition-id": "SM-11-01"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "issue"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "document_revision_id": {
          "type": "string",
          "format": "uuid"
        }
      },
      "required": [
        "action",
        "reason",
        "document_revision_id"
      ],
      "description": "SM-11-02 \u2014 ROLE-012; Required signers and authority verified; exact reviewed version unchanged. Issue signing invitations with expiring authorized access",
      "x-transition-id": "SM-11-02"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "record-signature"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "document_revision_id": {
          "type": "string",
          "format": "uuid"
        },
        "signer_id": {
          "type": "string",
          "format": "uuid"
        },
        "signed_at": {
          "type": "string",
          "format": "date-time",
          "pattern": "Z$"
        }
      },
      "required": [
        "action",
        "reason",
        "document_revision_id",
        "signer_id",
        "signed_at"
      ],
      "description": "SM-11-03 \u2014 ROLE-012; One verified signer on exact document hash; other required signers outstanding. Append signature evidence; never overwrite document",
      "x-transition-id": "SM-11-03"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "complete-signatures"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "document_revision_id": {
          "type": "string",
          "format": "uuid"
        }
      },
      "required": [
        "action",
        "reason",
        "document_revision_id"
      ],
      "description": "SM-11-04 \u2014 ROLE-012; All required valid signatures refer to same document hash. Emit contract.signed; does not imply settlement",
      "x-transition-id": "SM-11-04"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "void"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-11-05 \u2014 ROLE-012; Approved legal basis and notice obligations recorded. Revoke unsigned invitations; preserve all signatures",
      "x-transition-id": "SM-11-05"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "amend"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "document_revision_id": {
          "type": "string",
          "format": "uuid"
        }
      },
      "required": [
        "action",
        "reason",
        "document_revision_id"
      ],
      "description": "SM-11-06 \u2014 ROLE-012; Authorized amendment process and newly executed successor. Retain old agreement linked to replacement",
      "x-transition-id": "SM-11-06"
    }
  ]
}
```

## PaymentObligationRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"type":"string","enum":["disputed","evidence_pending","outstanding","partially_satisfied","reconciled","voided"]}` |
| `transaction_id` | Optional | `{"type":"string","format":"uuid"}` |
| `payer_party_id` | Optional | `{"type":"string","format":"uuid"}` |
| `payee_party_id` | Optional | `{"type":"string","format":"uuid"}` |
| `amount_minor` | Optional | `{"type":"integer","minimum":0,"maximum":9007199254740991}` |
| `matched_minor` | Optional | `{"type":"integer","minimum":0,"maximum":9007199254740991}` |
| `currency` | Optional | `{"type":"string","pattern":"^[A-Z]{3}$"}` |
| `due_at` | Optional | `{"type":"string","format":"date-time","pattern":"Z$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PaymentObligationPage

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/PaymentObligationRecord"}}` |
| `next_cursor` | Required | `{"type":["string","null"],"maxLength":1024}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PaymentObligationTransition

Additional schema rules:

```json
{
  "oneOf": [
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "submit-evidence"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "amount_minor": {
          "type": "integer",
          "minimum": 0,
          "maximum": 9007199254740991
        },
        "currency": {
          "type": "string",
          "pattern": "^[A-Z]{3}$"
        },
        "source_reference": {
          "type": "string",
          "minLength": 1,
          "maxLength": 200
        }
      },
      "required": [
        "action",
        "reason",
        "evidence_ids",
        "amount_minor",
        "currency",
        "source_reference"
      ],
      "description": "SM-12-01 \u2014 ROLE-013; Clean evidence references known payer/payee, source, amount and currency. Record claimed payment; no transfer or settled flag",
      "x-transition-id": "SM-12-01"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "record-partial"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "amount_minor": {
          "type": "integer",
          "minimum": 0,
          "maximum": 9007199254740991
        },
        "currency": {
          "type": "string",
          "pattern": "^[A-Z]{3}$"
        },
        "source_reference": {
          "type": "string",
          "minLength": 1,
          "maxLength": 200
        }
      },
      "required": [
        "action",
        "reason",
        "evidence_ids",
        "amount_minor",
        "currency",
        "source_reference"
      ],
      "description": "SM-12-02 \u2014 ROLE-014; Independent matching confirms part of exact obligation. Record matched allocation and remaining balance",
      "x-transition-id": "SM-12-02"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "dispute"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-12-03 \u2014 ROLE-014; Mismatch, duplicate allocation or uncertain finality. Assign exception and prohibit closure",
      "x-transition-id": "SM-12-03"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "reconcile"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "amount_minor": {
          "type": "integer",
          "minimum": 0,
          "maximum": 9007199254740991
        },
        "currency": {
          "type": "string",
          "pattern": "^[A-Z]{3}$"
        },
        "source_reference": {
          "type": "string",
          "minLength": 1,
          "maxLength": 200
        }
      },
      "required": [
        "action",
        "reason",
        "evidence_ids",
        "amount_minor",
        "currency",
        "source_reference"
      ],
      "description": "SM-12-04 \u2014 ROLE-014; Independent reviewer, exact approved total, authentic source, no unresolved reversal. Record reconciliation and settlement.reconciled",
      "x-transition-id": "SM-12-04"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "record-reversal"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "amount_minor": {
          "type": "integer",
          "minimum": 0,
          "maximum": 9007199254740991
        },
        "currency": {
          "type": "string",
          "pattern": "^[A-Z]{3}$"
        },
        "source_reference": {
          "type": "string",
          "minLength": 1,
          "maxLength": 200
        }
      },
      "required": [
        "action",
        "reason",
        "evidence_ids",
        "amount_minor",
        "currency",
        "source_reference"
      ],
      "description": "SM-12-05 \u2014 ROLE-014; New authenticated reversal evidence. Append compensating fact, reopen financial exception; never erase history",
      "x-transition-id": "SM-12-05"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "void"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-12-06 \u2014 ROLE-014; Underlying obligation legally cancelled; no unhandled payment. Preserve reason and source approval",
      "x-transition-id": "SM-12-06"
    }
  ]
}
```

## DeliveryRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"type":"string","enum":["assigned","cancelled","collected","delivered","exception","in_transit","scheduled"]}` |
| `transaction_id` | Optional | `{"type":"string","format":"uuid"}` |
| `carrier_id` | Optional | `{"type":"string","format":"uuid"}` |
| `pickup_at` | Optional | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `current_custodian_id` | Optional | `{"type":"string","format":"uuid"}` |
| `proof_ids` | Optional | `{"type":"array","items":{"type":"string","format":"uuid"},"minItems":1,"maxItems":100,"uniqueItems":true}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## DeliveryPage

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/DeliveryRecord"}}` |
| `next_cursor` | Required | `{"type":["string","null"],"maxLength":1024}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## DeliveryTransition

Additional schema rules:

```json
{
  "oneOf": [
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "assign"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "assignee_id": {
          "type": "string",
          "format": "uuid"
        }
      },
      "required": [
        "action",
        "reason",
        "assignee_id"
      ],
      "description": "SM-13-01 \u2014 ROLE-020; Qualified carrier, coverage, window and pickup authority. Share minimal job information with assigned carrier",
      "x-transition-id": "SM-13-01"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "collect"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "occurred_at": {
          "type": "string",
          "format": "date-time",
          "pattern": "Z$"
        }
      },
      "required": [
        "action",
        "reason",
        "evidence_ids",
        "occurred_at"
      ],
      "description": "SM-13-02 \u2014 ROLE-018; Pickup authority, condition, signed proof and custody verified. Append custody event and immutable condition evidence",
      "x-transition-id": "SM-13-02"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "dispatch"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-13-03 \u2014 ROLE-020; Carrier acceptance and destination details validated. Record dispatch and estimated window",
      "x-transition-id": "SM-13-03"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "deliver"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "occurred_at": {
          "type": "string",
          "format": "date-time",
          "pattern": "Z$"
        }
      },
      "required": [
        "action",
        "reason",
        "evidence_ids",
        "occurred_at"
      ],
      "description": "SM-13-04 \u2014 ROLE-018; Authorized recipient proof, condition and time recorded. Record physical handover only",
      "x-transition-id": "SM-13-04"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "report-exception"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-13-05 \u2014 ROLE-020; Delay, damage or failed attempt has evidence and current custodian. Assign claims/dispatch owner; preserve custody",
      "x-transition-id": "SM-13-05"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "reschedule"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "pickup_at": {
          "type": "string",
          "format": "date-time",
          "pattern": "Z$"
        },
        "carrier_id": {
          "type": "string",
          "format": "uuid"
        }
      },
      "required": [
        "action",
        "reason",
        "pickup_at",
        "carrier_id"
      ],
      "description": "SM-13-06 \u2014 ROLE-020; New agreed window and verified custody/insurance. Create new attempt; retain failed attempt",
      "x-transition-id": "SM-13-06"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "cancel"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-13-07 \u2014 ROLE-020; Vehicle not collected and authorized cancellation. Notify participants; no implied fee refund",
      "x-transition-id": "SM-13-07"
    }
  ]
}
```

## WarrantyClaimRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"type":"string","enum":["approved","closed","denied","needs_evidence","received","under_review"]}` |
| `transaction_id` | Optional | `{"type":"string","format":"uuid"}` |
| `policy_version_id` | Optional | `{"type":"string","format":"uuid"}` |
| `claimant_id` | Optional | `{"type":"string","format":"uuid"}` |
| `reviewer_id` | Optional | `{"type":"string","format":"uuid"}` |
| `evidence_ids` | Optional | `{"type":"array","items":{"type":"string","format":"uuid"},"minItems":1,"maxItems":100,"uniqueItems":true}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## WarrantyClaimPage

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/WarrantyClaimRecord"}}` |
| `next_cursor` | Required | `{"type":["string","null"],"maxLength":1024}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## WarrantyClaimTransition

Additional schema rules:

```json
{
  "oneOf": [
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "request-evidence"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-14-01 \u2014 ROLE-022; Applicable policy/version and missing evidence identified. Record next action and notice; original claim time retained",
      "x-transition-id": "SM-14-01"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "review"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-14-02 \u2014 ROLE-022; Required evidence available; independent reviewer assigned. Preserve report, policy and transaction snapshots",
      "x-transition-id": "SM-14-02"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "approve"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-14-03 \u2014 ROLE-022; Coverage, liability and proposed remedy supported by approved policy. Create remedy proposal; finance separately authorizes money",
      "x-transition-id": "SM-14-03"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "deny"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-14-04 \u2014 ROLE-022; Reason and applicable appeal path supplied. Record reasoned decision without deleting evidence",
      "x-transition-id": "SM-14-04"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "complete-remedy"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "occurred_at": {
          "type": "string",
          "format": "date-time",
          "pattern": "Z$"
        }
      },
      "required": [
        "action",
        "reason",
        "evidence_ids",
        "occurred_at"
      ],
      "description": "SM-14-05 \u2014 ROLE-022; Authorized remedy completion independently confirmed. Close with remedy evidence and notification",
      "x-transition-id": "SM-14-05"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "appeal"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-14-06 \u2014 ROLE-022; Appeal admissible under policy; independent new reviewer. Create linked review cycle; prior decision remains",
      "x-transition-id": "SM-14-06"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "close"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-14-07 \u2014 ROLE-022; Applicable appeal handling completed. Record closure and evidence retention policy",
      "x-transition-id": "SM-14-07"
    }
  ]
}
```

## SupportTicketRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"type":"string","enum":["assigned","awaiting_customer","closed","investigating","open","resolved"]}` |
| `requester_id` | Optional | `{"type":"string","format":"uuid"}` |
| `subject` | Optional | `{"type":"string","minLength":1,"maxLength":200}` |
| `description` | Optional | `{"type":"string","minLength":1,"maxLength":2000}` |
| `assigned_to` | Optional | `{"type":"string","format":"uuid"}` |
| `case_id` | Optional | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## SupportTicketPage

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/SupportTicketRecord"}}` |
| `next_cursor` | Required | `{"type":["string","null"],"maxLength":1024}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## SupportTicketTransition

Additional schema rules:

```json
{
  "oneOf": [
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "assign"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        },
        "assignee_id": {
          "type": "string",
          "format": "uuid"
        }
      },
      "required": [
        "action",
        "reason",
        "assignee_id"
      ],
      "description": "SM-15-01 \u2014 ROLE-011; Available authorized team member. Set owner and response target",
      "x-transition-id": "SM-15-01"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "investigate"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-15-02 \u2014 ROLE-011; Verified customer and minimum necessary case access. Record evidence request and investigation log",
      "x-transition-id": "SM-15-02"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "wait-customer"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-15-03 \u2014 ROLE-011; Specific information request and follow-up date. Pause only approved resolution clock; not initial response",
      "x-transition-id": "SM-15-03"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "resume"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-15-04 \u2014 ROLE-011; Customer evidence received or staff follow-up. Resume clock and preserve waiting interval",
      "x-transition-id": "SM-15-04"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "resolve"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-15-05 \u2014 ROLE-011; Reasoned resolution recorded; domain actions confirmed independently. Notify with appeal/reopen path",
      "x-transition-id": "SM-15-05"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "close"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-15-06 \u2014 ROLE-011; Approved confirmation/closure policy satisfied. Record closure, no financial powers inferred",
      "x-transition-id": "SM-15-06"
    },
    {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "action": {
          "type": "string",
          "const": "reopen"
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "evidence_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uuid"
          },
          "minItems": 1,
          "maxItems": 100,
          "uniqueItems": true
        }
      },
      "required": [
        "action",
        "reason"
      ],
      "description": "SM-15-07 \u2014 ROLE-011; New evidence or permitted customer request. Reopen with owner, preserve prior resolution",
      "x-transition-id": "SM-15-07"
    }
  ]
}
```

## ResultRecord

Outcome is not seller acceptance, a signed contract, verified settlement or title transfer. Reserve and disqualification handling require approved policy.

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `auction_id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"type":"string","enum":["no_bid","pending_seller_decision","cancelled","no_qualifying_bid","pending_review"]}` |
| `winning_bid_id` | Required | `{"type":["string","null"],"format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |

Additional schema rules:

```json
{
  "additionalProperties": false,
  "allOf": [
    {
      "if": {
        "properties": {
          "status": {
            "const": "pending_seller_decision"
          }
        },
        "required": [
          "status"
        ]
      },
      "then": {
        "properties": {
          "winning_bid_id": {
            "type": "string",
            "format": "uuid"
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "status": {
            "enum": [
              "no_bid",
              "no_qualifying_bid",
              "cancelled"
            ]
          }
        },
        "required": [
          "status"
        ]
      },
      "then": {
        "properties": {
          "winning_bid_id": {
            "type": "null"
          }
        }
      }
    }
  ]
}
```

## ReconciliationRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `obligation_id` | Required | `{"type":"string","format":"uuid"}` |
| `prepared_by` | Required | `{"type":"string","format":"uuid","readOnly":true}` |
| `status` | Required | `{"type":"string","enum":["draft","pending_review","discrepancy","reconciled"]}` |
| `evidence_ids` | Required | `{"type":"array","items":{"type":"string","format":"uuid"},"minItems":1,"maxItems":100,"uniqueItems":true}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PolicyRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"type":"string","enum":["draft","pending_approval","approved","retired"]}` |
| `type` | Required | `{"type":"string","minLength":1,"maxLength":200}` |
| `policy_version_id` | Required | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## TransactionRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"type":"string","enum":["open","on_hold","closed","cancelled"]}` |
| `contract_id` | Optional | `{"type":"string","format":"uuid"}` |
| `obligation_ids` | Optional | `{"type":"array","items":{"type":"string","format":"uuid"},"minItems":1,"maxItems":100,"uniqueItems":true}` |
| `transfer_id` | Optional | `{"type":"string","format":"uuid"}` |
| `delivery_id` | Optional | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## OwnershipTransferRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `transaction_id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"type":"string","enum":["pending","evidence_pending","verified","disputed"]}` |
| `jurisdiction` | Required | `{"type":"string","minLength":1,"maxLength":200}` |
| `evidence_ids` | Optional | `{"type":"array","items":{"type":"string","format":"uuid"},"minItems":1,"maxItems":100,"uniqueItems":true}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ClosureRequest

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `evidence_ids` | Required | `{"type":"array","items":{"type":"string","format":"uuid"},"minItems":1,"maxItems":100,"uniqueItems":true}` |
| `policy_version_id` | Required | `{"type":"string","format":"uuid"}` |
| `reason` | Required | `{"type":"string","minLength":1,"maxLength":2000}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## TransferVerification

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `evidence_ids` | Required | `{"type":"array","items":{"type":"string","format":"uuid"},"minItems":1,"maxItems":100,"uniqueItems":true}` |
| `reason` | Required | `{"type":"string","minLength":1,"maxLength":2000}` |
| `authority_reference` | Required | `{"type":"string","minLength":1,"maxLength":200}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## AuthChallenge

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `challenge_id` | Required | `{"type":"string","format":"uuid"}` |
| `expires_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `methods` | Required | `{"type":"array","items":{"type":"string","enum":["webauthn","totp"]},"minItems":1,"maxItems":100}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## AuthSession

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `user_id` | Required | `{"type":"string","format":"uuid"}` |
| `expires_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `mfa_required` | Required | `{"type":"boolean","const":false}` |
| `csrf_token` | Required | `{"type":"string","minLength":32,"maxLength":512}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## MfaCompletion

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `challenge_id` | Required | `{"type":"string","format":"uuid"}` |
| `method` | Required | `{"type":"string","enum":["webauthn","totp"]}` |
| `response` | Required | `{"type":"string","minLength":1,"maxLength":16384}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## StepUpRequest

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `purpose` | Required | `{"type":"string","enum":["finance_approval","policy_approval","access_change","dealer_suspension"]}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## RecoveryRequest

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `identifier` | Required | `{"type":"string","minLength":1,"maxLength":254}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## QueuedResult

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `status` | Required | `{"type":"string","const":"accepted"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ProviderEvent

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `provider_id` | Required | `{"type":"string","format":"uuid"}` |
| `provider_event_id` | Required | `{"type":"string","minLength":1,"maxLength":200}` |
| `kind` | Required | `{"type":"string","enum":["payment_observed","payment_reversed","signature_verified","financing_approved","financing_rejected","financing_funded"]}` |
| `occurred_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `resource_id` | Required | `{"type":"string","format":"uuid"}` |
| `evidence_id` | Required | `{"type":"string","format":"uuid"}` |
| `source_payload_hash` | Required | `{"type":"string","pattern":"^[a-f0-9]{64}$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## Elevation

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `elevation_id` | Required | `{"type":"string","format":"uuid"}` |
| `purpose` | Required | `{"type":"string","enum":["finance_approval","policy_approval","access_change","dealer_suspension"]}` |
| `expires_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## TaxonomyItem

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `name` | Required | `{"type":"string","maxLength":200}` |
| `parent_id` | Required | `{"type":["string","null"],"format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## TaxonomyPage

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/TaxonomyItem"}}` |
| `next_cursor` | Required | `{"type":["string","null"]}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## Slot

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `starts_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `ends_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `timezone` | Required | `{"type":"string","maxLength":64}` |
| `available` | Required | `{"type":"boolean"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## SlotList

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/Slot"}}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## UploadRequest

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `case_id` | Required | `{"type":"string","format":"uuid"}` |
| `kind` | Required | `{"type":"string","enum":["identity","inspection","contract","payment","delivery","claim"]}` |
| `mime_type` | Required | `{"type":"string","enum":["image/jpeg","image/png","application/pdf"]}` |
| `size_bytes` | Required | `{"type":"integer","minimum":1,"maximum":20971520}` |
| `checksum_sha256` | Required | `{"type":"string","pattern":"^[a-f0-9]{64}$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## UploadGrant

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `file_id` | Required | `{"type":"string","format":"uuid"}` |
| `upload_url` | Required | `{"type":"string","format":"uri"}` |
| `expires_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `max_bytes` | Required | `{"type":"integer","minimum":1,"maximum":20971520}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## FileRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `case_id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"type":"string","enum":["quarantined","scanning","clean","rejected"]}` |
| `checksum_sha256` | Required | `{"type":"string","pattern":"^[a-f0-9]{64}$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## DownloadGrant

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `url` | Required | `{"type":"string","format":"uri"}` |
| `expires_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## InspectionCreate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `vehicle_id` | Required | `{"type":"string","format":"uuid"}` |
| `branch_id` | Required | `{"type":"string","format":"uuid"}` |
| `inspector_id` | Required | `{"type":"string","format":"uuid"}` |
| `template_version_id` | Required | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## VehicleListingCreate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `vehicle_id` | Required | `{"type":"string","format":"uuid"}` |
| `title` | Required | `{"type":"string","minLength":1,"maxLength":200}` |
| `price_minor` | Required | `{"type":"integer","minimum":0,"maximum":9007199254740991}` |
| `currency` | Required | `{"type":"string","pattern":"^[A-Z]{3}$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## DealerVerificationCreate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `organization_id` | Required | `{"type":"string","format":"uuid"}` |
| `evidence_ids` | Required | `{"type":"array","items":{"type":"string","format":"uuid"},"minItems":1,"maxItems":100,"uniqueItems":true}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## FinancingApplicationCreate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `party_id` | Required | `{"type":"string","format":"uuid"}` |
| `provider_id` | Required | `{"type":"string","format":"uuid"}` |
| `consent_id` | Required | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ContractCreate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `transaction_id` | Required | `{"type":"string","format":"uuid"}` |
| `template_version_id` | Required | `{"type":"string","format":"uuid"}` |
| `required_signer_ids` | Required | `{"type":"array","items":{"type":"string","format":"uuid"},"minItems":1,"maxItems":100,"uniqueItems":true}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PaymentObligationCreate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `transaction_id` | Required | `{"type":"string","format":"uuid"}` |
| `payer_party_id` | Required | `{"type":"string","format":"uuid"}` |
| `payee_party_id` | Required | `{"type":"string","format":"uuid"}` |
| `amount_minor` | Required | `{"type":"integer","minimum":0,"maximum":9007199254740991}` |
| `currency` | Required | `{"type":"string","pattern":"^[A-Z]{3}$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## DeliveryCreate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `transaction_id` | Required | `{"type":"string","format":"uuid"}` |
| `pickup_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## WarrantyClaimCreate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `transaction_id` | Required | `{"type":"string","format":"uuid"}` |
| `policy_version_id` | Required | `{"type":"string","format":"uuid"}` |
| `claimant_id` | Required | `{"type":"string","format":"uuid"}` |
| `evidence_ids` | Required | `{"type":"array","items":{"type":"string","format":"uuid"},"minItems":1,"maxItems":100,"uniqueItems":true}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ReconciliationCreate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `obligation_id` | Required | `{"type":"string","format":"uuid"}` |
| `evidence_ids` | Required | `{"type":"array","items":{"type":"string","format":"uuid"},"minItems":1,"maxItems":100,"uniqueItems":true}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PreferenceUpdate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `purpose` | Required | `{"enum":["marketing_email","marketing_sms","optional_analytics"]}` |
| `enabled` | Required | `{"type":"boolean"}` |
| `notice_version` | Required | `{"type":"string","minLength":1,"maxLength":200}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PreferenceRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `purpose` | Required | `{"enum":["marketing_email","marketing_sms","optional_analytics"]}` |
| `enabled` | Required | `{"type":"boolean"}` |
| `recorded_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PreferenceList

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/PreferenceRecord"}}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## SavedVehicleRequest

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `listing_id` | Required | `{"type":"string","format":"uuid"}` |
| `saved` | Required | `{"type":"boolean"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## SavedVehicleList

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":100,"items":{"$ref":"#/components/schemas/Listing"}}` |
| `next_cursor` | Required | `{"type":["string","null"]}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ProcurementCreate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `make_ids` | Required | `{"type":"array","maxItems":10,"items":{"type":"string","format":"uuid"}}` |
| `model_ids` | Required | `{"type":"array","maxItems":20,"items":{"type":"string","format":"uuid"}}` |
| `budget_minor` | Required | `{"type":"integer","minimum":1,"maximum":9007199254740991}` |
| `currency` | Required | `{"type":"string","pattern":"^[A-Z]{3}$"}` |
| `region` | Required | `{"type":"string","minLength":1,"maxLength":200}` |
| `payment_preference` | Required | `{"enum":["cash","third_party_finance","undecided"]}` |
| `notice_version` | Required | `{"type":"string","minLength":1,"maxLength":200}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ProcurementRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"enum":["submitted","assigned","matching","proposal_presented","selected","fulfilled","cancelled"]}` |
| `criteria` | Required | `{"$ref":"#/components/schemas/ProcurementCreate"}` |
| `advisor_id` | Optional | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ProcurementAction

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `action` | Required | `{"enum":["assign","present_proposal","select","fulfil","cancel"]}` |
| `reason` | Required | `{"type":"string","minLength":1,"maxLength":200}` |
| `candidate_listing_id` | Optional | `{"type":"string","format":"uuid"}` |
| `advisor_id` | Optional | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PrivacyRequest

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `kind` | Required | `{"enum":["access","correction","erasure"]}` |
| `subject_fields` | Required | `{"type":"array","minItems":1,"maxItems":20,"items":{"enum":["name","phone","email","consent","case_records","all_personal_data"]}}` |
| `reason` | Optional | `{"type":"string","maxLength":2000}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PrivacyRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"enum":["received","identity_review","scoping","processor_pending","fulfilled","partially_fulfilled","denied"]}` |
| `kind` | Required | `{"enum":["access","correction","erasure"]}` |
| `received_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `next_update_at` | Optional | `{"type":"string","format":"date-time","pattern":"Z$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ExportRequest

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `report` | Required | `{"enum":["branch_capacity","auction_audit","financial_statement","approved_metrics"]}` |
| `from` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `to` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `purpose` | Required | `{"type":"string","minLength":1,"maxLength":200}` |
| `scope_id` | Required | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ExportJob

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"enum":["pending_approval","queued","running","ready","failed","expired"]}` |
| `expires_at` | Optional | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `row_count` | Optional | `{"type":"integer","minimum":0}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ContentBlock

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `kind` | Required | `{"enum":["paragraph","heading","image","list"]}` |
| `text` | Optional | `{"type":"string","maxLength":10000}` |
| `media_id` | Optional | `{"type":"string","format":"uuid"}` |
| `alt` | Optional | `{"type":"string","maxLength":500}` |

Additional schema rules:

```json
{
  "additionalProperties": false,
  "allOf": [
    {
      "if": {
        "properties": {
          "kind": {
            "const": "image"
          }
        }
      },
      "then": {
        "required": [
          "media_id",
          "alt"
        ]
      },
      "else": {
        "required": [
          "text"
        ]
      }
    }
  ]
}
```

## ContentDraft

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `slug` | Required | `{"type":"string","pattern":"^[a-z0-9]+(-[a-z0-9]+)*$","maxLength":120}` |
| `title` | Required | `{"type":"string","minLength":1,"maxLength":200}` |
| `blocks` | Required | `{"type":"array","minItems":1,"maxItems":200,"items":{"$ref":"#/components/schemas/ContentBlock"}}` |
| `source_urls` | Required | `{"type":"array","maxItems":50,"items":{"type":"string","format":"uri"}}` |
| `review_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `indexable` | Required | `{"type":"boolean"}` |
| `canonical_path` | Required | `{"type":"string","pattern":"^/","maxLength":500}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ContentRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `revision_id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"enum":["draft","review","approved","scheduled","published","retired"]}` |
| `content` | Required | `{"$ref":"#/components/schemas/ContentDraft"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ContentAction

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `action` | Required | `{"enum":["submit_review","approve","schedule","publish","retire"]}` |
| `revision_id` | Required | `{"type":"string","format":"uuid"}` |
| `reason` | Required | `{"type":"string","minLength":1,"maxLength":200}` |
| `publish_at` | Optional | `{"type":"string","format":"date-time","pattern":"Z$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## CampaignDraft

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `name` | Required | `{"type":"string","minLength":1,"maxLength":200}` |
| `purpose` | Required | `{"const":"marketing"}` |
| `channel` | Required | `{"enum":["email","sms"]}` |
| `template_version_id` | Required | `{"type":"string","format":"uuid"}` |
| `audience_rule` | Required | `{"enum":["consented_inactive_leads","consented_repeat_buyers","consented_dealer_members"]}` |
| `starts_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `ends_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## CampaignRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"enum":["draft","review","approved","scheduled","running","stopped","completed"]}` |
| `definition` | Required | `{"$ref":"#/components/schemas/CampaignDraft"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## CampaignAction

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `action` | Required | `{"enum":["submit_review","approve","schedule","stop"]}` |
| `reason` | Required | `{"type":"string","minLength":1,"maxLength":200}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PolicyApproval

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `policy_version_id` | Required | `{"type":"string","format":"uuid"}` |
| `decision` | Required | `{"enum":["approve","reject"]}` |
| `reason` | Required | `{"type":"string","minLength":1,"maxLength":200}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## AuctionPolicy

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `starting_minor` | Required | `{"type":"integer","minimum":1,"maximum":9007199254740991}` |
| `increment_minor` | Required | `{"type":"integer","minimum":1,"maximum":9007199254740991}` |
| `reserve_minor` | Required | `{"type":["integer","null"],"minimum":1,"maximum":9007199254740991}` |
| `currency` | Required | `{"type":"string","pattern":"^[A-Z]{3}$"}` |
| `reserve_disclosure` | Required | `{"enum":["visible","hidden"]}` |
| `tie_rule` | Required | `{"const":"first_accepted_sequence"}` |
| `extensions_enabled` | Required | `{"const":false}` |
| `proxy_bidding_enabled` | Required | `{"const":false}` |
| `deposits_enabled` | Required | `{"const":false}` |
| `seller_response_seconds` | Required | `{"type":"integer","minimum":60,"maximum":2592000}` |
| `approved_terms_id` | Required | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## FinancePolicy

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `mode` | Required | `{"const":"external_evidence_only"}` |
| `currency` | Required | `{"type":"string","pattern":"^[A-Z]{3}$"}` |
| `reconciliation_tolerance_minor` | Required | `{"const":0}` |
| `maker_checker` | Required | `{"const":true}` |
| `approved_terms_id` | Required | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## RetentionPolicy

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `jurisdiction` | Required | `{"type":"string","minLength":1,"maxLength":200}` |
| `data_class` | Required | `{"enum":["identity","contact","contract","financial","inspection","audit","analytics"]}` |
| `retention_days` | Required | `{"type":"integer","minimum":1,"maximum":36500}` |
| `authority_reference` | Required | `{"type":"string","minLength":1,"maxLength":200}` |
| `honor_legal_hold` | Required | `{"const":true,"description":"A hold takes precedence and prevents disposal; this field cannot disable or bypass a hold."}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## DealerApplication

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `legal_name` | Required | `{"type":"string","minLength":1,"maxLength":200}` |
| `jurisdiction` | Required | `{"type":"string","minLength":2,"maxLength":64}` |
| `registration_number` | Required | `{"type":"string","minLength":1,"maxLength":100}` |
| `notice_version` | Required | `{"type":"string","maxLength":200}` |
| `evidence_ids` | Required | `{"type":"array","minItems":1,"maxItems":20,"items":{"type":"string","format":"uuid"},"uniqueItems":true}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## DealerApplicationResult

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `organization_id` | Required | `{"type":"string","format":"uuid"}` |
| `verification_id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"const":"submitted"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## IntakeChallengeRequest

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `resource_type` | Required | `{"enum":["seller_lead","purchase_request"]}` |
| `resource_id` | Required | `{"type":"string","format":"uuid"}` |
| `contact` | Required | `{"$ref":"#/components/schemas/ContactInput"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## IntakeClaimRequest

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `challenge_id` | Required | `{"type":"string","format":"uuid"}` |
| `code` | Required | `{"type":"string","pattern":"^[0-9]{6}$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## IntakeClaimResult

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `resource_type` | Required | `{"enum":["seller_lead","purchase_request"]}` |
| `resource_id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"const":"claimed"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## RecoveryComplete

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `recovery_token` | Required | `{"type":"string","minLength":1,"maxLength":1024}` |
| `new_password` | Required | `{"type":"string","minLength":12,"maxLength":128}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## Acknowledged

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `status` | Required | `{"const":"accepted"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ClaimChallengeResult

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `challenge_id` | Required | `{"type":"string","format":"uuid"}` |
| `status` | Required | `{"const":"accepted"}` |
| `expires_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ConsumerOfferCreate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `purchase_request_id` | Required | `{"type":"string","format":"uuid"}` |
| `listing_id` | Required | `{"type":"string","format":"uuid"}` |
| `listing_version` | Required | `{"type":"integer","minimum":1}` |
| `buyer_id` | Required | `{"type":"string","format":"uuid"}` |
| `amount_minor` | Required | `{"type":"integer","minimum":1,"maximum":9007199254740991}` |
| `currency` | Required | `{"type":"string","pattern":"^[A-Z]{3}$"}` |
| `terms_version` | Required | `{"type":"string","minLength":1,"maxLength":100}` |
| `seller_authorization_evidence_id` | Required | `{"type":"string","format":"uuid"}` |
| `expires_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ConsumerOfferRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"enum":["issued","accepted","expired","withdrawn"]}` |
| `listing_id` | Required | `{"type":"string","format":"uuid"}` |
| `buyer_id` | Required | `{"type":"string","format":"uuid"}` |
| `amount_minor` | Required | `{"type":"integer","minimum":1,"maximum":9007199254740991}` |
| `currency` | Required | `{"type":"string","pattern":"^[A-Z]{3}$"}` |
| `terms_version` | Required | `{"type":"string","minLength":1,"maxLength":100}` |
| `expires_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `transaction_id` | Optional | `{"type":"string","format":"uuid"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ConsumerOfferAcceptance

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `terms_version` | Required | `{"type":"string","minLength":1,"maxLength":100}` |
| `consent` | Required | `{"$ref":"#/components/schemas/ConsentEvidence"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ConsumerOfferWithdrawal

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `reason` | Required | `{"type":"string","minLength":1,"maxLength":1000}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PublishedMedia

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `url` | Required | `{"type":"string","format":"uri"}` |
| `alt` | Required | `{"type":"string","minLength":1,"maxLength":500}` |
| `width` | Required | `{"type":"integer","minimum":1,"maximum":12000}` |
| `height` | Required | `{"type":"integer","minimum":1,"maximum":12000}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PublicVehicle

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `make_id` | Required | `{"type":"string","format":"uuid"}` |
| `model_id` | Required | `{"type":"string","format":"uuid"}` |
| `make_name` | Required | `{"type":"string","minLength":1,"maxLength":100}` |
| `model_name` | Required | `{"type":"string","minLength":1,"maxLength":100}` |
| `year` | Required | `{"type":"integer","minimum":1886,"maximum":2100}` |
| `mileage` | Required | `{"type":"integer","minimum":0,"maximum":10000000}` |
| `mileage_unit` | Required | `{"enum":["km","mi"]}` |
| `body_type` | Required | `{"type":"string","minLength":1,"maxLength":64}` |
| `transmission` | Required | `{"enum":["manual","automatic","other","unknown"]}` |
| `fuel_type` | Required | `{"enum":["petrol","diesel","electric","hybrid","other","unknown"]}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PublicArticle

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `slug` | Required | `{"type":"string","minLength":1,"maxLength":120}` |
| `title` | Required | `{"type":"string","minLength":1,"maxLength":200}` |
| `blocks` | Required | `{"type":"array","minItems":1,"maxItems":200,"items":{"$ref":"#/components/schemas/ContentBlock"}}` |
| `published_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `reviewed_at` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `canonical_path` | Required | `{"type":"string","minLength":1,"maxLength":500}` |
| `author_display_name` | Required | `{"type":"string","minLength":1,"maxLength":150}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PublicValuationInput

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `vehicle` | Required | `{"$ref":"#/components/schemas/VehicleInput"}` |
| `market_code` | Required | `{"type":"string","minLength":1,"maxLength":64}` |
| `currency` | Required | `{"type":"string","pattern":"^[A-Z]{3}$"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## PublicValuation

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `status` | Required | `{"enum":["estimate","insufficient_data","unavailable"]}` |
| `low_minor` | Optional | `{"type":"integer","minimum":1,"maximum":9007199254740991}` |
| `high_minor` | Optional | `{"type":"integer","minimum":1,"maximum":9007199254740991}` |
| `currency` | Optional | `{"type":"string","pattern":"^[A-Z]{3}$"}` |
| `policy_version` | Required | `{"type":"string","minLength":1,"maxLength":100}` |
| `as_of` | Required | `{"type":"string","format":"date-time","pattern":"Z$"}` |
| `disclaimer` | Required | `{"type":"string","minLength":1,"maxLength":1000}` |

Additional schema rules:

```json
{
  "additionalProperties": false,
  "allOf": [
    {
      "if": {
        "properties": {
          "status": {
            "const": "estimate"
          }
        },
        "required": [
          "status"
        ]
      },
      "then": {
        "required": [
          "low_minor",
          "high_minor",
          "currency"
        ]
      },
      "else": {
        "not": {
          "anyOf": [
            {
              "required": [
                "low_minor"
              ]
            },
            {
              "required": [
                "high_minor"
              ]
            }
          ]
        }
      }
    }
  ]
}
```

## InspectionPoint

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `code` | Required | `{"type":"string","minLength":1,"maxLength":80}` |
| `section` | Required | `{"type":"string","minLength":1,"maxLength":100}` |
| `label` | Required | `{"type":"string","minLength":1,"maxLength":200}` |
| `required` | Required | `{"type":"boolean"}` |
| `allowed_results` | Required | `{"type":"array","minItems":1,"maxItems":4,"uniqueItems":true,"items":{"enum":["pass","defect","not_applicable","unknown"]}}` |
| `evidence_required_on_defect` | Required | `{"type":"boolean"}` |
| `guidance` | Required | `{"type":"string","minLength":1,"maxLength":2000}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## InspectionTemplateRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `status` | Required | `{"enum":["draft","approved","retired"]}` |
| `jurisdiction` | Required | `{"type":"string","minLength":1,"maxLength":64}` |
| `points` | Required | `{"type":"array","minItems":1,"maxItems":500,"items":{"$ref":"#/components/schemas/InspectionPoint"}}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## ListingFilters

Service checks min <= max, model belongs to make, market-supported codes and comparable units; omitted filter is unconstrained, never zero.

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `make_id` | Optional | `{"type":"string","format":"uuid"}` |
| `model_id` | Optional | `{"type":"string","format":"uuid"}` |
| `year_min` | Optional | `{"type":"integer","minimum":1886,"maximum":2100}` |
| `year_max` | Optional | `{"type":"integer","minimum":1886,"maximum":2100}` |
| `mileage_max` | Optional | `{"type":"integer","minimum":0,"maximum":10000000}` |
| `mileage_unit` | Optional | `{"enum":["km","mi"]}` |
| `price_min_minor` | Optional | `{"type":"integer","minimum":1,"maximum":9007199254740991}` |
| `price_max_minor` | Optional | `{"type":"integer","minimum":1,"maximum":9007199254740991}` |
| `currency` | Optional | `{"type":"string","pattern":"^[A-Z]{3}$"}` |
| `region_id` | Optional | `{"type":"string","format":"uuid"}` |
| `transmission` | Optional | `{"enum":["manual","automatic","other","unknown"]}` |
| `body_type` | Optional | `{"type":"string","minLength":1,"maxLength":64}` |

Additional schema rules:

```json
{
  "additionalProperties": false,
  "dependentRequired": {
    "price_min_minor": [
      "currency"
    ],
    "price_max_minor": [
      "currency"
    ],
    "mileage_max": [
      "mileage_unit"
    ]
  }
}
```

## SavedSearchCreate

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `name` | Required | `{"type":"string","minLength":1,"maxLength":100}` |
| `filters` | Required | `{"$ref":"#/components/schemas/ListingFilters"}` |
| `notification_frequency` | Required | `{"enum":["none","daily","weekly"]}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## SavedSearchRecord

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `id` | Required | `{"type":"string","format":"uuid"}` |
| `version` | Required | `{"type":"integer","minimum":1}` |
| `search` | Required | `{"$ref":"#/components/schemas/SavedSearchCreate"}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

## SavedSearchList

| Field | Presence | Type, reference and constraints |
|---|---|---|
| `items` | Required | `{"type":"array","maxItems":50,"items":{"$ref":"#/components/schemas/SavedSearchRecord"}}` |

Additional schema rules:

```json
{
  "additionalProperties": false
}
```

