"""
Council Module - Multi-Agent Strategy Debate
=============================================
Multi-agent debate system with Ops, Legal, Finance, and PR perspectives.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod


class Perspective(Enum):
    """Council member perspectives."""
    OPERATIONS = "operations"
    LEGAL = "legal"
    FINANCE = "finance"
    PUBLIC_RELATIONS = "public_relations"
    SECURITY = "security"
    STRATEGY = "strategy"


class Priority(Enum):
    """Priority levels for recommendations."""
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1


@dataclass
class Argument:
    """An argument made by a council member."""
    member: Perspective
    position: str
    supporting_points: List[str]
    risks: List[str]
    priority: Priority
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Consensus:
    """The final consensus of the council."""
    decision: str
    confidence: float
    supporting_members: List[Perspective]
    dissenting_members: List[Perspective]
    action_items: List[Dict[str, Any]]
    timeline: str
    risks_acknowledged: List[str]


@dataclass
class DebateResult:
    """Result of a council debate session."""
    session_id: str
    topic: str
    timestamp: str
    arguments: List[Argument]
    consensus: Optional[Consensus]
    debate_rounds: int
    summary: str


class CouncilMember(ABC):
    """Abstract base class for council members."""
    
    def __init__(self, perspective: Perspective):
        self.perspective = perspective
    
    @abstractmethod
    def analyze(self, situation: Dict[str, Any]) -> Argument:
        """Analyze a situation and provide perspective."""
        pass
    
    @abstractmethod
    def respond_to(self, argument: Argument) -> Optional[str]:
        """Respond to another member's argument."""
        pass


class OperationsMember(CouncilMember):
    """Operations perspective - focuses on continuity and execution."""
    
    def __init__(self):
        super().__init__(Perspective.OPERATIONS)
    
    def analyze(self, situation: Dict[str, Any]) -> Argument:
        severity = situation.get("severity", "medium")
        affected_assets = situation.get("affected_assets", [])
        
        if severity == "critical":
            position = "Immediate operational contingency activation required"
            points = [
                "Activate backup suppliers and alternative workflows",
                "Establish war room for real-time coordination",
                "Implement emergency staffing protocols",
            ]
            risks = [
                "Delayed response could cascade into customer-facing failures",
                "Resource reallocation may strain other operations",
            ]
            priority = Priority.CRITICAL
        elif severity == "high":
            position = "Proactive operational adjustments recommended"
            points = [
                "Pre-position backup resources",
                "Increase monitoring frequency",
                "Prepare contingency communication chains",
            ]
            risks = [
                "Over-preparation costs if situation de-escalates",
            ]
            priority = Priority.HIGH
        else:
            position = "Standard monitoring with documented escalation triggers"
            points = [
                "Monitor situation through normal channels",
                "Document escalation criteria",
            ]
            risks = ["Minimal operational risk at current level"]
            priority = Priority.MEDIUM
        
        return Argument(
            member=self.perspective,
            position=position,
            supporting_points=points,
            risks=risks,
            priority=priority,
        )
    
    def respond_to(self, argument: Argument) -> Optional[str]:
        if argument.member == Perspective.FINANCE:
            return "Cost concerns noted, but operational continuity must be prioritized to protect revenue streams"
        elif argument.member == Perspective.LEGAL:
            return "Will coordinate with legal on compliance requirements for contingency measures"
        return None


