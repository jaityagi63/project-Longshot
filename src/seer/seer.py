"""
Seer Module - Prediction Engine
================================
Simulates the Domino Effect chain reaction of events.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ImpactCategory(Enum):
    """Categories of impact."""
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    REPUTATIONAL = "reputational"
    REGULATORY = "regulatory"
    STRATEGIC = "strategic"


class Severity(Enum):
    """Severity levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class DominoEffect:
    """Represents a single domino in the chain reaction."""
    id: str
    description: str
    category: ImpactCategory
    severity: Severity
    probability: float  # 0-1
    time_to_impact: timedelta
    dependencies: List[str] = field(default_factory=list)
    triggered_by: Optional[str] = None
    mitigations: List[str] = field(default_factory=list)


@dataclass
class SimulationResult:
    """Result of a domino effect simulation."""
    scenario_id: str
    initial_event: str
    timestamp: str
    chain: List[DominoEffect]
    total_financial_impact: float
    peak_severity: Severity
    time_to_peak: timedelta
    confidence_score: float
    recommendations: List[str]


class Seer:
    """
    The Seer module: Prediction.
    Simulates the Domino Effect chain reaction of events.
    """

    def __init__(self, simulation_depth: int = 5):
        """
        Initialize the Seer.
        
        Args:
            simulation_depth: Maximum depth of domino chain to simulate.
        """
        self.simulation_depth = simulation_depth
        self.effect_templates = self._load_effect_templates()
        self.simulations: List[SimulationResult] = []
    
    def _load_effect_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load predefined effect templates for common scenarios."""
        return {
            "supplier_disruption": [
                {
                    "description": "Production delays due to component shortage",
                    "category": ImpactCategory.OPERATIONAL,
                    "severity": Severity.HIGH,
                    "probability": 0.85,
                    "days_to_impact": 7,
                    "financial_impact": 500000,
                },
                {
                    "description": "Customer order fulfillment failures",
                    "category": ImpactCategory.OPERATIONAL,
                    "severity": Severity.HIGH,
                    "probability": 0.7,
                    "days_to_impact": 14,
                    "financial_impact": 1000000,
                },
                {
                    "description": "Contract penalty clauses triggered",
                    "category": ImpactCategory.FINANCIAL,
                    "severity": Severity.CRITICAL,
                    "probability": 0.5,
                    "days_to_impact": 30,
                    "financial_impact": 2000000,
                },
                {
                    "description": "Negative media coverage",
                    "category": ImpactCategory.REPUTATIONAL,
                    "severity": Severity.MEDIUM,
                    "probability": 0.6,
                    "days_to_impact": 21,
                    "financial_impact": 300000,
                },
                {
                    "description": "Customer churn acceleration",
                    "category": ImpactCategory.STRATEGIC,
                    "severity": Severity.HIGH,
                    "probability": 0.4,
                    "days_to_impact": 60,
                    "financial_impact": 5000000,
                },
            ],
            "cybersecurity_incident": [
                {
                    "description": "System downtime and service interruption",
                    "category": ImpactCategory.OPERATIONAL,
                    "severity": Severity.CRITICAL,
                    "probability": 0.9,
                    "days_to_impact": 0,
                    "financial_impact": 200000,
                },
                {
                    "description": "Data breach notification requirements",
                    "category": ImpactCategory.REGULATORY,
                    "severity": Severity.HIGH,
                    "probability": 0.7,
                    "days_to_impact": 3,
                    "financial_impact": 500000,
                },
                {
                    "description": "Regulatory investigation and fines",
                    "category": ImpactCategory.REGULATORY,
                    "severity": Severity.CRITICAL,
                    "probability": 0.5,
                    "days_to_impact": 30,
                    "financial_impact": 4000000,
                },
                {
                    "description": "Class action lawsuit risk",
                    "category": ImpactCategory.FINANCIAL,
                    "severity": Severity.CRITICAL,
                    "probability": 0.3,
                    "days_to_impact": 90,
                    "financial_impact": 10000000,
                },
                {
                    "description": "Customer trust erosion",
                    "category": ImpactCategory.REPUTATIONAL,
                    "severity": Severity.HIGH,
                    "probability": 0.8,
                    "days_to_impact": 7,
                    "financial_impact": 2000000,
                },
            ],
            "geopolitical_event": [
                {
                    "description": "Supply chain rerouting required",
                    "category": ImpactCategory.OPERATIONAL,
                    "severity": Severity.HIGH,
                    "probability": 0.75,
                    "days_to_impact": 14,
                    "financial_impact": 800000,
                },
                {
                    "description": "Increased logistics costs",
                    "category": ImpactCategory.FINANCIAL,
                    "severity": Severity.MEDIUM,
                    "probability": 0.9,
                    "days_to_impact": 7,
                    "financial_impact": 400000,
                },
                {
                    "description": "Currency exchange volatility",
                    "category": ImpactCategory.FINANCIAL,
                    "severity": Severity.MEDIUM,
                    "probability": 0.6,
                    "days_to_impact": 3,
                    "financial_impact": 600000,
                },
                {
                    "description": "Market access restrictions",
                    "category": ImpactCategory.STRATEGIC,
                    "severity": Severity.CRITICAL,
                    "probability": 0.4,
                    "days_to_impact": 30,
                    "financial_impact": 8000000,
                },
            ],
            "default": [
                {
                    "description": "Operational disruption",
                    "category": ImpactCategory.OPERATIONAL,
                    "severity": Severity.MEDIUM,
                    "probability": 0.6,
                    "days_to_impact": 7,
                    "financial_impact": 250000,
                },
                {
                    "description": "Stakeholder concern escalation",
                    "category": ImpactCategory.REPUTATIONAL,
                    "severity": Severity.LOW,
                    "probability": 0.5,
                    "days_to_impact": 14,
                    "financial_impact": 100000,
                },
            ],
        }
    
    def _classify_event(self, event_text: str) -> str:
        """Classify an event into a scenario type."""
        text_lower = event_text.lower()
        
        if any(word in text_lower for word in ["supplier", "supply chain", "shortage", "manufacturer", "production"]):
            return "supplier_disruption"
        elif any(word in text_lower for word in ["cyber", "hack", "breach", "security", "ransomware", "data leak"]):
            return "cybersecurity_incident"
        elif any(word in text_lower for word in ["sanction", "tariff", "trade war", "geopolitical", "regulation", "embargo"]):
            return "geopolitical_event"
        else:
            return "default"
    
    def prophesy(self, event_summary: str, affected_assets: List[str] = None, 
                 impact_scores: Dict[str, float] = None) -> SimulationResult:
        """
        Simulate the domino effect chain reaction for an event.
        
        Args:
            event_summary: Description of the triggering event.
            affected_assets: List of initially affected asset IDs.
            impact_scores: Initial impact scores per asset.
        
        Returns:
            SimulationResult with the predicted chain of effects.
        """
        print(f"🔮 Seer is prophesying outcomes for: '{event_summary[:50]}...'")
        
        # Classify the event
        scenario_type = self._classify_event(event_summary)
        templates = self.effect_templates.get(scenario_type, self.effect_templates["default"])
        
        print(f"   Scenario classified as: {scenario_type}")
        
        # Build the domino chain
        chain: List[DominoEffect] = []
        total_financial_impact = 0.0
        peak_severity = Severity.LOW
        time_to_peak = timedelta(days=0)
        
        # Use impact scores to modify probabilities if available
        probability_modifier = 1.0
        if impact_scores:
            avg_impact = sum(impact_scores.values()) / len(impact_scores) if impact_scores else 0.5
            probability_modifier = 0.5 + avg_impact  # Range: 0.5 to 1.5
        
        for i, template in enumerate(templates[:self.simulation_depth]):
            # Apply some randomness to simulation
            adjusted_probability = min(1.0, template["probability"] * probability_modifier * random.uniform(0.8, 1.2))
            
            # Simulate whether this domino falls
            if random.random() < adjusted_probability:
                effect = DominoEffect(
                    id=f"DOM-{i+1:03d}",
                    description=template["description"],
                    category=template["category"],
                    severity=template["severity"],
                    probability=adjusted_probability,
                    time_to_impact=timedelta(days=template["days_to_impact"]),
                    triggered_by=chain[-1].id if chain else "INITIAL_EVENT",
                    mitigations=self._generate_mitigations(template["category"], template["severity"]),
                )
                chain.append(effect)
                
                # Track metrics
                total_financial_impact += template["financial_impact"] * adjusted_probability
                if template["severity"].value > peak_severity.value:
                    peak_severity = template["severity"]
                    time_to_peak = effect.time_to_impact
        
        # Generate recommendations
        recommendations = self._generate_recommendations(chain, scenario_type)
        
        # Calculate confidence based on data quality
        confidence = 0.7 if affected_assets else 0.5
        if impact_scores:
            confidence += 0.15
        confidence = min(0.95, confidence + random.uniform(-0.1, 0.1))
        
        result = SimulationResult(
            scenario_id=f"SIM-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            initial_event=event_summary,
            timestamp=datetime.now().isoformat(),
            chain=chain,
            total_financial_impact=total_financial_impact,
            peak_severity=peak_severity,
            time_to_peak=time_to_peak,
            confidence_score=confidence,
            recommendations=recommendations,
        )
        
        self.simulations.append(result)
        
        print(f"✅ Seer predicted {len(chain)} domino effects.")
        print(f"   Peak severity: {peak_severity.name}, Est. financial impact: ${total_financial_impact:,.0f}")
        
        return result
    
    def _generate_mitigations(self, category: ImpactCategory, severity: Severity) -> List[str]:
        """Generate mitigation suggestions based on impact category and severity."""
        mitigations = {
            ImpactCategory.FINANCIAL: [
                "Activate emergency reserve funds",
                "Negotiate payment deferrals with vendors",
                "Review insurance coverage options",
            ],
            ImpactCategory.OPERATIONAL: [
                "Activate backup suppliers",
                "Implement contingency production schedule",
                "Redeploy resources to critical operations",
            ],
            ImpactCategory.REPUTATIONAL: [
                "Prepare proactive media statement",
                "Engage PR crisis management team",
                "Increase customer communication frequency",
            ],
            ImpactCategory.REGULATORY: [
                "Engage legal counsel immediately",
                "Document all actions for compliance",
                "Prepare regulatory disclosure materials",
            ],
            ImpactCategory.STRATEGIC: [
                "Convene emergency board session",
                "Review long-term strategic alternatives",
                "Assess market repositioning options",
            ],
        }
        
        base_mitigations = mitigations.get(category, ["Review situation and assess options"])
        
        if severity in [Severity.HIGH, Severity.CRITICAL]:
            base_mitigations.insert(0, "⚠️ URGENT: Escalate to executive leadership")
        
        return base_mitigations[:2]  # Return top 2 most relevant
    
    def _generate_recommendations(self, chain: List[DominoEffect], scenario_type: str) -> List[str]:
        """Generate overall recommendations based on the simulation."""
        recommendations = []
        
        # Count categories
        category_counts = {}
        for effect in chain:
            cat = effect.category.value
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Generate recommendations based on dominant categories
        if category_counts.get("operational", 0) >= 2:
            recommendations.append("🔧 Prioritize operational continuity measures")
        if category_counts.get("financial", 0) >= 2:
            recommendations.append("💰 Activate financial contingency protocols")
        if category_counts.get("reputational", 0) >= 1:
            recommendations.append("📢 Prepare stakeholder communication strategy")
        if category_counts.get("regulatory", 0) >= 1:
            recommendations.append("⚖️ Engage legal and compliance teams immediately")
        
        # Scenario-specific recommendations
        if scenario_type == "supplier_disruption":
            recommendations.append("🏭 Identify and pre-qualify alternative suppliers")
        elif scenario_type == "cybersecurity_incident":
            recommendations.append("🔐 Activate incident response plan")
        elif scenario_type == "geopolitical_event":
            recommendations.append("🌍 Monitor situation for further developments")
        
        if not recommendations:
            recommendations.append("📊 Continue monitoring and reassess in 24 hours")
        
        return recommendations
    
    def get_simulation_summary(self, result: SimulationResult) -> str:
        """Generate a human-readable summary of a simulation."""
        lines = [
            f"📊 SEER SIMULATION REPORT",
            f"{'=' * 50}",
            f"Scenario ID: {result.scenario_id}",
            f"Initial Event: {result.initial_event}",
            f"Confidence: {result.confidence_score:.0%}",
            f"",
            f"📈 IMPACT SUMMARY",
            f"  Total Est. Financial Impact: ${result.total_financial_impact:,.0f}",
            f"  Peak Severity: {result.peak_severity.name}",
            f"  Time to Peak: {result.time_to_peak.days} days",
            f"",
            f"🎯 DOMINO CHAIN ({len(result.chain)} effects):",
        ]
        
        for i, effect in enumerate(result.chain, 1):
            lines.append(f"  {i}. [{effect.severity.name}] {effect.description}")
            lines.append(f"     Category: {effect.category.value} | Probability: {effect.probability:.0%}")
        
        lines.append("")
        lines.append("💡 RECOMMENDATIONS:")
        for rec in result.recommendations:
            lines.append(f"  • {rec}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test the Seer
    seer = Seer()
    
    # Simulate a supply chain event
    result = seer.prophesy(
        event_summary="Major semiconductor supplier announces production halt due to factory fire",
        affected_assets=["SUP-001", "PROD-001"],
        impact_scores={"SUP-001": 0.85, "PROD-001": 0.6}
    )
    
    print("\n" + seer.get_simulation_summary(result))
