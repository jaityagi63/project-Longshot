# Ledger 📒

**Domain:** Audit  
**Description:** Blockchain-backed immutable log of all actions and decisions.

## Overview

The Ledger module maintains an immutable audit trail of all system activities. It uses blockchain principles with proof-of-work to ensure tamper-evident logging.

## Features

- **Immutable Records**: Cannot modify past entries
- **Blockchain Structure**: Linked blocks with hashes
- **Proof-of-Work**: Mining difficulty for tamper resistance
- **Chain Verification**: Integrity checking
- **Typed Entries**: Categorized log entries
- **Audit Trail**: Filtered historical queries

## Entry Types

- `action` - Operations performed
- `decision` - Strategic decisions made
- `event` - External/internal events
- `communication` - Messages sent
- `document` - Documents created
- `system` - System events

## Usage

### Recording Entries

```python
from src.ledger import Ledger

ledger = Ledger(difficulty=2)

# Record an event
ledger.record_event(
    source="Detective",
    event="Detected supply chain news",
    severity="high",
    data={"results": 5}
)

# Record a decision
ledger.record_decision(
    decision_maker="Council",
    decision="Activate contingency plan",
    rationale="High severity supply risk",
    alternatives_considered=["Wait and monitor", "Partial response"]
)

# Record an action
ledger.record_action(
    actor="Hand",
    action="Generated purchase order",
    result="PO-2024-0001 created",
    metadata={"vendor": "Backup Inc", "value": 50000}
)

# Force commit pending entries to a block
ledger.commit()
```

### Verification

```python
# Verify chain integrity
is_valid, error = ledger.verify_chain()
print(f"Chain valid: {is_valid}")

# Get audit trail
trail = ledger.get_audit_trail(
    entry_types=["decision", "action"],
    start_time="2024-01-01T00:00:00"
)
```

## Block Structure

Each block contains:
- `index`: Block number
- `timestamp`: Creation time
- `entries`: List of ledger entries
- `previous_hash`: Link to previous block
- `nonce`: Proof-of-work value
- `hash`: Block hash (meets difficulty requirement)

## Entry Structure

Each entry contains:
- `id`: Unique entry ID
- `timestamp`: Entry creation time
- `entry_type`: Category of entry
- `actor`: Who/what created the entry
- `action`: Description of what happened
- `details`: Additional context
- `hash`: Entry hash
- `previous_hash`: Link to previous entry

## Configuration

- `difficulty`: Number of leading zeros required (default: 2)
- `entries_per_block`: Entries before auto-commit (default: 10)
