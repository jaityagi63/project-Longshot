# Hand ✋

**Domain:** Operations  
**Description:** Drafts code, purchase orders, and legal notices.

## Overview

The Hand module generates operational documents from templates. It creates purchase orders, legal notices, incident reports, and other formal documentation.

## Features

- **Template-Based Generation**: Consistent document formatting
- **Multiple Document Types**: POs, legal notices, incident reports, code patches
- **Approval Workflow**: Tracks which documents require approval
- **Metadata Tracking**: Maintains creation context and status
- **Convenience Methods**: Simplified APIs for common document types

## Document Types

- `purchase_order` - Emergency and standard procurement
- `legal_notice` - Formal legal communications
- `customer_notification` - Customer-facing updates
- `internal_memo` - Internal communications
- `incident_report` - Incident documentation
- `code_patch` - Emergency code changes
- `press_release` - Media communications
- `regulatory_filing` - Compliance submissions

## Usage

```python
from src.hand import Hand, DocumentType

hand = Hand()

# Draft a purchase order
po = hand.draft_purchase_order(
    vendor="Emergency Supplies Inc.",
    items=[
        {"description": "Component A", "quantity": 100, "unit_price": 250.00},
        {"description": "Component B", "quantity": 50, "unit_price": 500.00},
    ],
    urgency="urgent"
)

print(po.content)

# Draft an incident report
report = hand.draft_incident_report(
    incident_summary="Supplier disruption affecting production",
    affected_assets=["SUP-001", "PROD-001"],
    severity="high",
    actions_taken=["Activated backup supplier", "Notified customers"]
)

# Check pending approvals
pending = hand.get_pending_approvals()
print(f"Documents pending approval: {len(pending)}")
```

## Output

Each `DraftedDocument` contains:
- `id`: Unique document identifier
- `document_type`: Type of document
- `title`: Document title
- `content`: Full document text
- `metadata`: Original context/parameters
- `requires_approval`: Whether approval is needed
- `approvers`: List of required approvers
- `status`: Current status (draft/approved)

## Approval Workflow

Certain documents require approval before use:
- Legal notices → Legal team, CEO
- Press releases → PR, Legal, CEO
- Regulatory filings → Legal, CFO
- Customer notifications → PR, Legal
