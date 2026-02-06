"""
Hand Module - Operations & Drafting
=====================================
Drafts code, purchase orders, and legal notices.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from string import Template


class DocumentType(Enum):
    """Types of documents the Hand can draft."""
    PURCHASE_ORDER = "purchase_order"
    LEGAL_NOTICE = "legal_notice"
    CUSTOMER_NOTIFICATION = "customer_notification"
    INTERNAL_MEMO = "internal_memo"
    INCIDENT_REPORT = "incident_report"
    CODE_PATCH = "code_patch"
    PRESS_RELEASE = "press_release"
    REGULATORY_FILING = "regulatory_filing"


@dataclass
class DraftedDocument:
    """A document drafted by the Hand."""
    id: str
    document_type: DocumentType
    title: str
    content: str
    metadata: Dict[str, Any]
    created_at: str
    requires_approval: bool
    approvers: List[str]
    status: str = "draft"


class Hand:
    """
    The Hand module: Operations.
    Drafts code, purchase orders, and legal notices.
    """

    def __init__(self):
        """Initialize the Hand."""
        self.templates = self._load_templates()
        self.drafts: List[DraftedDocument] = []
    
    def _load_templates(self) -> Dict[DocumentType, str]:
        """Load document templates."""
        return {
            DocumentType.PURCHASE_ORDER: """
PURCHASE ORDER
==============

PO Number: ${po_number}
Date: ${date}
Vendor: ${vendor_name}

SHIP TO:
${ship_to_address}

BILL TO:
${bill_to_address}

LINE ITEMS:
-----------
${line_items}

SUBTOTAL: ${subtotal}
TAX: ${tax}
SHIPPING: ${shipping}
-----------
TOTAL: ${total}

TERMS: ${terms}
DELIVERY DATE: ${delivery_date}

SPECIAL INSTRUCTIONS:
${special_instructions}

---
Authorized by: ____________________
Date: ____________________
""",
            DocumentType.LEGAL_NOTICE: """
LEGAL NOTICE
============

Date: ${date}
Reference: ${reference_number}

TO: ${recipient_name}
    ${recipient_address}

FROM: ${sender_name}
      ${sender_title}
      ${company_name}

RE: ${subject}

Dear ${recipient_name},

${opening_paragraph}

${body_paragraphs}

${legal_clauses}

${closing_paragraph}

This notice is being provided pursuant to ${legal_basis}.

Sincerely,

${sender_name}
${sender_title}
${company_name}

CC: ${cc_list}
""",
            DocumentType.CUSTOMER_NOTIFICATION: """
CUSTOMER NOTIFICATION
=====================

Date: ${date}
Subject: ${subject}

Dear Valued Customer,

${opening}

What Happened:
${incident_description}

What We're Doing:
${remediation_steps}

What You Can Do:
${customer_actions}

Timeline:
${timeline}

We apologize for any inconvenience this may cause. If you have questions, please contact:
${contact_info}

Sincerely,
${sender_name}
${sender_title}
${company_name}
""",
            DocumentType.INTERNAL_MEMO: """
INTERNAL MEMORANDUM
===================

TO: ${recipients}
FROM: ${sender}
DATE: ${date}
RE: ${subject}

CLASSIFICATION: ${classification}

---

${summary}

BACKGROUND:
${background}

KEY POINTS:
${key_points}

RECOMMENDED ACTIONS:
${actions}

TIMELINE:
${timeline}

Please direct questions to ${contact}.

---
This memo is for internal use only.
""",
            DocumentType.INCIDENT_REPORT: """
INCIDENT REPORT
===============

Report ID: ${report_id}
Date/Time of Incident: ${incident_datetime}
Date/Time of Report: ${report_datetime}
Reported By: ${reporter}

INCIDENT TYPE: ${incident_type}
SEVERITY: ${severity}
STATUS: ${status}

---

INCIDENT SUMMARY:
${summary}

AFFECTED SYSTEMS/ASSETS:
${affected_assets}

TIMELINE OF EVENTS:
${timeline}

ROOT CAUSE ANALYSIS:
${root_cause}

IMMEDIATE ACTIONS TAKEN:
${immediate_actions}

LONG-TERM REMEDIATION:
${remediation}

LESSONS LEARNED:
${lessons_learned}

---
Approved by: ____________________
Date: ____________________
""",
            DocumentType.CODE_PATCH: """
# EMERGENCY CODE PATCH
# ====================
# Patch ID: ${patch_id}
# Date: ${date}
# Author: ${author}
# Issue: ${issue_description}
# Severity: ${severity}

# BEFORE (Original Code):
# ${original_code}

# AFTER (Patched Code):
${patched_code}

# TESTING NOTES:
# ${testing_notes}

