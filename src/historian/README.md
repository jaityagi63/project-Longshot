# Historian 📚

**Domain:** Wisdom  
**Description:** Retrieves precedents and stores post-mortem lessons.

## Overview

The Historian module manages organizational memory. It retrieves relevant historical precedents and stores lessons learned from post-mortem analyses for future reference.

## Features

- **Precedent Research**: Finds similar past events
- **Relevance Scoring**: Ranks precedents by applicability
- **Post-Mortem Creation**: Structures incident analysis
- **Lesson Extraction**: Distills actionable insights
- **Category Filtering**: Filters by incident type
- **Knowledge Persistence**: Builds organizational wisdom

## Pre-loaded Precedents

The module comes with notable case studies:
- 2011 Thailand Floods (supply chain)
- 2017 Equifax Data Breach (cybersecurity)
- 2021 Suez Canal Blockage (logistics)
- 2020 SolarWinds Attack (supply chain attack)

## Usage

### Researching Precedents

```python
from src.historian import Historian

historian = Historian()

# Search for relevant precedents
precedents = historian.research(
    query="semiconductor supply chain disruption",
    category="supply_chain",
    max_results=3
)

for prec in precedents:
    print(f"Title: {prec.title}")
    print(f"Relevance: {prec.relevance_score:.0%}")
    print(f"Lessons: {prec.lessons_learned}")
```

### Creating Post-Mortems

```python
pm = historian.create_post_mortem(
    incident_id="INC-2024-001",
    title="Q1 Supplier Disruption",
    timeline=[
        {"time": "09:00", "event": "Supplier halt announced"},
        {"time": "10:30", "event": "Operations notified"},
    ],
    root_cause="Single-source dependency",
    what_went_well=["Fast escalation", "Clear communication"],
    what_went_wrong=["No backup supplier", "Low inventory"],
    action_items=[
        {"action": "Qualify backup supplier", "priority": "high", "owner": "Procurement"},
    ]
)

print(historian.get_post_mortem_report(pm))
```

## Precedent Structure

Each `Precedent` contains:
- `id`: Unique identifier
- `title`: Event name
- `date`: When it occurred
- `category`: Type of incident
- `summary`: Brief overview
- `what_happened`: Detailed description
- `impact`: Financial and operational metrics
- `response_actions`: Actions taken
- `outcome`: Final result
- `lessons_learned`: Key takeaways
- `keywords`: Search terms

## Configuration

- `HISTORIAN_MAX_PRECEDENTS`: Maximum precedents to return (default: 10)
