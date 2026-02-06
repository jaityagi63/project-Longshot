# Connector 🔗

**Domain:** Relevance  
**Description:** Maps external events to internal assets and stakeholders.

## Overview

The Connector module determines organizational relevance by mapping external events to internal assets, stakeholders, and dependencies. It identifies cascade effects through dependency analysis.

## Features

- **Asset Registry**: Maintains a database of organizational assets
- **Keyword Indexing**: Fast lookup of assets by keywords
- **Cascade Detection**: Identifies dependent assets affected by primary impacts
- **Impact Assessment**: Calculates impact scores based on risk profiles
- **Stakeholder Mapping**: Links affected assets to responsible stakeholders

## Asset Categories

- `supplier` - External suppliers and vendors
- `product` - Products and services
- `facility` - Physical locations and plants
- `contract` - Legal agreements
- `personnel` - Key personnel
- `system` - IT systems and infrastructure

## Usage

```python
from src.connector import Connector, Asset

connector = Connector()

# Register a custom asset
asset = Asset(
    id="SUP-NEW",
    name="New Supplier",
    category="supplier",
    metadata={"country": "Germany", "products": ["components"]},
    dependencies=[],
    stakeholders=["procurement@company.com"],
    risk_score=0.5
)
connector.register_asset(asset)

# Map an event
event = {
    "title": "Germany manufacturing delays",
    "snippet": "Component shortages reported...",
    "link": "https://example.com",
    "timestamp": "2024-01-15T10:00:00"
}

mapping = connector.connect(event)
print(f"Affected assets: {mapping.affected_assets}")
print(f"Stakeholders: {connector.get_stakeholders(mapping.affected_assets)}")
```

## Output

The `EventMapping` contains:
- `event_id`: Unique identifier for the event
- `event_summary`: Brief description
- `affected_assets`: List of impacted asset IDs
- `impact_assessment`: Dictionary of asset_id -> impact_score (0-1)
- `keywords_matched`: Keywords that triggered the mapping

## Configuration

Assets can be loaded from a JSON file:

```json
{
  "assets": [
    {
      "id": "SUP-001",
      "name": "Supplier Name",
      "category": "supplier",
      "metadata": {},
      "dependencies": [],
      "stakeholders": ["email@company.com"],
      "risk_score": 0.5
    }
  ]
}
```