# ROLLBACK PROCEDURE:
# ${rollback_procedure}
""",
            DocumentType.PRESS_RELEASE: """
FOR IMMEDIATE RELEASE

${headline}

${subheadline}

${city}, ${date} — ${opening_paragraph}

${body_paragraphs}

"${quote}" said ${quote_attribution}.

${about_section}

MEDIA CONTACT:
${media_contact_name}
${media_contact_email}
${media_contact_phone}

###
""",
            DocumentType.REGULATORY_FILING: """
REGULATORY FILING
=================

Filing Date: ${date}
Regulatory Body: ${regulatory_body}
Filing Type: ${filing_type}
Reference Number: ${reference_number}

FILER INFORMATION:
Company: ${company_name}
Address: ${company_address}
Contact: ${contact_name}
Phone: ${contact_phone}
Email: ${contact_email}

FILING SUMMARY:
${summary}

DETAILED DISCLOSURE:
${disclosure}

SUPPORTING DOCUMENTATION:
${supporting_docs}

CERTIFICATION:
I certify that the information provided in this filing is true and accurate to the best of my knowledge.

Signature: ____________________
Name: ${certifier_name}
Title: ${certifier_title}
Date: ____________________
""",
        }
    
    def draft(self, document_type: DocumentType, context: Dict[str, Any]) -> DraftedDocument:
        """
        Draft a document based on type and context.
        
        Args:
            document_type: Type of document to draft.
            context: Dictionary of values to fill in the template.
        
        Returns:
            DraftedDocument with the generated content.
        """
        print(f"✋ Hand drafting: {document_type.value}...")
        
        # Get template
        template_str = self.templates.get(document_type, "No template available for ${document_type}")
        template = Template(template_str)
        
        # Add standard fields if not provided
        if "date" not in context:
            context["date"] = datetime.now().strftime("%Y-%m-%d")
        
        # Generate document ID
        doc_id = f"{document_type.value.upper()[:3]}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Fill template with safe substitution (won't fail on missing keys)
        content = template.safe_substitute(context)
        
        # Determine approvers based on document type
        approvers_map = {
            DocumentType.PURCHASE_ORDER: ["procurement@company.com", "finance@company.com"],
            DocumentType.LEGAL_NOTICE: ["legal@company.com", "ceo@company.com"],
            DocumentType.CUSTOMER_NOTIFICATION: ["pr@company.com", "legal@company.com"],
            DocumentType.INTERNAL_MEMO: ["manager@company.com"],
            DocumentType.INCIDENT_REPORT: ["security@company.com", "cto@company.com"],
            DocumentType.CODE_PATCH: ["tech-lead@company.com", "security@company.com"],
            DocumentType.PRESS_RELEASE: ["pr@company.com", "legal@company.com", "ceo@company.com"],
            DocumentType.REGULATORY_FILING: ["legal@company.com", "cfo@company.com"],
        }
        
        requires_approval = document_type in [
            DocumentType.LEGAL_NOTICE,
            DocumentType.PRESS_RELEASE,
            DocumentType.REGULATORY_FILING,
            DocumentType.CUSTOMER_NOTIFICATION,
        ]
        
        draft = DraftedDocument(
            id=doc_id,
            document_type=document_type,
            title=context.get("subject", context.get("title", document_type.value)),
            content=content,
            metadata=context,
            created_at=datetime.now().isoformat(),
            requires_approval=requires_approval,
            approvers=approvers_map.get(document_type, []),
        )
        
        self.drafts.append(draft)
        
        print(f"✅ Hand drafted: {doc_id}")
        return draft
    
    def draft_purchase_order(self, vendor: str, items: List[Dict[str, Any]], 
                              urgency: str = "standard") -> DraftedDocument:
        """Convenience method to draft a purchase order."""
        # Format line items
        line_items_str = ""
        subtotal = 0
        for i, item in enumerate(items, 1):
            qty = item.get("quantity", 1)
            unit_price = item.get("unit_price", 0)
            total = qty * unit_price
            subtotal += total
            line_items_str += f"{i}. {item.get('description', 'Item')} - Qty: {qty} @ ${unit_price:,.2f} = ${total:,.2f}\n"
        
        tax = subtotal * 0.08  # 8% tax
        shipping = 0 if subtotal > 1000 else 50
        total = subtotal + tax + shipping
        
        delivery_days = 3 if urgency == "urgent" else 14
        delivery_date = (datetime.now() + timedelta(days=delivery_days)).strftime("%Y-%m-%d")
        
        context = {
            "po_number": f"PO-{datetime.now().strftime('%Y%m%d')}-{len(self.drafts)+1:04d}",
            "vendor_name": vendor,
            "ship_to_address": "Operations Center\n123 Business Ave\nCity, State 12345",
            "bill_to_address": "Accounts Payable\n123 Business Ave\nCity, State 12345",
            "line_items": line_items_str,
            "subtotal": f"${subtotal:,.2f}",
            "tax": f"${tax:,.2f}",
            "shipping": f"${shipping:,.2f}",
            "total": f"${total:,.2f}",
            "terms": "Net 30" if urgency != "urgent" else "Due on Receipt",
            "delivery_date": delivery_date,
            "special_instructions": "EXPEDITE" if urgency == "urgent" else "Standard delivery",
        }
        
        return self.draft(DocumentType.PURCHASE_ORDER, context)
    
    def draft_incident_report(self, incident_summary: str, affected_assets: List[str],
                               severity: str, actions_taken: List[str]) -> DraftedDocument:
        """Convenience method to draft an incident report."""
        context = {
            "report_id": f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "incident_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "report_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reporter": "Longshot System (Automated)",
            "incident_type": "Operational Disruption",
            "severity": severity.upper(),
            "status": "Under Investigation",
            "summary": incident_summary,
            "affected_assets": "\n".join([f"  - {asset}" for asset in affected_assets]),
            "timeline": f"  - {datetime.now().strftime('%H:%M')} - Incident detected by monitoring systems",
            "root_cause": "Under investigation - preliminary analysis pending",
            "immediate_actions": "\n".join([f"  - {action}" for action in actions_taken]),
            "remediation": "To be determined following root cause analysis",
            "lessons_learned": "To be documented post-incident",
        }
        
        return self.draft(DocumentType.INCIDENT_REPORT, context)
    
    def draft_customer_notification(self, subject: str, incident_description: str,
                                     remediation_steps: List[str], timeline: str) -> DraftedDocument:
        """Convenience method to draft a customer notification."""
        context = {
            "subject": subject,
            "opening": "We are writing to inform you of an important update regarding our services.",
            "incident_description": incident_description,
            "remediation_steps": "\n".join([f"  • {step}" for step in remediation_steps]),
            "customer_actions": "  • No action is required from you at this time.\n  • We will provide updates as the situation develops.",
            "timeline": timeline,
            "contact_info": "  Support: support@company.com\n  Phone: 1-800-COMPANY",
            "sender_name": "Customer Success Team",
            "sender_title": "Customer Relations",
            "company_name": "Your Company Name",
        }
        
        return self.draft(DocumentType.CUSTOMER_NOTIFICATION, context)
    
    def draft_code_patch(self, issue_description: str, original_code: str,
                          patched_code: str, testing_notes: str) -> DraftedDocument:
        """Convenience method to draft a code patch."""
        context = {
            "patch_id": f"PATCH-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "author": "Longshot System",
            "issue_description": issue_description,
            "severity": "HIGH",
            "original_code": original_code,
            "patched_code": patched_code,
            "testing_notes": testing_notes,
            "rollback_procedure": "Revert to previous commit and redeploy",
        }
        
        return self.draft(DocumentType.CODE_PATCH, context)
    
    def get_drafts_by_type(self, document_type: DocumentType) -> List[DraftedDocument]:
        """Get all drafts of a specific type."""
        return [d for d in self.drafts if d.document_type == document_type]
    
    def get_pending_approvals(self) -> List[DraftedDocument]:
        """Get all drafts pending approval."""
        return [d for d in self.drafts if d.requires_approval and d.status == "draft"]
    
    def approve_draft(self, draft_id: str, approver: str) -> bool:
        """Mark a draft as approved."""
        for draft in self.drafts:
            if draft.id == draft_id:
                if approver in draft.approvers:
                    draft.status = "approved"
                    draft.metadata["approved_by"] = approver
                    draft.metadata["approved_at"] = datetime.now().isoformat()
                    return True
        return False


if __name__ == "__main__":
    # Test the Hand
    hand = Hand()
    
    # Test purchase order
    po = hand.draft_purchase_order(
        vendor="Emergency Suppliers Inc.",
        items=[
            {"description": "Critical Component A", "quantity": 100, "unit_price": 250.00},
            {"description": "Critical Component B", "quantity": 50, "unit_price": 500.00},
        ],
        urgency="urgent"
    )
    
    print("\n--- PURCHASE ORDER ---")
    print(po.content)
    
    # Test incident report
    report = hand.draft_incident_report(
        incident_summary="Supplier disruption affecting production line",
        affected_assets=["SUP-001", "PROD-001", "FAC-001"],
        severity="high",
        actions_taken=[
            "Activated backup supplier protocol",
            "Notified affected customers",
            "Initiated inventory assessment",
        ]
    )
    
    print("\n--- INCIDENT REPORT ---")
    print(report.content)
    
    # Summary
    print(f"\n✅ Hand created {len(hand.drafts)} documents")
    print(f"📋 Pending approvals: {len(hand.get_pending_approvals())}")
