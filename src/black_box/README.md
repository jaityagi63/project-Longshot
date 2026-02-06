# Black Box 📦

**Domain:** Hindsight  
**Description:** Re-runs simulations to find what could have been done better.

## Overview

The Black Box module performs post-incident analysis by simulating alternative decisions. It identifies what could have been done differently and quantifies potential improvements.

## Features

- **Alternative Scenario Generation**: Models different decision paths
- **Decision Point Analysis**: Examines each critical juncture
- **Improvement Quantification**: Estimates time and cost savings
- **Feasibility Assessment**: Rates practicality of alternatives
- **Optimal Path Identification**: Recommends best response path
- **Actionable Insights**: Generates improvement recommendations

## Decision Points Analyzed

- `detection` - How/when was the issue identified?
- `escalation` - How was it escalated?
- `response_selection` - What response was chosen?
- `resource_allocation` - How were resources deployed?
- `communication` - How were stakeholders informed?
- `mitigation` - What mitigation was applied?

## Usage

```python
from src.black_box import BlackBox

bb = BlackBox()

incident = {
    "incident_id": "INC-2024-001",
    "summary": "Supplier disruption",
    "duration_hours": 72,
    "financial_impact": 2500000,
    "severity": "high",
    "decisions_made": {
        "detection": "Reactive - learned from news",
        "escalation": "Escalated after 2 hours",
        "response_selection": "Standard protocol",
    },
}

analysis = bb.analyze(incident)

print(f"Potential Savings: ${analysis.potential_savings:,.0f}")
print(f"Time Savings: {analysis.time_savings}")

print("\nOptimal Path:")
for step in analysis.optimal_path:
    print(f"  → {step}")

print("\nTop Recommendations:")
for rec in analysis.recommendations:
    print(f"  • {rec}")
```

## Output

The `HindsightAnalysis` contains:
- `analysis_id`: Unique analysis identifier
- `original_outcome`: Actual results
- `alternatives`: List of simulated alternatives
- `optimal_path`: Recommended decision sequence
- `potential_savings`: Estimated cost reduction
- `time_savings`: Estimated time reduction
- `key_insights`: Important observations
- `recommendations`: Action items for improvement

## Alternative Scoring

Each alternative is scored on:
- **Improvement Potential** (-1 to 1): Expected outcome improvement
- **Feasibility** (0 to 1): How practical to implement
- **Weighted Score**: Combined metric for prioritization
