"""
Project Longshot - Source Package
=================================
AI-Powered Strategic Intelligence & Crisis Management System

Modules:
    - detective: Web intelligence gathering
    - connector: Asset-event mapping
    - seer: Domino effect prediction
    - truth_serum: Misinformation filtering
    - council: Multi-agent strategy debate
    - hand: Operational drafting
    - town_crier: Stakeholder communications
    - historian: Precedent retrieval
    - black_box: Post-mortem analysis
    - ledger: Immutable audit log
    - digital_twin: 3D visualization
"""

__version__ = "1.0.0"
__author__ = "Longshot Team"

from .detective.detective import Detective
from .connector.connector import Connector
from .seer.seer import Seer
from .truth_serum.truth_serum import TruthSerum
from .council.council import Council
from .hand.hand import Hand
from .town_crier.town_crier import TownCrier
from .historian.historian import Historian
from .black_box.black_box import BlackBox
from .ledger.ledger import Ledger
from .digital_twin.digital_twin import DigitalTwin

__all__ = [
    "Detective",
    "Connector",
    "Seer",
    "TruthSerum",
    "Council",
    "Hand",
    "TownCrier",
    "Historian",
    "BlackBox",
    "Ledger",
    "DigitalTwin",
]
