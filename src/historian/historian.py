"""
Historian Module - Wisdom & Precedents
=======================================
Retrieves precedents and stores post-mortem lessons.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
import hashlib


@dataclass
class Precedent:
    """A historical precedent/case study."""
    id: str
    title: str
    date: str
    category: str  # supply_chain, cyber, geopolitical, financial, operational
    summary: str
    what_happened: str
    impact: Dict[str, Any]
    response_actions: List[str]
    outcome: str
    lessons_learned: List[str]
    keywords: List[str]
    relevance_score: float = 0.0


@dataclass
class PostMortem:
    """A post-mortem analysis of an incident."""
    id: str
    incident_id: str
    date: str
    title: str
    timeline: List[Dict[str, str]]
    root_cause: str
    contributing_factors: List[str]
    what_went_well: List[str]
    what_went_wrong: List[str]
    action_items: List[Dict[str, Any]]
    lessons_learned: List[str]
    recommendations: List[str]


class Historian:
    """
    The Historian module: Wisdom.
    Retrieves precedents and stores post-mortem lessons.
    """

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize the Historian.
        
        Args:
            storage_path: Path to store precedents and post-mortems.
        """
        self.storage_path = storage_path or Path("data/precedents")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.precedents: Dict[str, Precedent] = {}
        self.post_mortems: Dict[str, PostMortem] = {}
        
        self._load_demo_precedents()
    
    def _load_demo_precedents(self):
        """Load demonstration precedents."""
        demo_precedents = [
            Precedent(
                id="PREC-2011-THAI-FLOOD",
                title="2011 Thailand Floods - Hard Drive Supply Crisis",
                date="2011-10-01",
                category="supply_chain",
                summary="Massive flooding in Thailand disrupted global hard drive production, causing shortages and price spikes lasting over a year.",
                what_happened="Severe flooding affected major hard drive manufacturing facilities in Thailand, which produced 40% of global supply. Western Digital and other manufacturers lost significant production capacity.",
                impact={
                    "financial": "Industry losses estimated at $45 billion",
                    "duration": "18 months to full recovery",
                    "price_increase": "40-80% for hard drives",
                    "affected_industries": ["computing", "servers", "consumer electronics"],
                },
                response_actions=[
                    "Activated secondary suppliers in other regions",
                    "Expedited inventory from unaffected facilities",
                    "Customers implemented rationing and allocation",
                    "Accelerated SSD adoption as alternative",
                ],
                outcome="Industry recovered but accelerated shift to solid-state storage. Companies diversified manufacturing locations.",
                lessons_learned=[
                    "Geographic concentration of suppliers creates systemic risk",
                    "Maintain strategic inventory buffers for critical components",
                    "Develop relationships with alternative suppliers before crisis",
                    "Consider alternative technologies as backup",
                ],
                keywords=["flooding", "thailand", "hard drive", "supply chain", "manufacturing", "shortage"],
            ),
            Precedent(
                id="PREC-2017-EQUIFAX",
                title="2017 Equifax Data Breach",
                date="2017-09-07",
                category="cyber",
                summary="Massive data breach exposed personal information of 147 million people, resulting in billions in costs and leadership changes.",
                what_happened="Attackers exploited a known vulnerability in Apache Struts to access Equifax systems. The breach went undetected for 76 days.",
                impact={
                    "financial": "$1.4 billion in direct costs, $700M settlement",
                    "records_exposed": 147000000,
                    "stock_drop": "35% in first week",
                    "leadership": "CEO, CIO, and CSO resigned",
                },
                response_actions=[
                    "Engaged forensic investigators immediately",
                    "Set up dedicated breach response website",
                    "Offered free credit monitoring to affected individuals",
                    "Cooperated with regulatory investigations",
                ],
                outcome="Company paid $700M settlement. Industry-wide focus on patch management increased. New regulations proposed.",
                lessons_learned=[
                    "Patch known vulnerabilities immediately",
                    "Implement effective security monitoring",
                    "Have incident response plan ready before breach",
                    "Executive accountability for security is critical",
                    "Communication speed matters - delays increase reputational damage",
                ],
                keywords=["data breach", "cyber", "security", "vulnerability", "regulatory", "personal data"],
            ),
            Precedent(
                id="PREC-2021-SUEZ",
                title="2021 Suez Canal Blockage",
                date="2021-03-23",
                category="supply_chain",
                summary="Container ship Ever Given blocked the Suez Canal for 6 days, disrupting global shipping and highlighting supply chain fragility.",
                what_happened="The Ever Given, one of the largest container ships, ran aground in the Suez Canal, blocking all traffic through a route handling 12% of global trade.",
                impact={
                    "financial": "$9.6 billion per day in blocked trade",
                    "duration": "6 days of blockage, weeks of delays",
                    "ships_delayed": 400,
                    "affected_industries": ["retail", "energy", "manufacturing"],
                },
                response_actions=[
                    "Tugboats and dredging operations deployed",
                    "Some ships rerouted around Cape of Good Hope",
                    "Ports prepared for surge of delayed cargo",
                    "Companies activated air freight for critical items",
                ],
                outcome="Canal cleared after 6 days. Highlighted need for supply chain diversification and contingency planning.",
                lessons_learned=[
                    "Single points of failure in logistics can have global impact",
                    "Maintain visibility into shipping routes and alternatives",
                    "Buffer inventory for critical items",
                    "Have contingency shipping arrangements ready",
                ],
                keywords=["suez", "shipping", "logistics", "supply chain", "blockage", "container"],
            ),
            Precedent(
                id="PREC-2020-SOLARWINDS",
                title="2020 SolarWinds Supply Chain Attack",
                date="2020-12-13",
                category="cyber",
                summary="Sophisticated supply chain attack compromised SolarWinds software updates, affecting 18,000+ organizations including government agencies.",
                what_happened="Attackers inserted malicious code into SolarWinds Orion software builds, which was then distributed to customers through legitimate update channels.",
                impact={
                    "organizations_affected": 18000,
                    "government_agencies": "Treasury, Commerce, DHS, and more",
                    "detection_time": "9 months undetected",
                    "remediation_cost": "Billions across affected organizations",
                },
                response_actions=[
                    "Immediate isolation of affected systems",
                    "Comprehensive threat hunting across networks",
                    "Rebuilt systems from known-good sources",
                    "Enhanced monitoring for lateral movement",
                ],
                outcome="Led to major changes in software supply chain security practices and government cybersecurity requirements.",
                lessons_learned=[
                    "Supply chain attacks can bypass perimeter security",
                    "Verify integrity of software updates",
                    "Implement zero-trust architecture",
                    "Enhance monitoring for unusual activity",
                    "Third-party risk management is critical",
                ],
                keywords=["solarwinds", "supply chain attack", "apt", "cyber", "government", "update"],
            ),
        ]
        
        for precedent in demo_precedents:
            self.precedents[precedent.id] = precedent
        
        print(f"📚 Historian loaded {len(self.precedents)} precedents.")
    
    def _calculate_relevance(self, precedent: Precedent, query_keywords: List[str],
                             query_category: Optional[str] = None) -> float:
        """Calculate relevance score for a precedent."""
        score = 0.0
        
        # Category match (high weight)
        if query_category and precedent.category == query_category:
            score += 0.4
        
        # Keyword matching
        precedent_text = " ".join([
            precedent.title.lower(),
            precedent.summary.lower(),
            " ".join(precedent.keywords),
        ])
        
        matched_keywords = 0
        for keyword in query_keywords:
            if keyword.lower() in precedent_text:
                matched_keywords += 1
        
        if query_keywords:
            keyword_score = matched_keywords / len(query_keywords)
            score += keyword_score * 0.6
        
        return min(1.0, score)
    
    def research(self, query: str, category: Optional[str] = None,
                 max_results: int = 5) -> List[Precedent]:
        """
        Research historical precedents relevant to a query.
        
        Args:
            query: Search query or situation description.
            category: Optional category filter.
            max_results: Maximum number of results to return.
        
        Returns:
            List of relevant precedents sorted by relevance.
        """
        print(f"📚 Historian researching: '{query[:50]}...'")
        
        # Extract keywords from query
        query_keywords = query.lower().split()
        
        # Filter common words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "is", "are", "was", "were"}
        query_keywords = [w for w in query_keywords if w not in stop_words and len(w) > 2]
        
        # Score all precedents
        scored_precedents = []
        for precedent in self.precedents.values():
            relevance = self._calculate_relevance(precedent, query_keywords, category)
            if relevance > 0.1:  # Minimum threshold
                precedent.relevance_score = relevance
                scored_precedents.append(precedent)
        
        # Sort by relevance
        scored_precedents.sort(key=lambda p: p.relevance_score, reverse=True)
        
        results = scored_precedents[:max_results]
        print(f"✅ Historian found {len(results)} relevant precedents.")
        
        return results
    
    def create_post_mortem(self, incident_id: str, title: str,
                           timeline: List[Dict[str, str]],
                           root_cause: str,
                           what_went_well: List[str],
                           what_went_wrong: List[str],
                           action_items: List[Dict[str, Any]]) -> PostMortem:
        """
        Create a post-mortem analysis.
        
        Args:
            incident_id: ID of the incident being analyzed.
            title: Title of the post-mortem.
            timeline: List of timeline events.
            root_cause: Root cause analysis.
            what_went_well: Things that went well.
            what_went_wrong: Things that went wrong.
            action_items: Follow-up action items.
        
        Returns:
            Created PostMortem object.
        """
        print(f"📚 Historian creating post-mortem for: {incident_id}")
        
        # Generate lessons learned from what went wrong
        lessons = []
        for item in what_went_wrong:
            # Simple transformation - in production this could be AI-enhanced
            lesson = f"Ensure systems/processes prevent: {item}"
            lessons.append(lesson)
        
        # Generate recommendations
        recommendations = []
        for action in action_items:
            if action.get("priority") in ["high", "critical"]:
                recommendations.append(f"[PRIORITY] {action.get('action', 'TBD')}")
            else:
                recommendations.append(action.get("action", "TBD"))
        
        pm_id = f"PM-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        post_mortem = PostMortem(
            id=pm_id,
            incident_id=incident_id,
            date=datetime.now().strftime("%Y-%m-%d"),
            title=title,
            timeline=timeline,
            root_cause=root_cause,
            contributing_factors=[item for item in what_went_wrong[:3]],
            what_went_well=what_went_well,
            what_went_wrong=what_went_wrong,
            action_items=action_items,
            lessons_learned=lessons,
            recommendations=recommendations,
        )
        
        self.post_mortems[pm_id] = post_mortem
        
        # Also create a precedent from this for future reference
        self._create_precedent_from_post_mortem(post_mortem)
        
        print(f"✅ Historian created post-mortem: {pm_id}")
        return post_mortem
    
    def _create_precedent_from_post_mortem(self, pm: PostMortem):
        """Create a precedent entry from a post-mortem."""
        # Generate a precedent ID
        hash_input = f"{pm.incident_id}{pm.date}"
        short_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        prec_id = f"PREC-{datetime.now().year}-{short_hash.upper()}"
        
        precedent = Precedent(
            id=prec_id,
            title=pm.title,
            date=pm.date,
            category="internal_incident",
            summary=pm.root_cause[:200],
            what_happened=pm.root_cause,
            impact={"timeline_events": len(pm.timeline)},
            response_actions=[a.get("action", "") for a in pm.action_items[:5]],
            outcome="See post-mortem for details",
            lessons_learned=pm.lessons_learned,
            keywords=pm.title.lower().split()[:10],
        )
        
        self.precedents[prec_id] = precedent
    
    def get_lessons_for_situation(self, situation_summary: str,
                                   category: Optional[str] = None) -> List[str]:
        """
        Get aggregated lessons learned relevant to a situation.
        
        Args:
            situation_summary: Description of the current situation.
            category: Optional category filter.
        
        Returns:
            List of relevant lessons learned.
        """
        precedents = self.research(situation_summary, category, max_results=3)
        
        lessons = []
        for prec in precedents:
            for lesson in prec.lessons_learned:
                if lesson not in lessons:
                    lessons.append(lesson)
        
        return lessons[:10]  # Top 10 unique lessons
    
    def get_precedent_report(self, precedent: Precedent) -> str:
        """Generate a human-readable precedent report."""
        lines = [
            f"📚 HISTORICAL PRECEDENT",
            f"{'=' * 50}",
            f"ID: {precedent.id}",
            f"Title: {precedent.title}",
            f"Date: {precedent.date}",
            f"Category: {precedent.category}",
            f"Relevance: {precedent.relevance_score:.0%}",
            f"",
            f"📋 SUMMARY:",
            f"{precedent.summary}",
            f"",
            f"❓ WHAT HAPPENED:",
            f"{precedent.what_happened}",
            f"",
            f"📊 IMPACT:",
        ]
        
        for key, value in precedent.impact.items():
            lines.append(f"  • {key}: {value}")
        
        lines.append(f"\n🔧 RESPONSE ACTIONS:")
        for action in precedent.response_actions:
            lines.append(f"  • {action}")
        
        lines.append(f"\n📈 OUTCOME:")
        lines.append(f"{precedent.outcome}")
        
        lines.append(f"\n💡 LESSONS LEARNED:")
        for lesson in precedent.lessons_learned:
            lines.append(f"  ★ {lesson}")
        
        return "\n".join(lines)
    
    def get_post_mortem_report(self, pm: PostMortem) -> str:
        """Generate a human-readable post-mortem report."""
        lines = [
            f"📋 POST-MORTEM REPORT",
            f"{'=' * 50}",
            f"ID: {pm.id}",
            f"Incident: {pm.incident_id}",
            f"Date: {pm.date}",
            f"Title: {pm.title}",
            f"",
            f"🕐 TIMELINE:",
        ]
        
        for event in pm.timeline:
            lines.append(f"  {event.get('time', 'N/A')} - {event.get('event', 'N/A')}")
        
        lines.append(f"\n🔍 ROOT CAUSE:")
        lines.append(f"{pm.root_cause}")
        
        lines.append(f"\n✅ WHAT WENT WELL:")
        for item in pm.what_went_well:
            lines.append(f"  + {item}")
        
        lines.append(f"\n❌ WHAT WENT WRONG:")
        for item in pm.what_went_wrong:
            lines.append(f"  - {item}")
        
        lines.append(f"\n📝 ACTION ITEMS:")
        for action in pm.action_items:
            priority = action.get("priority", "medium").upper()
            owner = action.get("owner", "TBD")
            lines.append(f"  [{priority}] {action.get('action', 'TBD')} (Owner: {owner})")
        
        lines.append(f"\n💡 LESSONS LEARNED:")
        for lesson in pm.lessons_learned:
            lines.append(f"  ★ {lesson}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test the Historian
    historian = Historian()
    
    # Research precedents
    results = historian.research(
        "semiconductor supply chain disruption manufacturing",
        category="supply_chain"
    )
    
    print("\n--- RESEARCH RESULTS ---")
    for prec in results:
        print(f"\n{historian.get_precedent_report(prec)[:500]}...")
    
    # Create a post-mortem
    pm = historian.create_post_mortem(
        incident_id="INC-2024-001",
        title="Q4 Supplier Disruption Incident",
        timeline=[
            {"time": "2024-01-15 09:00", "event": "Supplier announced production halt"},
            {"time": "2024-01-15 10:30", "event": "Operations team notified"},
            {"time": "2024-01-15 14:00", "event": "Emergency response team convened"},
            {"time": "2024-01-16 09:00", "event": "Alternative supplier identified"},
        ],
        root_cause="Single-source dependency on critical component supplier with no backup",
        what_went_well=[
            "Fast internal communication",
            "Clear escalation path followed",
            "Alternative supplier found within 24 hours",
        ],
        what_went_wrong=[
            "No backup supplier pre-qualified",
            "Inventory buffer was below target levels",
            "Supplier risk assessment had not been updated",
        ],
        action_items=[
            {"action": "Qualify secondary supplier for all critical components", "priority": "high", "owner": "Procurement"},
            {"action": "Increase safety stock to 30 days", "priority": "high", "owner": "Operations"},
            {"action": "Implement quarterly supplier risk reviews", "priority": "medium", "owner": "Risk Management"},
        ]
    )
    
    print("\n--- POST-MORTEM ---")
    print(historian.get_post_mortem_report(pm))
