# Council 👥

**Domain:** Strategy  
**Description:** Multi-agent debate system (Ops, Legal, Finance, PR).

## Overview

The Council module simulates a multi-perspective strategic debate. It models different organizational viewpoints to reach balanced decisions during crises.

## Features

- **Multiple Perspectives**: Operations, Legal, Finance, PR viewpoints
- **Structured Debate**: Multi-round deliberation process
- **Priority Assessment**: Each perspective assigns urgency levels
- **Consensus Building**: Aggregates viewpoints into actionable decisions
- **Risk Aggregation**: Compiles risks from all perspectives

## Council Members

### Operations (🔧)
- Focus: Business continuity, service delivery
- Priorities: Uptime, capacity, contingencies
- Style: Action-oriented, immediate solutions

### Legal (⚖️)
- Focus: Compliance, liability, contracts
- Priorities: Regulatory requirements, documentation
- Style: Risk-averse, process-driven

### Finance (💰)
- Focus: Costs, budgets, financial exposure
- Priorities: ROI, reserves, insurance
- Style: Quantitative, impact-focused

### Public Relations (📢)
- Focus: Reputation, stakeholder perception
- Priorities: Communication, transparency
- Style: Proactive, relationship-focused

## Usage

```python
from src.council import Council

council = Council(debate_rounds=3)

situation = {
    "summary": "Major supplier bankruptcy",
    "severity": "high",
    "affected_assets": ["SUP-001"],
    "financial_impact": 2500000,
    "threat_type": "supplier_disruption",
    "regulatory_exposure": False,
    "media_exposure": "medium",
    "customer_impact": True,
}

result = council.convene(situation)

print(f"Decision: {result.consensus.decision}")
print(f"Confidence: {result.consensus.confidence:.0%}")
print(f"Timeline: {result.consensus.timeline}")

for item in result.consensus.action_items:
    print(f"  [{item['priority']}] {item['owner']}: {item['action']}")
```

## Output

The `DebateResult` contains:
- `session_id`: Unique debate session ID
- `arguments`: List of arguments from each member
- `consensus`: Final decision with confidence and action items
- `debate_rounds`: Number of rounds conducted
- `summary`: Narrative summary of the debate

## Configuration

- `COUNCIL_DEBATE_ROUNDS`: Number of debate rounds (default: 3)
