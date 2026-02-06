# Seer 🔮

**Domain:** Prediction  
**Description:** Simulates the Domino Effect chain reaction of events.

## Overview

The Seer module predicts cascading impacts of events through scenario simulation. It models the "domino effect" to forecast financial, operational, and reputational consequences.

## Features

- **Scenario Classification**: Automatically classifies events into scenario types
- **Chain Reaction Modeling**: Simulates cascading effects over time
- **Multi-Category Impact**: Tracks financial, operational, reputational, regulatory, and strategic impacts
- **Probability Weighting**: Adjusts predictions based on initial impact severity
- **Mitigation Suggestions**: Generates actionable mitigation recommendations

## Scenario Types

- `supplier_disruption` - Supply chain and vendor issues
- `cybersecurity_incident` - Data breaches and security events
- `geopolitical_event` - Sanctions, tariffs, political changes
- `default` - General operational disruptions

## Impact Categories

- **Financial**: Direct and indirect monetary impacts
- **Operational**: Production, logistics, service delivery
- **Reputational**: Brand, customer trust, public perception
- **Regulatory**: Compliance, fines, legal exposure
- **Strategic**: Long-term market position, competitive disadvantage

## Usage

```python
from src.seer import Seer

seer = Seer(simulation_depth=5)

result = seer.prophesy(
    event_summary="Major supplier declares bankruptcy",
    affected_assets=["SUP-001", "PROD-001"],
    impact_scores={"SUP-001": 0.85, "PROD-001": 0.6}
)

print(f"Peak Severity: {result.peak_severity.name}")
print(f"Financial Impact: ${result.total_financial_impact:,.0f}")
print(f"Time to Peak: {result.time_to_peak}")

for effect in result.chain:
    print(f"  → {effect.description} ({effect.severity.name})")
```

## Output

The `SimulationResult` contains:
- `scenario_id`: Unique simulation identifier
- `chain`: List of predicted DominoEffect events
- `total_financial_impact`: Aggregated financial exposure
- `peak_severity`: Maximum severity level reached
- `time_to_peak`: Time until worst impact
- `confidence_score`: Simulation confidence (0-1)
- `recommendations`: Suggested actions

## Configuration

- `SEER_SIMULATION_DEPTH`: Maximum chain length (default: 5)
