"""
Digital Twin Module - 3D Visualization
=======================================
Renders impacts on a 3D interactive globe.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class GeoLocation:
    """A geographic location."""
    latitude: float
    longitude: float
    name: str
    country: str = ""


@dataclass
class ImpactMarker:
    """A marker showing impact on the globe."""
    id: str
    location: GeoLocation
    impact_type: str  # supply_chain, facility, market, partner, event
    severity: str  # low, medium, high, critical
    label: str
    description: str
    radius: float  # Visual radius on globe
    color: str
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConnectionLine:
    """A connection line between two points."""
    id: str
    source: GeoLocation
    target: GeoLocation
    connection_type: str  # supply, distribution, communication
    status: str  # active, disrupted, rerouted
    label: str
    color: str
    animated: bool = True


@dataclass
class GlobeSnapshot:
    """A snapshot of the globe visualization."""
    id: str
    timestamp: str
    title: str
    markers: List[ImpactMarker]
    connections: List[ConnectionLine]
    center_location: Optional[GeoLocation]
    zoom_level: float
    annotations: List[Dict[str, Any]]


class DigitalTwin:
    """
    The Digital Twin module: Visualization.
    Renders impacts on a 3D interactive globe.
    """

    def __init__(self, output_path: Optional[Path] = None):
        """
        Initialize the Digital Twin.
        
        Args:
            output_path: Path to save visualization outputs.
        """
        self.output_path = output_path or Path("data/visualizations")
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        self.markers: List[ImpactMarker] = []
        self.connections: List[ConnectionLine] = []
        self.snapshots: List[GlobeSnapshot] = []
        
        # Pre-defined locations database
        self.locations = self._load_locations()
        
        # Color schemes
        self.severity_colors = {
            "low": "#4CAF50",      # Green
            "medium": "#FFC107",   # Amber
            "high": "#FF9800",     # Orange
            "critical": "#F44336", # Red
        }
        
        self.connection_colors = {
            "active": "#2196F3",     # Blue
            "disrupted": "#F44336",  # Red
            "rerouted": "#9C27B0",   # Purple
        }
    
    def _load_locations(self) -> Dict[str, GeoLocation]:
        """Load predefined geographic locations."""
        return {
            # Major manufacturing hubs
            "taiwan_hsinchu": GeoLocation(24.8047, 120.9714, "Hsinchu Science Park", "Taiwan"),
            "taiwan_taipei": GeoLocation(25.0330, 121.5654, "Taipei", "Taiwan"),
            "korea_seoul": GeoLocation(37.5665, 126.9780, "Seoul", "South Korea"),
            "korea_suwon": GeoLocation(37.2636, 127.0286, "Suwon (Samsung)", "South Korea"),
            "china_shenzhen": GeoLocation(22.5431, 114.0579, "Shenzhen", "China"),
            "china_shanghai": GeoLocation(31.2304, 121.4737, "Shanghai", "China"),
            "japan_tokyo": GeoLocation(35.6762, 139.6503, "Tokyo", "Japan"),
            "japan_osaka": GeoLocation(34.6937, 135.5023, "Osaka", "Japan"),
            "vietnam_hanoi": GeoLocation(21.0285, 105.8542, "Hanoi", "Vietnam"),
            "india_bangalore": GeoLocation(12.9716, 77.5946, "Bangalore", "India"),
            "germany_munich": GeoLocation(48.1351, 11.5820, "Munich", "Germany"),
            "netherlands_eindhoven": GeoLocation(51.4416, 5.4697, "Eindhoven (ASML)", "Netherlands"),
            "usa_austin": GeoLocation(30.2672, -97.7431, "Austin, TX", "USA"),
            "usa_portland": GeoLocation(45.5152, -122.6784, "Portland, OR", "USA"),
            "usa_san_jose": GeoLocation(37.3382, -121.8863, "San Jose, CA", "USA"),
            "usa_phoenix": GeoLocation(33.4484, -112.0740, "Phoenix, AZ", "USA"),
            "usa_new_york": GeoLocation(40.7128, -74.0060, "New York, NY", "USA"),
            # Major ports and logistics
            "singapore": GeoLocation(1.3521, 103.8198, "Singapore", "Singapore"),
            "rotterdam": GeoLocation(51.9244, 4.4777, "Rotterdam", "Netherlands"),
            "la_port": GeoLocation(33.7405, -118.2600, "Port of Los Angeles", "USA"),
            "suez_canal": GeoLocation(30.4550, 32.3511, "Suez Canal", "Egypt"),
            "panama_canal": GeoLocation(9.0800, -79.6800, "Panama Canal", "Panama"),
        }
    
    def add_impact_marker(self, location_key: str, impact_type: str,
                           severity: str, label: str, description: str,
                           data: Optional[Dict[str, Any]] = None) -> ImpactMarker:
        """
        Add an impact marker to the globe.
        
        Args:
            location_key: Key from predefined locations or custom GeoLocation.
            impact_type: Type of impact.
            severity: Severity level.
            label: Short label for the marker.
            description: Detailed description.
            data: Additional data to attach to marker.
        
        Returns:
            Created ImpactMarker.
        """
        location = self.locations.get(location_key)
        if not location:
            print(f"⚠️ Location '{location_key}' not found, using default.")
            location = GeoLocation(0, 0, location_key, "Unknown")
        
        # Calculate radius based on severity
        radius_map = {"low": 50000, "medium": 100000, "high": 150000, "critical": 200000}
        
        marker = ImpactMarker(
            id=f"MRK-{datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]}",
            location=location,
            impact_type=impact_type,
            severity=severity,
            label=label,
            description=description,
            radius=radius_map.get(severity, 100000),
            color=self.severity_colors.get(severity, "#9E9E9E"),
            data=data or {},
        )
        
        self.markers.append(marker)
        print(f"🌍 Digital Twin: Added {severity} impact marker at {location.name}")
        return marker
    
    def add_connection(self, source_key: str, target_key: str,
                        connection_type: str, status: str,
                        label: str = "") -> ConnectionLine:
        """
        Add a connection line between two locations.
        
        Args:
            source_key: Source location key.
            target_key: Target location key.
            connection_type: Type of connection.
            status: Connection status.
            label: Optional label for the connection.
        
        Returns:
            Created ConnectionLine.
        """
        source = self.locations.get(source_key, GeoLocation(0, 0, source_key, ""))
        target = self.locations.get(target_key, GeoLocation(0, 0, target_key, ""))
        
        connection = ConnectionLine(
            id=f"CON-{datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]}",
            source=source,
            target=target,
            connection_type=connection_type,
            status=status,
            label=label or f"{source.name} → {target.name}",
            color=self.connection_colors.get(status, "#9E9E9E"),
            animated=status != "active",
        )
        
        self.connections.append(connection)
        print(f"🌍 Digital Twin: Added {status} connection: {source.name} → {target.name}")
        return connection
    
    def visualize_supply_chain_impact(self, affected_assets: List[Dict[str, Any]],
                                       severity: str) -> List[ImpactMarker]:
        """
        Visualize supply chain impacts on the globe.
        
        Args:
            affected_assets: List of affected assets with location info.
            severity: Overall severity level.
        
        Returns:
            List of created markers.
        """
        markers = []
        
        for asset in affected_assets:
            location_key = asset.get("location_key", "usa_austin")
            
            marker = self.add_impact_marker(
                location_key=location_key,
                impact_type="supply_chain",
                severity=asset.get("severity", severity),
                label=asset.get("name", "Affected Asset"),
                description=asset.get("description", "Supply chain disruption"),
                data=asset,
            )
            markers.append(marker)
        
        return markers
    
    def create_snapshot(self, title: str, 
                        center_key: Optional[str] = None,
                        zoom: float = 1.0) -> GlobeSnapshot:
        """
        Create a snapshot of the current globe state.
        
        Args:
            title: Title for the snapshot.
            center_key: Location key to center the view on.
            zoom: Zoom level (1.0 = default).
        
        Returns:
            Created GlobeSnapshot.
        """
        center = self.locations.get(center_key) if center_key else None
        
        snapshot = GlobeSnapshot(
            id=f"SNAP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            timestamp=datetime.now().isoformat(),
            title=title,
            markers=self.markers.copy(),
            connections=self.connections.copy(),
            center_location=center,
            zoom_level=zoom,
            annotations=[],
        )
        
        self.snapshots.append(snapshot)
        print(f"🌍 Digital Twin: Created snapshot '{title}'")
        return snapshot
    
    def generate_html_visualization(self, snapshot: Optional[GlobeSnapshot] = None) -> str:
        """
        Generate an HTML visualization of the globe.
        
        Args:
            snapshot: Snapshot to visualize. Uses current state if None.
        
        Returns:
            HTML string containing the visualization.
        """
        markers = snapshot.markers if snapshot else self.markers
        connections = snapshot.connections if snapshot else self.connections
        title = snapshot.title if snapshot else "Project Longshot - Digital Twin"
        
        # Convert markers to GeoJSON-like format for the visualization
        markers_data = []
        for m in markers:
            markers_data.append({
                "lat": m.location.latitude,
                "lng": m.location.longitude,
                "label": m.label,
                "description": m.description,
                "color": m.color,
                "radius": m.radius / 10000,  # Scale for display
                "severity": m.severity,
            })
        
        connections_data = []
        for c in connections:
            connections_data.append({
                "source": {"lat": c.source.latitude, "lng": c.source.longitude},
                "target": {"lat": c.target.latitude, "lng": c.target.longitude},
                "label": c.label,
                "color": c.color,
                "status": c.status,
                "animated": c.animated,
            })
        
        html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three-globe@2.24.0/dist/three-globe.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            min-height: 100vh;
        }}
        .header {{
            padding: 20px;
            text-align: center;
            background: rgba(0,0,0,0.3);
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        .header h1 {{
            font-size: 2rem;
            background: linear-gradient(90deg, #00d4ff, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        #globe-container {{
            width: 100%;
            height: 70vh;
            position: relative;
        }}
        .legend {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: rgba(0,0,0,0.7);
            padding: 15px;
            border-radius: 10px;
            z-index: 100;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            margin: 5px 0;
        }}
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 10px;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            padding: 30px;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.1);
            padding: 20px 40px;
            border-radius: 15px;
            text-align: center;
            backdrop-filter: blur(10px);
        }}
        .stat-value {{
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(90deg, #00d4ff, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .stat-label {{
            color: #888;
            margin-top: 5px;
        }}
        .marker-list {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .marker-item {{
            display: flex;
            align-items: center;
            background: rgba(255,255,255,0.05);
            padding: 15px;
            margin: 10px 0;
            border-radius: 10px;
            border-left: 4px solid;
        }}
        .marker-icon {{
            font-size: 2rem;
            margin-right: 15px;
        }}
        .marker-info h3 {{ margin-bottom: 5px; }}
        .marker-info p {{ color: #888; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 {title}</h1>
        <p>Real-time global impact visualization</p>
    </div>
    
    <div id="globe-container">
        <div class="legend">
            <h4>Impact Severity</h4>
            <div class="legend-item">
                <div class="legend-color" style="background: #4CAF50;"></div>
                <span>Low</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #FFC107;"></div>
                <span>Medium</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #FF9800;"></div>
                <span>High</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #F44336;"></div>
                <span>Critical</span>
            </div>
        </div>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-value">{len(markers)}</div>
            <div class="stat-label">Impact Points</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{len(connections)}</div>
            <div class="stat-label">Connections</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{len([m for m in markers if m.severity in ['high', 'critical']])}</div>
            <div class="stat-label">Critical Alerts</div>
        </div>
    </div>
    
    <div class="marker-list">
        <h2>📍 Impact Markers</h2>
        {"".join([f'''
        <div class="marker-item" style="border-color: {m.color};">
            <div class="marker-icon">{"🔴" if m.severity == "critical" else "🟠" if m.severity == "high" else "🟡" if m.severity == "medium" else "🟢"}</div>
            <div class="marker-info">
                <h3>{m.label}</h3>
                <p>{m.description} | {m.location.name}, {m.location.country}</p>
            </div>
        </div>''' for m in markers])}
    </div>
    
    <script>
        // Globe visualization placeholder
        // In production, this would use Three.js Globe or similar
        const container = document.getElementById('globe-container');
        
        // Add a placeholder message
        const placeholder = document.createElement('div');
        placeholder.style.cssText = 'position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;';
        placeholder.innerHTML = '<h2>🌍 Interactive Globe</h2><p>3D visualization requires WebGL support</p>';
        container.appendChild(placeholder);
        
        // Marker data for interactive features
        const markers = {json.dumps(markers_data)};
        const connections = {json.dumps(connections_data)};
        
        console.log('Digital Twin loaded with', markers.length, 'markers and', connections.length, 'connections');
    </script>
</body>
</html>'''
        
        return html_template
    
    def save_visualization(self, filename: str = "digital_twin.html",
                            snapshot: Optional[GlobeSnapshot] = None) -> Path:
        """
        Save the visualization to an HTML file.
        
        Args:
            filename: Output filename.
            snapshot: Optional snapshot to visualize.
        
        Returns:
            Path to the saved file.
        """
        html = self.generate_html_visualization(snapshot)
        output_file = self.output_path / filename
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"🌍 Digital Twin: Saved visualization to {output_file}")
        return output_file
    
    def clear(self):
        """Clear all markers and connections."""
        self.markers = []
        self.connections = []
        print("🌍 Digital Twin: Cleared all markers and connections")
    
    def get_summary(self) -> str:
        """Get a summary of the current visualization state."""
        severity_counts = {}
        for m in self.markers:
            severity_counts[m.severity] = severity_counts.get(m.severity, 0) + 1
        
        status_counts = {}
        for c in self.connections:
            status_counts[c.status] = status_counts.get(c.status, 0) + 1
        
        lines = [
            f"🌍 DIGITAL TWIN SUMMARY",
            f"{'=' * 50}",
            f"Total Markers: {len(self.markers)}",
            f"Total Connections: {len(self.connections)}",
            f"Snapshots: {len(self.snapshots)}",
            f"",
            f"📍 MARKERS BY SEVERITY:",
        ]
        
        for sev, count in sorted(severity_counts.items()):
            lines.append(f"  {sev}: {count}")
        
        lines.append(f"\n🔗 CONNECTIONS BY STATUS:")
        for status, count in sorted(status_counts.items()):
            lines.append(f"  {status}: {count}")
        
        if self.markers:
            lines.append(f"\n📍 MARKER LOCATIONS:")
            for m in self.markers[:5]:
                lines.append(f"  • [{m.severity.upper()}] {m.label} - {m.location.name}")
            if len(self.markers) > 5:
                lines.append(f"  ... and {len(self.markers) - 5} more")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test the Digital Twin
    dt = DigitalTwin()
    
    # Add supply chain impacts
    dt.add_impact_marker(
        location_key="taiwan_hsinchu",
        impact_type="supply_chain",
        severity="critical",
        label="TSMC Production Halt",
        description="Major semiconductor fab experiencing power issues",
        data={"estimated_impact": "$500M"}
    )
    
    dt.add_impact_marker(
        location_key="korea_suwon",
        impact_type="supply_chain",
        severity="high",
        label="Samsung Memory Shortage",
        description="Memory production below capacity",
    )
    
    dt.add_impact_marker(
        location_key="usa_austin",
        impact_type="facility",
        severity="medium",
        label="Assembly Plant Delayed",
        description="Downstream impact from component shortage",
    )
    
    # Add connections
    dt.add_connection("taiwan_hsinchu", "usa_austin", "supply", "disrupted", "Chip Supply Route")
    dt.add_connection("korea_suwon", "usa_austin", "supply", "active", "Memory Supply Route")
    dt.add_connection("taiwan_hsinchu", "japan_tokyo", "supply", "rerouted", "Rerouted via Japan")
    
    # Create snapshot
    snapshot = dt.create_snapshot("Supply Chain Disruption - Feb 2024", center_key="taiwan_hsinchu")
    
    # Save visualization
    dt.save_visualization("supply_chain_impact.html", snapshot)
    
    # Print summary
    print("\n" + dt.get_summary())
