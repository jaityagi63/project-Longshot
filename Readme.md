# 🎯 Project Longshot

> **An AI-Powered Strategic Intelligence & Crisis Management System**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🌟 Overview

**Project Longshot** is a modular, AI-driven platform designed to help organizations navigate complex crises and strategic decisions. It combines real-time intelligence gathering, predictive modeling, multi-agent deliberation, and automated response generation into a cohesive system.

Think of it as your organization's **AI War Room** — capable of detecting emerging threats, simulating their impact, debating response strategies across multiple perspectives, and generating actionable outputs.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PROJECT LONGSHOT                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐               │
│   │   DETECTIVE   │───▶│   CONNECTOR   │───▶│     SEER      │               │
│   │  Intelligence │    │   Relevance   │    │  Prediction   │               │
│   └───────────────┘    └───────────────┘    └───────────────┘               │
│          │                                          │                        │
│          ▼                                          ▼                        │
│   ┌───────────────┐                         ┌───────────────┐               │
│   │ TRUTH SERUM   │                         │    COUNCIL    │               │
│   │  Counter-Intel│                         │   Strategy    │               │
│   └───────────────┘                         └───────────────┘               │
│                                                     │                        │
│                                                     ▼                        │
│   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐               │
│   │   HISTORIAN   │◀──▶│     HAND      │◀───│  TOWN CRIER   │               │
│   │    Wisdom     │    │  Operations   │    │    Comms      │               │
│   └───────────────┘    └───────────────┘    └───────────────┘               │
│          │                    │                                              │
│          ▼                    ▼                                              │
│   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐               │
│   │   BLACK BOX   │    │    LEDGER     │    │ DIGITAL TWIN  │               │
│   │   Hindsight   │    │     Audit     │    │ Visualization │               │
│   └───────────────┘    └───────────────┘    └───────────────┘               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Modules

| Module | Domain | Description |
|--------|--------|-------------|
| 🕵️ **Detective** | Intelligence | Searches the web for facts and news related to specific keywords or events |
| 🔗 **Connector** | Relevance | Maps external events to internal assets and stakeholders |
| 🔮 **Seer** | Prediction | Simulates the Domino Effect chain reaction of events |
| 🧪 **Truth Serum** | Counter-Intel | Filters deepfakes, misinformation, and botnets |
| 👥 **Council** | Strategy | Multi-agent debate system (Ops, Legal, Finance, PR perspectives) |
| ✋ **Hand** | Operations | Drafts code, purchase orders, and legal notices |
| 📢 **Town Crier** | Comms | Drafts unified messaging for all stakeholders |
| 📚 **Historian** | Wisdom | Retrieves precedents and stores post-mortem lessons |
| 📦 **Black Box** | Hindsight | Re-runs simulations to find what could have been done better |
| 📒 **Ledger** | Audit | Blockchain-backed immutable log of all actions and decisions |
| 🌍 **Digital Twin** | Visualization | Renders impacts on a 3D interactive globe |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Node.js 18+ (for Digital Twin visualization)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/project-longshot.git
cd project-longshot

# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### Running the System

```bash
# Run the main orchestrator
python main.py

# Or run individual modules
python -m src.detective.detective "your search query"
python -m src.seer.seer
python -m src.council.council
```

---

## 📁 Project Structure

```
project-Longshot/
├── main.py                    # Main orchestrator
├── requirements.txt           # Python dependencies
├── config.py                  # Global configuration
├── Readme.md                  # This file
├── LICENSE                    # MIT License
│
├── src/
│   ├── __init__.py
│   ├── detective/             # Intelligence module
│   │   ├── __init__.py
│   │   ├── detective.py
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   ├── connector/             # Relevance mapping
│   │   ├── __init__.py
│   │   ├── connector.py
│   │   └── README.md
│   │
│   ├── seer/                  # Prediction engine
│   │   ├── __init__.py
│   │   ├── seer.py
│   │   └── README.md
│   │
│   ├── truth_serum/           # Counter-intelligence
│   │   ├── __init__.py
│   │   ├── truth_serum.py
│   │   └── README.md
│   │
│   ├── council/               # Multi-agent strategy
│   │   ├── __init__.py
│   │   ├── council.py
│   │   └── README.md
│   │
│   ├── hand/                  # Operations & drafting
│   │   ├── __init__.py
│   │   ├── hand.py
│   │   └── README.md
│   │
│   ├── town_crier/            # Communications
│   │   ├── __init__.py
│   │   ├── town_crier.py
│   │   └── README.md
│   │
│   ├── historian/             # Knowledge & precedents
│   │   ├── __init__.py
│   │   ├── historian.py
│   │   └── README.md
│   │
│   ├── black_box/             # Post-mortem analysis
│   │   ├── __init__.py
│   │   ├── black_box.py
│   │   └── README.md
│   │
│   ├── ledger/                # Immutable audit log
│   │   ├── __init__.py
│   │   ├── ledger.py
│   │   └── README.md
│   │
│   └── digital_twin/          # 3D visualization
│       ├── __init__.py
│       ├── digital_twin.py
│       └── README.md
│
├── data/                      # Data storage
│   ├── precedents/            # Historical cases
│   ├── assets/                # Organization assets
│   └── logs/                  # System logs
│
└── tests/                     # Unit tests
    └── ...
```

---

## 💡 Use Cases

### 1. **Supply Chain Disruption**
A major supplier announces bankruptcy. Longshot:
- **Detective** finds breaking news and related coverage
- **Connector** maps the supplier to affected products and contracts
- **Seer** predicts cascading effects on production timelines
- **Council** debates mitigation strategies from Ops, Legal, and Finance perspectives
- **Hand** drafts emergency POs to alternative suppliers
- **Town Crier** prepares customer notifications

### 2. **Cybersecurity Incident**
A data breach is detected. Longshot:
- **Detective** gathers threat intelligence
- **Truth Serum** verifies the authenticity of leak claims
- **Seer** models potential regulatory and reputational impacts
- **Council** determines disclosure strategy
- **Hand** drafts legal notices and code patches
- **Ledger** maintains immutable incident log for compliance

### 3. **Geopolitical Event**
New trade sanctions are announced. Longshot:
- **Detective** collects policy details and expert analysis
- **Connector** identifies exposed assets and partners
- **Historian** retrieves similar past events and outcomes
- **Seer** simulates financial impacts
- **Council** debates strategic pivots
- **Digital Twin** visualizes global supply chain exposure

---

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
# API Keys (optional - enables enhanced features)
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key

# Database
DATABASE_URL=sqlite:///data/longshot.db

# Logging
LOG_LEVEL=INFO

# Feature Flags
ENABLE_BLOCKCHAIN_LEDGER=false
ENABLE_3D_VISUALIZATION=true
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific module tests
pytest tests/test_detective.py -v
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- DuckDuckGo for anonymous search capabilities
- The open-source AI community
- All contributors to this project

---

<p align="center">
  <strong>Built with ❤️ for strategic resilience</strong>
</p>