class LegalMember(CouncilMember):
    """Legal perspective - focuses on compliance and liability."""
    
    def __init__(self):
        super().__init__(Perspective.LEGAL)
    
    def analyze(self, situation: Dict[str, Any]) -> Argument:
        threat_type = situation.get("threat_type", "unknown")
        regulatory_exposure = situation.get("regulatory_exposure", False)
        
        if regulatory_exposure or "regulatory" in str(situation.get("categories", [])):
            position = "Immediate legal review and compliance documentation required"
            points = [
                "Engage outside counsel for regulatory matters",
                "Preserve all relevant documents and communications",
                "Prepare regulatory disclosure materials",
                "Review contractual obligations and force majeure clauses",
            ]
            risks = [
                "Regulatory penalties for delayed disclosure",
                "Potential shareholder litigation exposure",
                "Contractual breach claims from counterparties",
            ]
            priority = Priority.CRITICAL
        elif threat_type in ["cybersecurity_incident", "data_breach"]:
            position = "Data breach response protocol activation"
            points = [
                "Assess notification requirements (GDPR, CCPA, etc.)",
                "Document incident timeline for regulators",
                "Engage forensics and preserve evidence",
            ]
            risks = [
                "Class action exposure if mishandled",
                "Regulatory fines for delayed notification",
            ]
            priority = Priority.CRITICAL
        else:
            position = "Standard legal monitoring with contract review"
            points = [
                "Review relevant contracts for implications",
                "Monitor for regulatory developments",
            ]
            risks = ["Standard contractual risks"]
            priority = Priority.MEDIUM
        
        return Argument(
            member=self.perspective,
            position=position,
            supporting_points=points,
            risks=risks,
            priority=priority,
        )
    
    def respond_to(self, argument: Argument) -> Optional[str]:
        if argument.member == Perspective.PUBLIC_RELATIONS:
            return "All external communications must be reviewed by legal before release"
        elif argument.member == Perspective.OPERATIONS:
            return "Operational changes must be documented for potential regulatory review"
        return None


class FinanceMember(CouncilMember):
    """Finance perspective - focuses on costs and financial impact."""
    
    def __init__(self):
        super().__init__(Perspective.FINANCE)
    
    def analyze(self, situation: Dict[str, Any]) -> Argument:
        estimated_impact = situation.get("financial_impact", 0)
        
        if estimated_impact > 5000000:
            position = "Major financial contingency measures required"
            points = [
                "Activate emergency reserve authorization",
                "Review credit facilities and liquidity position",
                "Prepare board notification on material impact",
                "Assess insurance coverage and claims process",
            ]
            risks = [
                "Material impact on quarterly earnings",
                "Potential credit rating implications",
                "Shareholder disclosure requirements",
            ]
            priority = Priority.CRITICAL
        elif estimated_impact > 1000000:
            position = "Significant budget reallocation may be needed"
            points = [
                "Identify budget reallocation opportunities",
                "Review insurance deductibles and coverage",
                "Prepare variance explanations for stakeholders",
            ]
            risks = [
                "Impact on departmental budgets",
                "Potential project deferrals",
            ]
            priority = Priority.HIGH
        else:
            position = "Manageable within existing budgets with monitoring"
            points = [
                "Track expenditures against contingency reserves",
                "Document costs for potential recovery",
            ]
            risks = ["Minimal financial exposure at current level"]
            priority = Priority.LOW
        
        return Argument(
            member=self.perspective,
            position=position,
            supporting_points=points,
            risks=risks,
            priority=priority,
        )
    
    def respond_to(self, argument: Argument) -> Optional[str]:
        if argument.member == Perspective.OPERATIONS:
            return "All contingency spending requires documented ROI and impact justification"
        return None


class PublicRelationsMember(CouncilMember):
    """PR perspective - focuses on reputation and stakeholder communications."""
    
    def __init__(self):
        super().__init__(Perspective.PUBLIC_RELATIONS)
    
    def analyze(self, situation: Dict[str, Any]) -> Argument:
        media_exposure = situation.get("media_exposure", "none")
        customer_impact = situation.get("customer_impact", False)
        
        if media_exposure == "high" or customer_impact:
            position = "Proactive stakeholder communication strategy required"
            points = [
                "Prepare holding statement for media inquiries",
                "Draft customer notification templates",
                "Activate social media monitoring",
                "Brief executive spokespersons",
            ]
            risks = [
                "Reputation damage from perceived inaction",
                "Social media amplification of negative sentiment",
                "Customer churn from poor communication",
            ]
            priority = Priority.HIGH
        elif media_exposure == "medium":
            position = "Prepared response posture with monitoring"
            points = [
                "Draft Q&A for potential inquiries",
                "Increase social listening frequency",
            ]
            risks = ["Potential for unexpected media attention"]
            priority = Priority.MEDIUM
        else:
            position = "Standard monitoring, no proactive communication needed"
            points = [
                "Continue routine stakeholder communications",
            ]
            risks = ["Minimal reputational exposure"]
            priority = Priority.LOW
        
        return Argument(
            member=self.perspective,
            position=position,
            supporting_points=points,
            risks=risks,
            priority=priority,
        )
    
    def respond_to(self, argument: Argument) -> Optional[str]:
        if argument.member == Perspective.LEGAL:
            return "Will coordinate messaging with legal review requirements"
        return None


