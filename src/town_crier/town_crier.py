"""
Town Crier Module - Communications
===================================
Drafts unified messaging for all stakeholders.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class StakeholderType(Enum):
    """Types of stakeholders."""
    EMPLOYEES = "employees"
    CUSTOMERS = "customers"
    INVESTORS = "investors"
    MEDIA = "media"
    REGULATORS = "regulators"
    PARTNERS = "partners"
    BOARD = "board"
    PUBLIC = "public"


class MessageTone(Enum):
    """Tone of the message."""
    INFORMATIONAL = "informational"
    REASSURING = "reassuring"
    URGENT = "urgent"
    APOLOGETIC = "apologetic"
    CELEBRATORY = "celebratory"
    FORMAL = "formal"


class CommunicationChannel(Enum):
    """Communication channels."""
    EMAIL = "email"
    PRESS_RELEASE = "press_release"
    INTERNAL_MEMO = "internal_memo"
    SOCIAL_MEDIA = "social_media"
    SMS = "sms"
    VIDEO_MESSAGE = "video_message"
    WEBSITE_BANNER = "website_banner"


@dataclass
class StakeholderMessage:
    """A message crafted for a specific stakeholder group."""
    stakeholder: StakeholderType
    channel: CommunicationChannel
    subject: str
    content: str
    tone: MessageTone
    key_points: List[str]
    call_to_action: Optional[str]
    embargo_until: Optional[str] = None


@dataclass
class CommunicationPlan:
    """A unified communication plan for all stakeholders."""
    plan_id: str
    situation_summary: str
    created_at: str
    messages: List[StakeholderMessage]
    communication_sequence: List[Dict[str, Any]]
    talking_points: List[str]
    qa_pairs: List[Dict[str, str]]
    spokesperson: str


class TownCrier:
    """
    The Town Crier module: Communications.
    Drafts unified messaging for all stakeholders.
    """

    def __init__(self):
        """Initialize the Town Crier."""
        self.plans: List[CommunicationPlan] = []
        self.message_templates = self._load_templates()
    
    def _load_templates(self) -> Dict[StakeholderType, Dict[str, str]]:
        """Load message templates for each stakeholder type."""
        return {
            StakeholderType.EMPLOYEES: {
                "opening": "Team,\n\nI want to update you on an important development.",
                "closing": "I appreciate your continued dedication and resilience. We will get through this together.\n\nBest,\n{spokesperson}",
                "tone_guide": "Be transparent, supportive, and action-oriented",
            },
            StakeholderType.CUSTOMERS: {
                "opening": "Dear Valued Customer,\n\nWe are reaching out to keep you informed about a matter that may affect you.",
                "closing": "Thank you for your patience and continued trust in us.\n\nSincerely,\nCustomer Experience Team",
                "tone_guide": "Be apologetic if needed, focus on their experience and resolution",
            },
            StakeholderType.INVESTORS: {
                "opening": "Dear Shareholders,\n\nThis communication is to inform you of a material development.",
                "closing": "We remain committed to protecting shareholder value and will provide updates as appropriate.\n\nRespectfully,\n{spokesperson}",
                "tone_guide": "Be factual, quantify impacts, emphasize risk management",
            },
            StakeholderType.MEDIA: {
                "opening": "FOR IMMEDIATE RELEASE\n\n{company_name} Provides Update on {situation}",
                "closing": "For media inquiries, please contact:\n{media_contact}",
                "tone_guide": "Be factual, quotable, provide context",
            },
            StakeholderType.REGULATORS: {
                "opening": "Dear [Regulatory Body],\n\nIn accordance with our disclosure obligations, we are providing notice of the following.",
                "closing": "We are available to provide additional information as needed.\n\nRespectfully submitted,\n{spokesperson}",
                "tone_guide": "Be precise, compliant, comprehensive",
            },
            StakeholderType.PARTNERS: {
                "opening": "Dear Partner,\n\nWe want to proactively inform you of a development that may impact our relationship.",
                "closing": "We value our partnership and are committed to working through this together.\n\nBest regards,\n{spokesperson}",
                "tone_guide": "Be collaborative, focus on joint impact and solutions",
            },
            StakeholderType.BOARD: {
                "opening": "Board Members,\n\nThis briefing covers a developing situation requiring board awareness.",
                "closing": "A more detailed briefing will be provided at the next scheduled meeting.\n\n{spokesperson}",
                "tone_guide": "Be concise, strategic, governance-focused",
            },
            StakeholderType.PUBLIC: {
                "opening": "Statement from {company_name}",
                "closing": "We are committed to transparency and will provide updates as the situation develops.",
                "tone_guide": "Be clear, accessible, non-technical",
            },
        }
    
    def _craft_message(self, stakeholder: StakeholderType, situation: Dict[str, Any],
                       tone: MessageTone) -> StakeholderMessage:
        """Craft a message for a specific stakeholder group."""
        template = self.message_templates.get(stakeholder, {})
        
        # Determine channel based on stakeholder
        channel_map = {
            StakeholderType.EMPLOYEES: CommunicationChannel.INTERNAL_MEMO,
            StakeholderType.CUSTOMERS: CommunicationChannel.EMAIL,
            StakeholderType.INVESTORS: CommunicationChannel.EMAIL,
            StakeholderType.MEDIA: CommunicationChannel.PRESS_RELEASE,
            StakeholderType.REGULATORS: CommunicationChannel.EMAIL,
            StakeholderType.PARTNERS: CommunicationChannel.EMAIL,
            StakeholderType.BOARD: CommunicationChannel.INTERNAL_MEMO,
            StakeholderType.PUBLIC: CommunicationChannel.WEBSITE_BANNER,
        }
        
        # Build subject line
        severity = situation.get("severity", "medium")
        subject_prefix = {
            "critical": "URGENT: ",
            "high": "Important: ",
            "medium": "",
            "low": "Update: ",
        }
        subject = f"{subject_prefix.get(severity, '')}{situation.get('summary', 'Situation Update')}"
        
        # Build key points based on stakeholder interests
        key_points = self._generate_key_points(stakeholder, situation)
        
        # Build content
        opening = template.get("opening", "Dear Stakeholder,").format(
            spokesperson=situation.get("spokesperson", "Leadership Team"),
            company_name=situation.get("company_name", "Our Company"),
            situation=situation.get("summary", "current situation"),
        )
        
        body_paragraphs = self._generate_body(stakeholder, situation, key_points)
        
        closing = template.get("closing", "Thank you for your attention.").format(
            spokesperson=situation.get("spokesperson", "Leadership Team"),
            media_contact=situation.get("media_contact", "pr@company.com"),
        )
        
        content = f"{opening}\n\n{body_paragraphs}\n\n{closing}"
        
        # Determine call to action
        cta = self._generate_cta(stakeholder, situation)
        
        return StakeholderMessage(
            stakeholder=stakeholder,
            channel=channel_map.get(stakeholder, CommunicationChannel.EMAIL),
            subject=subject,
            content=content,
            tone=tone,
            key_points=key_points,
            call_to_action=cta,
        )
    
    def _generate_key_points(self, stakeholder: StakeholderType, situation: Dict[str, Any]) -> List[str]:
        """Generate key points tailored to stakeholder interests."""
        base_points = [
            f"Situation: {situation.get('summary', 'N/A')}",
        ]
        
        if stakeholder == StakeholderType.EMPLOYEES:
            base_points.extend([
                "Your safety and job security remain our top priorities",
                "Leadership is actively managing the situation",
                "Regular updates will be provided through established channels",
            ])
        elif stakeholder == StakeholderType.CUSTOMERS:
            base_points.extend([
                "We are working to minimize any impact on your service",
                situation.get("customer_impact", "Service levels may be temporarily affected"),
                "Our team is available to address your concerns",
            ])
        elif stakeholder == StakeholderType.INVESTORS:
            financial_impact = situation.get("financial_impact", 0)
            base_points.extend([
                f"Estimated financial impact: ${financial_impact:,.0f}" if financial_impact else "Financial impact under assessment",
                "Risk mitigation measures have been activated",
                "Management is actively monitoring the situation",
            ])
        elif stakeholder == StakeholderType.MEDIA:
            base_points.extend([
                situation.get("official_statement", "We are aware of the situation and responding appropriately"),
                "Additional details will be provided as they become available",
            ])
        elif stakeholder == StakeholderType.REGULATORS:
            base_points.extend([
                "All relevant compliance measures are being followed",
                "Documentation is being preserved for review",
                "We will provide additional filings as required",
            ])
        
        return base_points
    
    def _generate_body(self, stakeholder: StakeholderType, situation: Dict[str, Any],
                       key_points: List[str]) -> str:
        """Generate the body of the message."""
        paragraphs = []
        
        # Situation overview
        paragraphs.append(f"We want to inform you about the following development: {situation.get('summary', 'An operational matter requiring attention')}.")
        
        # Key points
        if key_points:
            points_list = "\n".join([f"• {point}" for point in key_points[1:]])  # Skip first (summary)
            paragraphs.append(f"Here's what you need to know:\n\n{points_list}")
        
        # Actions being taken
        actions = situation.get("actions_taken", ["Monitoring the situation closely"])
        actions_text = "\n".join([f"• {action}" for action in actions])
        paragraphs.append(f"Actions we are taking:\n\n{actions_text}")
        
        # Timeline if available
        timeline = situation.get("timeline", "")
        if timeline:
            paragraphs.append(f"Timeline: {timeline}")
        
        return "\n\n".join(paragraphs)
    
    def _generate_cta(self, stakeholder: StakeholderType, situation: Dict[str, Any]) -> str:
        """Generate a call to action for the stakeholder."""
        cta_map = {
            StakeholderType.EMPLOYEES: "Please direct questions to your manager or HR",
            StakeholderType.CUSTOMERS: "Contact support at support@company.com for any concerns",
            StakeholderType.INVESTORS: "Join our investor call scheduled for [DATE] at [TIME]",
            StakeholderType.MEDIA: "Media inquiries: pr@company.com",
            StakeholderType.REGULATORS: "We are available for follow-up at your convenience",
            StakeholderType.PARTNERS: "Please reach out to your account manager",
            StakeholderType.BOARD: "Detailed briefing materials will follow",
            StakeholderType.PUBLIC: "Visit our website for updates",
        }
        return cta_map.get(stakeholder, "Contact us for more information")
    
    def _generate_qa_pairs(self, situation: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate anticipated Q&A pairs for spokespeople."""
        qa = [
            {
                "question": "What happened?",
                "answer": situation.get("summary", "We are addressing an operational matter."),
            },
            {
                "question": "How many people/customers are affected?",
                "answer": situation.get("affected_count", "We are still assessing the full scope."),
            },
            {
                "question": "What are you doing about it?",
                "answer": " ".join(situation.get("actions_taken", ["We have activated our response protocols."])),
            },
            {
                "question": "When will it be resolved?",
                "answer": situation.get("timeline", "We are working to resolve this as quickly as possible."),
            },
            {
                "question": "Will there be financial impact?",
                "answer": f"We estimate the impact at ${situation.get('financial_impact', 0):,.0f}. We will provide updates as our assessment continues." if situation.get("financial_impact") else "We are still assessing potential impacts.",
            },
            {
                "question": "What should customers/stakeholders do?",
                "answer": "At this time, no action is required. We will reach out if that changes.",
            },
        ]
        return qa
    
    def _generate_talking_points(self, situation: Dict[str, Any]) -> List[str]:
        """Generate talking points for spokespeople."""
        return [
            f"We became aware of {situation.get('summary', 'the situation')} on {datetime.now().strftime('%B %d, %Y')}.",
            "We immediately activated our response protocols.",
            f"Our team is working around the clock to {'resolve this' if situation.get('severity') in ['high', 'critical'] else 'address this'}.",
            "The safety and security of our stakeholders remains our top priority.",
            "We are committed to transparency and will provide updates as appropriate.",
            "We have engaged all necessary internal and external resources.",
        ]
    
    def broadcast(self, situation: Dict[str, Any], 
                  stakeholders: Optional[List[StakeholderType]] = None) -> CommunicationPlan:
        """
        Create a unified communication plan for a situation.
        
        Args:
            situation: Dictionary describing the situation.
            stakeholders: Optional list of specific stakeholders. If None, communicates to all.
        
        Returns:
            CommunicationPlan with messages for all stakeholders.
        """
        summary = situation.get("summary", "Situation update")
        print(f"📢 Town Crier preparing communications for: '{summary[:50]}...'")
        
        # Default to all stakeholders if not specified
        if stakeholders is None:
            stakeholders = list(StakeholderType)
        
        # Determine appropriate tone based on severity
        severity = situation.get("severity", "medium")
        tone_map = {
            "critical": MessageTone.URGENT,
            "high": MessageTone.REASSURING,
            "medium": MessageTone.INFORMATIONAL,
            "low": MessageTone.INFORMATIONAL,
        }
        base_tone = tone_map.get(severity, MessageTone.INFORMATIONAL)
        
        # Craft messages for each stakeholder
        messages = []
        for stakeholder in stakeholders:
            msg = self._craft_message(stakeholder, situation, base_tone)
            messages.append(msg)
        
        # Define communication sequence (order matters)
        sequence = [
            {"stakeholder": StakeholderType.EMPLOYEES.value, "timing": "T+0", "note": "Internal first"},
            {"stakeholder": StakeholderType.BOARD.value, "timing": "T+0", "note": "Governance requirement"},
            {"stakeholder": StakeholderType.REGULATORS.value, "timing": "T+1hr", "note": "If required"},
            {"stakeholder": StakeholderType.CUSTOMERS.value, "timing": "T+2hr", "note": "Affected customers first"},
            {"stakeholder": StakeholderType.PARTNERS.value, "timing": "T+2hr", "note": "Concurrent with customers"},
            {"stakeholder": StakeholderType.INVESTORS.value, "timing": "T+4hr", "note": "After operational comms"},
            {"stakeholder": StakeholderType.MEDIA.value, "timing": "T+6hr", "note": "Only if needed"},
            {"stakeholder": StakeholderType.PUBLIC.value, "timing": "T+6hr", "note": "Concurrent with media"},
        ]
        
        # Filter sequence to only included stakeholders
        included = {s.value for s in stakeholders}
        sequence = [s for s in sequence if s["stakeholder"] in included]
        
        # Generate supporting materials
        talking_points = self._generate_talking_points(situation)
        qa_pairs = self._generate_qa_pairs(situation)
        
        plan = CommunicationPlan(
            plan_id=f"COMM-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            situation_summary=summary,
            created_at=datetime.now().isoformat(),
            messages=messages,
            communication_sequence=sequence,
            talking_points=talking_points,
            qa_pairs=qa_pairs,
            spokesperson=situation.get("spokesperson", "Chief Communications Officer"),
        )
        
        self.plans.append(plan)
        
        print(f"✅ Town Crier prepared {len(messages)} stakeholder messages.")
        return plan
    
    def get_communication_report(self, plan: CommunicationPlan) -> str:
        """Generate a human-readable communication plan report."""
        lines = [
            f"📢 TOWN CRIER COMMUNICATION PLAN",
            f"{'=' * 50}",
            f"Plan ID: {plan.plan_id}",
            f"Situation: {plan.situation_summary}",
            f"Spokesperson: {plan.spokesperson}",
            f"",
            f"📅 COMMUNICATION SEQUENCE:",
        ]
        
        for item in plan.communication_sequence:
            lines.append(f"  {item['timing']} - {item['stakeholder'].upper()} ({item['note']})")
        
        lines.append(f"\n📝 STAKEHOLDER MESSAGES ({len(plan.messages)}):")
        for msg in plan.messages:
            lines.append(f"\n  [{msg.stakeholder.value.upper()}] via {msg.channel.value}")
            lines.append(f"  Subject: {msg.subject}")
            lines.append(f"  Tone: {msg.tone.value}")
            lines.append(f"  Key Points: {len(msg.key_points)}")
        
        lines.append(f"\n💬 TALKING POINTS:")
        for point in plan.talking_points[:4]:
            lines.append(f"  • {point}")
        
        lines.append(f"\n❓ Q&A PREPARED: {len(plan.qa_pairs)} questions")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test the Town Crier
    crier = TownCrier()
    
    situation = {
        "summary": "Temporary service disruption affecting Western region customers",
        "severity": "high",
        "actions_taken": [
            "Engineering teams deployed to resolve the issue",
            "Backup systems activated",
            "Customer support capacity increased",
        ],
        "financial_impact": 2500000,
        "timeline": "Expected resolution within 24-48 hours",
        "spokesperson": "Jane Smith, Chief Operating Officer",
        "company_name": "Acme Corporation",
        "customer_impact": "Some customers may experience delayed order processing",
    }
    
    plan = crier.broadcast(
        situation,
        stakeholders=[
            StakeholderType.EMPLOYEES,
            StakeholderType.CUSTOMERS,
            StakeholderType.MEDIA,
        ]
    )
    
    print("\n" + crier.get_communication_report(plan))
    
    # Show one full message
    print("\n" + "=" * 50)
    print("SAMPLE MESSAGE (Customers):")
    print("=" * 50)
    for msg in plan.messages:
        if msg.stakeholder == StakeholderType.CUSTOMERS:
            print(f"Subject: {msg.subject}")
            print("-" * 50)
            print(msg.content)
