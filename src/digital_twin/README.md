# Digital Twin 🌍

**Domain:** Visualization  
**Description:** Renders impacts on a 3D interactive globe.

## Overview

The Digital Twin module creates visual representations of global impacts. It generates interactive HTML visualizations showing affected locations, connections, and severity levels.

## Features

- **Global Visualization**: 3D globe with impact markers
- **Location Database**: Pre-defined major business locations
- **Impact Markers**: Severity-coded points on the globe
- **Connection Lines**: Supply chain and communication routes
- **Snapshots**: Capture and save visualization states
- **HTML Export**: Self-contained interactive output

## Pre-defined Locations

### Manufacturing Hubs
- Taiwan (Hsinchu, Taipei)
- South Korea (Seoul, Suwon)
- China (Shenzhen, Shanghai)
- Japan (Tokyo, Osaka)
- Germany (Munich), Netherlands (Eindhoven)
- USA (Austin, Portland, San Jose, Phoenix)

### Logistics Points
- Singapore, Rotterdam, Los Angeles Port
- Suez Canal, Panama Canal

## Usage

```python
from src.digital_twin import DigitalTwin

dt = DigitalTwin()

# Add impact markers
dt.add_impact_marker(
    location_key="taiwan_hsinchu",
    impact_type="supply_chain",
    severity="critical",
    label="TSMC Disruption",
    description="Production halt",
    data={"estimated_impact": "$500M"}
)

dt.add_impact_marker(
    location_key="usa_austin",
    impact_type="facility",
    severity="medium",
    label="Assembly Delayed",
    description="Downstream impact"
)

# Add connections
dt.add_connection(
    source_key="taiwan_hsinchu",
    target_key="usa_austin",
    connection_type="supply",
    status="disrupted",
    label="Chip Supply Route"
)

# Create snapshot and save
snapshot = dt.create_snapshot("Supply Chain Crisis")
dt.save_visualization("crisis_view.html", snapshot)
```

## Severity Colors

- `low`: Green (#4CAF50)
- `medium`: Amber (#FFC107)
- `high`: Orange (#FF9800)
- `critical`: Red (#F44336)

## Connection Statuses

- `active`: Normal operation (Blue)
- `disrupted`: Connection broken (Red)
- `rerouted`: Alternative path (Purple)

## Output

The generated HTML includes:
- Interactive globe visualization
- Color-coded impact markers
- Animated connection lines
- Legend and statistics
- Marker detail list

## Adding Custom Locations

```python
from src.digital_twin import GeoLocation

dt.locations["custom_location"] = GeoLocation(
    latitude=40.7128,
    longitude=-74.0060,
    name="Custom Location",
    country="Country"
)
```
