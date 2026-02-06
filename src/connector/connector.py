"""
Connector Module - Relevance Mapping
=====================================
Maps external events to internal assets and stakeholders.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict


@dataclass
class Asset:
    """Represents an internal organizational asset."""
    id: str
    name: str
    category: str  # supplier, product, facility, contract, personnel, system
    metadata: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)  # IDs of other assets
    stakeholders: List[str] = field(default_factory=list)
    risk_score: float = 0.0


@dataclass
class EventMapping:
    """Mapping between an external event and internal assets."""
    event_id: str
    event_summary: str
    timestamp: str
    affected_assets: List[str]
    impact_assessment: Dict[str, float]  # asset_id -> impact_score (0-1)
    keywords_matched: List[str]


class Connector:
    """
    The Connector module: Relevance.
    Maps external events to internal assets and determines organizational impact.
    """

    def __init__(self, assets_path: Optional[Path] = None):
        """
        Initialize the Connector.
        
        Args:
            assets_path: Path to JSON file containing asset definitions.
        """
        self.assets: Dict[str, Asset] = {}
        self.keyword_index: Dict[str, List[str]] = {}  # keyword -> list of asset IDs
        self.mappings: List[EventMapping] = []
        
        if assets_path and assets_path.exists():
            self.load_assets(assets_path)
        else:
            self._load_demo_assets()
    
    def _load_demo_assets(self):
        """Load demonstration assets for testing."""
        demo_assets = [
            Asset(
                id="SUP-001",
                name="Acme Semiconductors",
                category="supplier",
                metadata={"country": "Taiwan", "products": ["chips", "processors"]},
                dependencies=[],
                stakeholders=["procurement@company.com", "ops-lead@company.com"],
                risk_score=0.7
            ),
            Asset(
                id="SUP-002",
                name="GlobalChip Industries",
                category="supplier",
                metadata={"country": "South Korea", "products": ["memory", "storage"]},
                dependencies=[],
                stakeholders=["procurement@company.com"],
                risk_score=0.5
            ),
            Asset(
                id="PROD-001",
                name="SmartWidget Pro",
                category="product",
                metadata={"sku": "SW-PRO-2024", "margin": 0.35},
                dependencies=["SUP-001", "SUP-002"],
                stakeholders=["product-manager@company.com", "sales@company.com"],
                risk_score=0.6
            ),
            Asset(
                id="FAC-001",
                name="Austin Manufacturing Plant",
                category="facility",
                metadata={"location": "Austin, TX", "capacity": 10000},
                dependencies=["SUP-001"],
                stakeholders=["plant-manager@company.com", "ops@company.com"],
                risk_score=0.4
            ),
            Asset(
                id="SYS-001",
                name="Cloud Infrastructure (AWS)",
                category="system",
                metadata={"provider": "AWS", "region": "us-east-1"},
                dependencies=[],
                stakeholders=["it-ops@company.com", "security@company.com"],
                risk_score=0.8
            ),
            Asset(
                id="CON-001",
                name="Government Contract #2024-DEF",
                category="contract",
                metadata={"value": 5000000, "expires": "2025-12-31"},
                dependencies=["PROD-001", "FAC-001"],
                stakeholders=["legal@company.com", "cfo@company.com"],
                risk_score=0.9
            ),
        ]
        
        for asset in demo_assets:
            self.register_asset(asset)
        
        print(f"🔗 Connector loaded {len(self.assets)} demo assets.")
    
    def load_assets(self, path: Path):
        """Load assets from a JSON file."""
        with open(path, 'r') as f:
            data = json.load(f)
        
        for asset_data in data.get("assets", []):
            asset = Asset(**asset_data)
            self.register_asset(asset)
        
        print(f"🔗 Connector loaded {len(self.assets)} assets from {path}")
    
    def register_asset(self, asset: Asset):
        """Register an asset and index its keywords."""
        self.assets[asset.id] = asset
        
        # Index keywords for fast lookup
        keywords = self._extract_keywords(asset)
        for keyword in keywords:
            keyword_lower = keyword.lower()
            if keyword_lower not in self.keyword_index:
                self.keyword_index[keyword_lower] = []
            self.keyword_index[keyword_lower].append(asset.id)
    
    def _extract_keywords(self, asset: Asset) -> List[str]:
        """Extract searchable keywords from an asset."""
        keywords = [asset.name, asset.category, asset.id]
        
        # Add metadata values as keywords
        for key, value in asset.metadata.items():
            if isinstance(value, str):
                keywords.append(value)
            elif isinstance(value, list):
                keywords.extend([str(v) for v in value])
        
        return keywords
    
    def connect(self, event_data: Dict[str, Any]) -> EventMapping:
        """
        Connect an external event to internal assets.
        
        Args:
            event_data: Dictionary containing event information with keys:
                - title: Event title
                - snippet: Event description
                - link: Source URL
                - timestamp: When the event was detected
        
        Returns:
            EventMapping object with affected assets and impact assessment.
        """
        print(f"🔗 Connector analyzing event: '{event_data.get('title', 'Unknown')[:50]}...'")
        
        # Extract text to analyze
        text_to_analyze = " ".join([
            event_data.get("title", ""),
            event_data.get("snippet", ""),
        ]).lower()
        
        # Find matching assets
        affected_assets = []
        keywords_matched = []
        
        for keyword, asset_ids in self.keyword_index.items():
            if keyword in text_to_analyze:
                keywords_matched.append(keyword)
                affected_assets.extend(asset_ids)
        
        # Remove duplicates while preserving order
        affected_assets = list(dict.fromkeys(affected_assets))
        
        # Also include dependent assets (cascade effect)
        cascaded_assets = self._find_dependent_assets(affected_assets)
        all_affected = list(dict.fromkeys(affected_assets + cascaded_assets))
        
        # Calculate impact scores
        impact_assessment = {}
        for asset_id in all_affected:
            asset = self.assets.get(asset_id)
            if asset:
                # Simple impact calculation based on risk score and keyword matches
                base_impact = asset.risk_score
                keyword_boost = min(0.3, len([k for k in keywords_matched if k in self._extract_keywords(asset)]) * 0.1)
                cascade_penalty = 0.1 if asset_id in cascaded_assets else 0
                
                impact_assessment[asset_id] = min(1.0, base_impact + keyword_boost - cascade_penalty)
        
        # Create mapping
        mapping = EventMapping(
            event_id=f"EVT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            event_summary=event_data.get("title", "Unknown Event"),
            timestamp=datetime.now().isoformat(),
            affected_assets=all_affected,
            impact_assessment=impact_assessment,
            keywords_matched=keywords_matched
        )
        
        self.mappings.append(mapping)
        
        print(f"✅ Connector identified {len(all_affected)} affected assets.")
        return mapping
    
    def _find_dependent_assets(self, asset_ids: List[str]) -> List[str]:
        """Find assets that depend on the given assets."""
        dependents = []
        
        for asset_id, asset in self.assets.items():
            if asset_id not in asset_ids:
                for dependency in asset.dependencies:
                    if dependency in asset_ids:
                        dependents.append(asset_id)
                        break
        
        return dependents
    
    def get_asset(self, asset_id: str) -> Optional[Asset]:
        """Get an asset by ID."""
        return self.assets.get(asset_id)
    
    def get_stakeholders(self, asset_ids: List[str]) -> List[str]:
        """Get unique stakeholders for a list of assets."""
        stakeholders = []
        for asset_id in asset_ids:
            asset = self.assets.get(asset_id)
            if asset:
                stakeholders.extend(asset.stakeholders)
        return list(set(stakeholders))
    
    def export_mapping(self, mapping: EventMapping) -> Dict[str, Any]:
        """Export a mapping to a dictionary."""
        return asdict(mapping)


if __name__ == "__main__":
    # Test the Connector
    connector = Connector()
    
    # Simulate an external event
    test_event = {
        "title": "Taiwan semiconductor industry faces supply disruptions",
        "snippet": "Major chip manufacturers in Taiwan report production delays due to power grid issues. This could affect global electronics supply chains.",
        "link": "https://example.com/news/1",
        "timestamp": datetime.now().isoformat()
    }
    
    mapping = connector.connect(test_event)
    
    print("\n--- CONNECTOR REPORT ---")
    print(f"Event: {mapping.event_summary}")
    print(f"Affected Assets: {mapping.affected_assets}")
    print(f"Keywords Matched: {mapping.keywords_matched}")
    print(f"Impact Assessment:")
    for asset_id, impact in mapping.impact_assessment.items():
        asset = connector.get_asset(asset_id)
        print(f"  - {asset.name}: {impact:.2%} impact")
    
    stakeholders = connector.get_stakeholders(mapping.affected_assets)
    print(f"\nStakeholders to notify: {stakeholders}")