class Council:
    """
    The Council module: Strategy.
    Multi-agent debate system for strategic decision-making.
    """

    def __init__(self, debate_rounds: int = 3):
        """
        Initialize the Council.
        
        Args:
            debate_rounds: Number of debate rounds before consensus.
        """
        self.debate_rounds = debate_rounds
        self.members: Dict[Perspective, CouncilMember] = {
            Perspective.OPERATIONS: OperationsMember(),
            Perspective.LEGAL: LegalMember(),
            Perspective.FINANCE: FinanceMember(),
            Perspective.PUBLIC_RELATIONS: PublicRelationsMember(),
        }
        self.sessions: List[DebateResult] = []
    
    def convene(self, situation: Dict[str, Any]) -> DebateResult:
        """
        Convene the council to debate a situation.
        
        Args:
            situation: Dictionary describing the situation with keys:
                - summary: Brief description
                - severity: low/medium/high/critical
                - affected_assets: List of affected assets
                - financial_impact: Estimated financial impact
                - threat_type: Type of threat
                - regulatory_exposure: Boolean
                - media_exposure: none/low/medium/high
                - customer_impact: Boolean
        
        Returns:
            DebateResult with all arguments and consensus.
        """
        topic = situation.get("summary", "Unknown situation")
        print(f"👥 Council convening on: '{topic[:50]}...'")
        
        session_id = f"COUNCIL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        arguments: List[Argument] = []
        
        # First round: Each member provides initial analysis
        print("   Round 1: Initial positions...")
        for perspective, member in self.members.items():
            arg = member.analyze(situation)
            arguments.append(arg)
            print(f"     {perspective.value}: {arg.position[:50]}...")
        
        # Subsequent rounds: Members respond to each other
        for round_num in range(2, self.debate_rounds + 1):
            print(f"   Round {round_num}: Cross-examination...")
            for perspective, member in self.members.items():
                for arg in arguments:
                    if arg.member != perspective:
                        response = member.respond_to(arg)
                        if response:
                            # Add response as supporting point to original argument
                            pass  # In a full implementation, this would modify arguments
        
        # Build consensus
        consensus = self._build_consensus(arguments, situation)
        
        # Generate summary
        summary = self._generate_summary(arguments, consensus)
        
        result = DebateResult(
            session_id=session_id,
            topic=topic,
            timestamp=datetime.now().isoformat(),
            arguments=arguments,
            consensus=consensus,
            debate_rounds=self.debate_rounds,
            summary=summary,
        )
        
        self.sessions.append(result)
        
        print(f"✅ Council reached consensus: {consensus.decision[:50]}...")
        
        return result
    
    def _build_consensus(self, arguments: List[Argument], situation: Dict[str, Any]) -> Consensus:
        """Build consensus from arguments."""
        # Determine highest priority
        max_priority = max(arg.priority.value for arg in arguments)
        critical_args = [arg for arg in arguments if arg.priority.value == max_priority]
        
        # Identify supporting and dissenting members
        supporting = [arg.member for arg in critical_args]
        dissenting = [arg.member for arg in arguments if arg.member not in supporting]
        
        # Build action items from all arguments
        action_items = []
        for arg in arguments:
            for point in arg.supporting_points[:2]:  # Top 2 from each
                action_items.append({
                    "action": point,
                    "owner": arg.member.value,
                    "priority": arg.priority.name,
                })
        
        # Aggregate risks
        all_risks = []
        for arg in arguments:
            all_risks.extend(arg.risks)
        
        # Determine timeline based on severity
        severity = situation.get("severity", "medium")
        if severity == "critical":
            timeline = "Immediate (within 24 hours)"
        elif severity == "high":
            timeline = "Urgent (within 72 hours)"
        else:
            timeline = "Standard (within 1 week)"
        
        # Calculate confidence based on agreement level
        agreement_ratio = len(supporting) / len(arguments)
        confidence = 0.5 + (agreement_ratio * 0.4)
        
        # Generate decision statement
        if max_priority == Priority.CRITICAL.value:
            decision = "CRITICAL RESPONSE REQUIRED: Activate all contingency protocols across Operations, Legal, Finance, and Communications"
        elif max_priority == Priority.HIGH.value:
            decision = "HIGH PRIORITY RESPONSE: Proactive measures required with executive oversight"
        elif max_priority == Priority.MEDIUM.value:
            decision = "MEASURED RESPONSE: Enhanced monitoring with prepared contingencies"
        else:
            decision = "STANDARD RESPONSE: Continue normal operations with awareness"
        
        return Consensus(
            decision=decision,
            confidence=confidence,
            supporting_members=supporting,
            dissenting_members=dissenting,
            action_items=action_items,
            timeline=timeline,
            risks_acknowledged=list(set(all_risks))[:5],  # Top 5 unique risks
        )
    
    def _generate_summary(self, arguments: List[Argument], consensus: Consensus) -> str:
        """Generate a narrative summary of the debate."""
        summary_parts = [
            f"The Council convened and heard from {len(arguments)} perspectives.",
            f"After {self.debate_rounds} rounds of deliberation, a consensus was reached.",
            f"",
            f"DECISION: {consensus.decision}",
            f"",
            f"Timeline: {consensus.timeline}",
            f"Confidence: {consensus.confidence:.0%}",
        ]
        return "\n".join(summary_parts)
    
    def get_debate_report(self, result: DebateResult) -> str:
        """Generate a detailed human-readable report."""
        lines = [
            f"👥 COUNCIL DEBATE REPORT",
            f"{'=' * 50}",
            f"Session: {result.session_id}",
            f"Topic: {result.topic}",
            f"Rounds: {result.debate_rounds}",
            f"",
            f"📣 MEMBER POSITIONS:",
        ]
        
        for arg in result.arguments:
            lines.append(f"\n  [{arg.priority.name}] {arg.member.value.upper()}")
            lines.append(f"  Position: {arg.position}")
            lines.append(f"  Key Points:")
            for point in arg.supporting_points[:2]:
                lines.append(f"    • {point}")
        
        if result.consensus:
            lines.append(f"\n{'─' * 50}")
            lines.append(f"✅ CONSENSUS REACHED")
            lines.append(f"Decision: {result.consensus.decision}")
            lines.append(f"Timeline: {result.consensus.timeline}")
            lines.append(f"Confidence: {result.consensus.confidence:.0%}")
            lines.append(f"\n📋 ACTION ITEMS:")
            for item in result.consensus.action_items[:5]:
                lines.append(f"  [{item['priority']}] {item['owner']}: {item['action']}")
            
            lines.append(f"\n⚠️ ACKNOWLEDGED RISKS:")
            for risk in result.consensus.risks_acknowledged:
                lines.append(f"  • {risk}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test the Council
    council = Council(debate_rounds=3)
    
    # Simulate a crisis situation
    situation = {
        "summary": "Major supplier bankruptcy announced, affecting critical components",
        "severity": "high",
        "affected_assets": ["SUP-001", "PROD-001", "CON-001"],
        "financial_impact": 3500000,
        "threat_type": "supplier_disruption",
        "regulatory_exposure": False,
        "media_exposure": "medium",
        "customer_impact": True,
    }
    
    result = council.convene(situation)
    print("\n" + council.get_debate_report(result))
