# Town Crier 📢

**Domain:** Communications  
**Description:** Drafts unified messaging for all stakeholders.

## Overview

The Town Crier module creates coordinated communication plans for multiple stakeholder groups. It tailors messages, tone, and channels for each audience while maintaining consistency.

## Features

- **Multi-Stakeholder Messaging**: Tailored content per audience
- **Communication Sequencing**: Proper notification order
- **Tone Adaptation**: Adjusts messaging style appropriately
- **Q&A Preparation**: Generates anticipated questions and answers
- **Talking Points**: Provides spokesperson guidance
- **Channel Selection**: Matches channels to stakeholders

## Stakeholder Types

- `employees` - Internal team members
- `customers` - End users and clients
- `investors` - Shareholders and analysts
- `media` - Press and journalists
- `regulators` - Government and compliance bodies
- `partners` - Business partners and vendors
- `board` - Board of directors
- `public` - General public

## Message Tones

- `informational` - Neutral, factual updates
- `reassuring` - Calming, confidence-building
- `urgent` - Time-sensitive, action-required
- `apologetic` - Acknowledging issues
- `formal` - Official, compliance-oriented

## Usage

```python
from src.town_crier import TownCrier, StakeholderType

crier = TownCrier()

situation = {
    "summary": "Service disruption affecting customers",
    "severity": "high",
    "actions_taken": ["Engineering deployed", "Backup activated"],
    "financial_impact": 1000000,
    "timeline": "Expected resolution in 24 hours",
    "spokesperson": "COO",
}

plan = crier.broadcast(
    situation,
    stakeholders=[
        StakeholderType.EMPLOYEES,
        StakeholderType.CUSTOMERS,
        StakeholderType.MEDIA,
    ]
)

print(f"Messages prepared: {len(plan.messages)}")
print(f"Sequence: {[s['stakeholder'] for s in plan.communication_sequence]}")

# View a specific message
for msg in plan.messages:
    if msg.stakeholder == StakeholderType.CUSTOMERS:
        print(msg.content)
```

## Output

The `CommunicationPlan` contains:
- `plan_id`: Unique plan identifier
- `messages`: List of stakeholder-specific messages
- `communication_sequence`: Ordered notification schedule
- `talking_points`: Spokesperson guidance
- `qa_pairs`: Anticipated Q&A
- `spokesperson`: Designated spokesperson

## Communication Sequence

Default notification order:
1. Employees (T+0) - Internal first
2. Board (T+0) - Governance requirement
3. Regulators (T+1hr) - If required
4. Customers (T+2hr) - Affected parties
5. Partners (T+2hr) - Business partners
6. Investors (T+4hr) - After operational comms
7. Media (T+6hr) - Only if needed
8. Public (T+6hr) - Concurrent with media
