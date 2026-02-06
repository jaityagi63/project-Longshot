"""
Black Box Module - Hindsight Analysis
======================================
Re-runs simulations to find what could have been done better.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random


class DecisionPoint(Enum):
    """Types of decision points that can be analyzed."""
    DETECTION = "detection"
    ESCALATION = "escalation"
    RESPONSE_SELECTION = "response_selection"
    RESOURCE_ALLOCATION = "resource_allocation"
    COMMUNICATION = "communication"
    MITIGATION = "mitigation"


@dataclass
class AlternativeScenario:
    """An alternative scenario/decision that could have been made."""
    id: str
    decision_point: DecisionPoint
    original_decision: str
    alternative_decision: str
    projected_outcome: Dict[str, Any]
    improvement_potential: float  # -1 to 1 (negative = worse)
    feasibility: float  # 0 to 1
    rationale: str


@dataclass
class HindsightAnalysis:
    """Complete hindsight analysis of an incident."""
    analysis_id: str
    incident_id: str
    timestamp: str
    original_outcome: Dict[str, Any]
    decision_points_analyzed: List[DecisionPoint]
    alternatives: List[AlternativeScenario]
    optimal_path: List[str]
    potential_savings: float
    time_savings: timedelta
    key_insights: List[str]
    recommendations: List[str]


class BlackBox:
    """
    The Black Box module: Hindsight.
    Re-runs simulations to find what could have been done better.
    """

    def __init__(self):
        """Initialize the Black Box."""
        self.analyses: List[HindsightAnalysis] = []
        self.decision_templates = self._load_decision_templates()
    
    def _load_decision_templates(self) -> Dict[DecisionPoint, List[Dict[str, Any]]]:
        """Load templates for alternative decisions at each decision point."""
        return {
            DecisionPoint.DETECTION: [
                {
                    "alternative": "Earlier detection through enhanced monitoring",
                    "time_improvement_hours": 12,
                    "cost_reduction_pct": 0.15,
                    "feasibility": 0.8,
                },
                {
                    "alternative": "Automated alerting on leading indicators",
                    "time_improvement_hours": 24,
                    "cost_reduction_pct": 0.25,
                    "feasibility": 0.6,
                },
                {
                    "alternative": "Third-party intelligence feed integration",
                    "time_improvement_hours": 48,
                    "cost_reduction_pct": 0.35,
                    "feasibility": 0.7,
                },
            ],
            DecisionPoint.ESCALATION: [
                {
                    "alternative": "Immediate executive escalation",
                    "time_improvement_hours": 4,
                    "cost_reduction_pct": 0.10,
                    "feasibility": 0.9,
                },
                {
                    "alternative": "Pre-defined escalation automation",
                    "time_improvement_hours": 2,
                    "cost_reduction_pct": 0.05,
                    "feasibility": 0.85,
                },
            ],
            DecisionPoint.RESPONSE_SELECTION: [
                {
                    "alternative": "Aggressive mitigation strategy",
                    "time_improvement_hours": 0,
                    "cost_reduction_pct": 0.20,
                    "feasibility": 0.6,
                },
                {
                    "alternative": "Conservative containment approach",
                    "time_improvement_hours": 0,
                    "cost_reduction_pct": -0.10,  # Might cost more but safer
                    "feasibility": 0.9,
                },
                {
                    "alternative": "Parallel multi-pronged response",
                    "time_improvement_hours": -6,  # Faster but more resources
                    "cost_reduction_pct": 0.15,
                    "feasibility": 0.5,
                },
            ],
            DecisionPoint.RESOURCE_ALLOCATION: [
                {
                    "alternative": "Pre-positioned emergency resources",
                    "time_improvement_hours": 8,
                    "cost_reduction_pct": 0.12,
                    "feasibility": 0.7,
                },
                {
                    "alternative": "Cross-functional rapid response team",
                    "time_improvement_hours": 4,
                    "cost_reduction_pct": 0.08,
                    "feasibility": 0.8,
                },
            ],
            DecisionPoint.COMMUNICATION: [
                {
                    "alternative": "Proactive stakeholder notification",
                    "time_improvement_hours": 0,
                    "cost_reduction_pct": 0.05,
                    "feasibility": 0.9,
                },
                {
                    "alternative": "Real-time status dashboard",
                    "time_improvement_hours": 0,
                    "cost_reduction_pct": 0.03,
                    "feasibility": 0.75,
                },
            ],
            DecisionPoint.MITIGATION: [
                {
                    "alternative": "Backup supplier activation within 4 hours",
                    "time_improvement_hours": 24,
                    "cost_reduction_pct": 0.30,
                    "feasibility": 0.4,
                },
                {
                    "alternative": "Insurance claim filed immediately",
                    "time_improvement_hours": 0,
                    "cost_reduction_pct": 0.40,
                    "feasibility": 0.7,
                },
            ],
        }
    
    def analyze(self, incident_data: Dict[str, Any]) -> HindsightAnalysis:
        """
        Perform hindsight analysis on an incident.
        
        Args:
            incident_data: Dictionary containing incident details:
                - incident_id: Unique identifier
                - summary: What happened
                - timeline: List of events with timestamps
                - decisions_made: List of decisions that were made
                - outcome: Final outcome metrics
                - duration_hours: How long the incident lasted
                - financial_impact: Total financial impact
        
        Returns:
            HindsightAnalysis with alternatives and recommendations.
        """
        incident_id = incident_data.get("incident_id", "UNKNOWN")
        print(f"📦 Black Box analyzing incident: {incident_id}")
        
        original_outcome = {
            "duration_hours": incident_data.get("duration_hours", 48),
            "financial_impact": incident_data.get("financial_impact", 1000000),
            "severity": incident_data.get("severity", "high"),
            "stakeholders_affected": incident_data.get("stakeholders_affected", 100),
        }
        
        # Analyze each decision point
        alternatives: List[AlternativeScenario] = []
        decision_points = list(DecisionPoint)
        
        for dp in decision_points:
            templates = self.decision_templates.get(dp, [])
            
            for i, template in enumerate(templates):
                # Simulate the alternative scenario
                alt_id = f"ALT-{dp.value[:3].upper()}-{i+1:02d}"
                
                # Calculate projected improvements
                time_improvement = template.get("time_improvement_hours", 0)
                cost_reduction = template.get("cost_reduction_pct", 0)
                
                projected_outcome = {
                    "duration_hours": max(1, original_outcome["duration_hours"] - time_improvement),
                    "financial_impact": original_outcome["financial_impact"] * (1 - cost_reduction),
                    "time_saved_hours": time_improvement,
                    "cost_saved": original_outcome["financial_impact"] * cost_reduction,
                }
                
                # Add some variance
                projected_outcome["financial_impact"] *= random.uniform(0.9, 1.1)
                
                alternative = AlternativeScenario(
                    id=alt_id,
                    decision_point=dp,
                    original_decision=incident_data.get("decisions_made", {}).get(dp.value, "Standard protocol followed"),
                    alternative_decision=template["alternative"],
                    projected_outcome=projected_outcome,
                    improvement_potential=cost_reduction + (time_improvement / 100),
                    feasibility=template.get("feasibility", 0.5),
                    rationale=f"Based on analysis of similar incidents and best practices",
                )
                alternatives.append(alternative)
        
        # Sort alternatives by improvement potential weighted by feasibility
        alternatives.sort(
            key=lambda a: a.improvement_potential * a.feasibility,
            reverse=True
        )
        
        # Determine optimal path (top alternatives with high feasibility)
        optimal_path = []
        for alt in alternatives:
            if alt.feasibility >= 0.7 and alt.improvement_potential > 0:
                optimal_path.append(f"{alt.decision_point.value}: {alt.alternative_decision}")
                if len(optimal_path) >= 5:
                    break
        
        # Calculate total potential savings
        top_alternatives = [a for a in alternatives[:5] if a.improvement_potential > 0]
        potential_savings = sum(
            a.projected_outcome.get("cost_saved", 0) * a.feasibility 
            for a in top_alternatives
        )
        time_savings = timedelta(hours=sum(
            a.projected_outcome.get("time_saved_hours", 0) * a.feasibility
            for a in top_alternatives
        ))
        
        # Generate key insights
        key_insights = self._generate_insights(alternatives, original_outcome)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(alternatives)
        
        analysis = HindsightAnalysis(
            analysis_id=f"BB-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            incident_id=incident_id,
            timestamp=datetime.now().isoformat(),
            original_outcome=original_outcome,
            decision_points_analyzed=decision_points,
            alternatives=alternatives,
            optimal_path=optimal_path,
            potential_savings=potential_savings,
            time_savings=time_savings,
            key_insights=key_insights,
            recommendations=recommendations,
        )
        
        self.analyses.append(analysis)
        
        print(f"✅ Black Box analysis complete. Potential savings: ${potential_savings:,.0f}")
        return analysis
    
    def _generate_insights(self, alternatives: List[AlternativeScenario],
                           original_outcome: Dict[str, Any]) -> List[str]:
        """Generate key insights from the analysis."""
        insights = []
        
        # Find highest impact decision point
        dp_impacts = {}
        for alt in alternatives:
            dp = alt.decision_point.value
            if dp not in dp_impacts:
                dp_impacts[dp] = []
            dp_impacts[dp].append(alt.improvement_potential)
        
        best_dp = max(dp_impacts.items(), key=lambda x: max(x[1]) if x[1] else 0)
        insights.append(f"Highest improvement potential at {best_dp[0]} decision point")
        
        # Detection insights
        detection_alts = [a for a in alternatives if a.decision_point == DecisionPoint.DETECTION]
        if detection_alts:
            best_detection = max(detection_alts, key=lambda a: a.improvement_potential)
            if best_detection.improvement_potential > 0.2:
                insights.append(f"Earlier detection could have reduced impact by {best_detection.improvement_potential:.0%}")
        
        # Cost insights
        high_feasible = [a for a in alternatives if a.feasibility >= 0.8 and a.improvement_potential > 0]
        if high_feasible:
            avg_improvement = sum(a.improvement_potential for a in high_feasible) / len(high_feasible)
            insights.append(f"Highly feasible improvements average {avg_improvement:.0%} impact reduction")
        
        # Time insights
        time_savers = [a for a in alternatives if a.projected_outcome.get("time_saved_hours", 0) > 0]
        if time_savers:
            total_time = sum(a.projected_outcome.get("time_saved_hours", 0) for a in time_savers[:3])
            insights.append(f"Top time-saving measures could have saved up to {total_time:.0f} hours")
        
        return insights
    
    def _generate_recommendations(self, alternatives: List[AlternativeScenario]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Get top feasible alternatives
        feasible_alts = sorted(
            [a for a in alternatives if a.feasibility >= 0.6 and a.improvement_potential > 0.1],
            key=lambda a: a.improvement_potential * a.feasibility,
            reverse=True
        )
        
        for alt in feasible_alts[:5]:
            rec = f"[{alt.decision_point.value.upper()}] Implement: {alt.alternative_decision} "
            rec += f"(Est. {alt.improvement_potential:.0%} improvement, {alt.feasibility:.0%} feasibility)"
            recommendations.append(rec)
        
        if not recommendations:
            recommendations.append("Current response protocols appear optimal for this scenario type")
        
        return recommendations
    
    def compare_scenarios(self, analysis: HindsightAnalysis, 
                          scenario_ids: List[str]) -> Dict[str, Any]:
        """Compare specific alternative scenarios."""
        scenarios = [a for a in analysis.alternatives if a.id in scenario_ids]
        
        if not scenarios:
            return {"error": "No matching scenarios found"}
        
        comparison = {
            "scenarios": [],
            "best_overall": None,
            "best_feasible": None,
        }
        
        for s in scenarios:
            comparison["scenarios"].append({
                "id": s.id,
                "decision_point": s.decision_point.value,
                "alternative": s.alternative_decision,
                "improvement": s.improvement_potential,
                "feasibility": s.feasibility,
                "weighted_score": s.improvement_potential * s.feasibility,
            })
        
        if scenarios:
            comparison["best_overall"] = max(scenarios, key=lambda s: s.improvement_potential).id
            comparison["best_feasible"] = max(scenarios, key=lambda s: s.improvement_potential * s.feasibility).id
        
        return comparison
    
    def get_analysis_report(self, analysis: HindsightAnalysis) -> str:
        """Generate a human-readable analysis report."""
        lines = [
            f"📦 BLACK BOX HINDSIGHT ANALYSIS",
            f"{'=' * 50}",
            f"Analysis ID: {analysis.analysis_id}",
            f"Incident: {analysis.incident_id}",
            f"Date: {analysis.timestamp}",
            f"",
            f"📊 ORIGINAL OUTCOME:",
            f"  Duration: {analysis.original_outcome.get('duration_hours', 'N/A')} hours",
            f"  Financial Impact: ${analysis.original_outcome.get('financial_impact', 0):,.0f}",
            f"  Severity: {analysis.original_outcome.get('severity', 'N/A')}",
            f"",
            f"✨ POTENTIAL IMPROVEMENTS:",
            f"  Total Potential Savings: ${analysis.potential_savings:,.0f}",
            f"  Time Savings: {analysis.time_savings}",
            f"",
            f"🛤️ OPTIMAL PATH:",
        ]
        
        for step in analysis.optimal_path:
            lines.append(f"  → {step}")
        
        lines.append(f"\n💡 KEY INSIGHTS:")
        for insight in analysis.key_insights:
            lines.append(f"  • {insight}")
        
        lines.append(f"\n🔝 TOP ALTERNATIVES ({len(analysis.alternatives)} analyzed):")
        for alt in analysis.alternatives[:5]:
            lines.append(f"\n  [{alt.id}] {alt.decision_point.value.upper()}")
            lines.append(f"    Alternative: {alt.alternative_decision}")
            lines.append(f"    Improvement: {alt.improvement_potential:.0%} | Feasibility: {alt.feasibility:.0%}")
        
        lines.append(f"\n📋 RECOMMENDATIONS:")
        for rec in analysis.recommendations:
            lines.append(f"  {rec}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test the Black Box
    bb = BlackBox()
    
    incident = {
        "incident_id": "INC-2024-001",
        "summary": "Major supplier disruption affecting production",
        "timeline": [
            {"time": "T+0", "event": "Supplier announces halt"},
            {"time": "T+2h", "event": "Internal teams notified"},
            {"time": "T+4h", "event": "Emergency meeting convened"},
            {"time": "T+24h", "event": "Alternative supplier identified"},
            {"time": "T+72h", "event": "Partial production resumed"},
        ],
        "decisions_made": {
            "detection": "Learned from news reports (reactive)",
            "escalation": "Escalated after 2 hours",
            "response_selection": "Standard contingency plan activated",
            "resource_allocation": "Existing team resources only",
            "communication": "Customer notification at T+48h",
            "mitigation": "Alternative supplier at market rates",
        },
        "outcome": {
            "resolved": True,
            "customer_impact": "Moderate",
        },
        "duration_hours": 72,
        "financial_impact": 2500000,
        "severity": "high",
        "stakeholders_affected": 500,
    }
    
    analysis = bb.analyze(incident)
    print("\n" + bb.get_analysis_report(analysis))
