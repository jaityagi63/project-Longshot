"""
Ledger Module - Immutable Audit Log
====================================
Blockchain-backed immutable log of all actions and decisions.
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class LedgerEntry:
    """A single entry in the ledger."""
    id: str
    timestamp: str
    entry_type: str  # action, decision, event, communication, document
    actor: str
    action: str
    details: Dict[str, Any]
    related_entries: List[str]
    hash: str = ""
    previous_hash: str = ""


@dataclass
class Block:
    """A block in the ledger chain."""
    index: int
    timestamp: str
    entries: List[LedgerEntry]
    previous_hash: str
    nonce: int = 0
    hash: str = ""
    
    def calculate_hash(self) -> str:
        """Calculate the hash of this block."""
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "entries": [asdict(e) for e in self.entries],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Ledger:
    """
    The Ledger module: Audit.
    Blockchain-backed immutable log of all actions and decisions.
    """

    def __init__(self, storage_path: Optional[Path] = None, difficulty: int = 2):
        """
        Initialize the Ledger.
        
        Args:
            storage_path: Path to persist the ledger.
            difficulty: Mining difficulty (number of leading zeros required).
        """
        self.storage_path = storage_path or Path("data/ledger")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.difficulty = difficulty
        self.chain: List[Block] = []
        self.pending_entries: List[LedgerEntry] = []
        self.entries_per_block = 10
        
        # Initialize with genesis block
        self._create_genesis_block()
    
    def _create_genesis_block(self):
        """Create the genesis (first) block."""
        genesis_entry = LedgerEntry(
            id="GENESIS",
            timestamp=datetime.now().isoformat(),
            entry_type="system",
            actor="SYSTEM",
            action="Ledger initialized",
            details={"version": "1.0.0", "difficulty": self.difficulty},
            related_entries=[],
        )
        
        genesis_block = Block(
            index=0,
            timestamp=datetime.now().isoformat(),
            entries=[genesis_entry],
            previous_hash="0" * 64,
        )
        
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)
        
        print(f"📒 Ledger initialized with genesis block.")
    
    def _mine_block(self, block: Block) -> Block:
        """Mine a block (find valid hash with required difficulty)."""
        target = "0" * self.difficulty
        
        while not block.hash.startswith(target):
            block.nonce += 1
            block.hash = block.calculate_hash()
        
        return block
    
    def record(self, entry_type: str, actor: str, action: str,
               details: Optional[Dict[str, Any]] = None,
               related_entries: Optional[List[str]] = None) -> LedgerEntry:
        """
        Record an action in the ledger.
        
        Args:
            entry_type: Type of entry (action, decision, event, communication, document).
            actor: Who/what performed the action.
            action: Description of the action.
            details: Additional details as a dictionary.
            related_entries: IDs of related ledger entries.
        
        Returns:
            The created LedgerEntry.
        """
        entry_id = f"LE-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        entry = LedgerEntry(
            id=entry_id,
            timestamp=datetime.now().isoformat(),
            entry_type=entry_type,
            actor=actor,
            action=action,
            details=details or {},
            related_entries=related_entries or [],
        )
        
        # Calculate entry hash
        entry_data = asdict(entry)
        entry_data.pop("hash", None)
        entry_data.pop("previous_hash", None)
        entry.hash = hashlib.sha256(json.dumps(entry_data, sort_keys=True).encode()).hexdigest()
        
        # Set previous hash from last entry
        if self.pending_entries:
            entry.previous_hash = self.pending_entries[-1].hash
        elif self.chain:
            last_block = self.chain[-1]
            if last_block.entries:
                entry.previous_hash = last_block.entries[-1].hash
            else:
                entry.previous_hash = last_block.hash
        
        self.pending_entries.append(entry)
        
        # Auto-mine if we have enough entries
        if len(self.pending_entries) >= self.entries_per_block:
            self._commit_pending_entries()
        
        print(f"📒 Ledger recorded: [{entry_type}] {action[:50]}...")
        return entry
    
    def _commit_pending_entries(self):
        """Commit pending entries to a new block."""
        if not self.pending_entries:
            return
        
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            entries=self.pending_entries.copy(),
            previous_hash=self.chain[-1].hash,
        )
        
        # Mine the block
        new_block = self._mine_block(new_block)
        
        self.chain.append(new_block)
        self.pending_entries = []
        
        print(f"📒 New block mined: #{new_block.index} (hash: {new_block.hash[:16]}...)")
    
    def commit(self):
        """Force commit of pending entries."""
        if self.pending_entries:
            self._commit_pending_entries()
    
    def record_decision(self, decision_maker: str, decision: str,
                        rationale: str, alternatives_considered: List[str] = None) -> LedgerEntry:
        """Convenience method to record a decision."""
        return self.record(
            entry_type="decision",
            actor=decision_maker,
            action=decision,
            details={
                "rationale": rationale,
                "alternatives_considered": alternatives_considered or [],
            }
        )
    
    def record_action(self, actor: str, action: str,
                      result: str = None, metadata: Dict[str, Any] = None) -> LedgerEntry:
        """Convenience method to record an action."""
        return self.record(
            entry_type="action",
            actor=actor,
            action=action,
            details={
                "result": result,
                **(metadata or {}),
            }
        )
    
    def record_event(self, source: str, event: str,
                     severity: str = "info", data: Dict[str, Any] = None) -> LedgerEntry:
        """Convenience method to record an event."""
        return self.record(
            entry_type="event",
            actor=source,
            action=event,
            details={
                "severity": severity,
                **(data or {}),
            }
        )
    
    def record_communication(self, sender: str, recipients: List[str],
                              subject: str, channel: str) -> LedgerEntry:
        """Convenience method to record a communication."""
        return self.record(
            entry_type="communication",
            actor=sender,
            action=f"Sent: {subject}",
            details={
                "recipients": recipients,
                "channel": channel,
                "subject": subject,
            }
        )
    
    def record_document(self, creator: str, document_type: str,
                        document_id: str, title: str) -> LedgerEntry:
        """Convenience method to record document creation."""
        return self.record(
            entry_type="document",
            actor=creator,
            action=f"Created {document_type}: {title}",
            details={
                "document_type": document_type,
                "document_id": document_id,
                "title": title,
            }
        )
    
    def verify_chain(self) -> Tuple[bool, Optional[str]]:
        """
        Verify the integrity of the entire chain.
        
        Returns:
            Tuple of (is_valid, error_message).
        """
        print("📒 Verifying ledger integrity...")
        
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verify current block's hash
            if current_block.hash != current_block.calculate_hash():
                return False, f"Block {i} hash is invalid"
            
            # Verify link to previous block
            if current_block.previous_hash != previous_block.hash:
                return False, f"Block {i} previous_hash doesn't match block {i-1}"
            
            # Verify difficulty requirement
            if not current_block.hash.startswith("0" * self.difficulty):
                return False, f"Block {i} doesn't meet difficulty requirement"
        
        print("✅ Ledger integrity verified.")
        return True, None
    
    def get_entries_by_type(self, entry_type: str) -> List[LedgerEntry]:
        """Get all entries of a specific type."""
        entries = []
        
        for block in self.chain:
            for entry in block.entries:
                if entry.entry_type == entry_type:
                    entries.append(entry)
        
        # Include pending entries
        for entry in self.pending_entries:
            if entry.entry_type == entry_type:
                entries.append(entry)
        
        return entries
    
    def get_entries_by_actor(self, actor: str) -> List[LedgerEntry]:
        """Get all entries by a specific actor."""
        entries = []
        
        for block in self.chain:
            for entry in block.entries:
                if entry.actor == actor:
                    entries.append(entry)
        
        # Include pending entries
        for entry in self.pending_entries:
            if entry.actor == actor:
                entries.append(entry)
        
        return entries
    
    def get_entry(self, entry_id: str) -> Optional[LedgerEntry]:
        """Get a specific entry by ID."""
        for block in self.chain:
            for entry in block.entries:
                if entry.id == entry_id:
                    return entry
        
        for entry in self.pending_entries:
            if entry.id == entry_id:
                return entry
        
        return None
    
    def get_audit_trail(self, start_time: str = None, end_time: str = None,
                        entry_types: List[str] = None) -> List[LedgerEntry]:
        """
        Get an audit trail of entries.
        
        Args:
            start_time: ISO format start time filter.
            end_time: ISO format end time filter.
            entry_types: List of entry types to include.
        
        Returns:
            List of matching entries in chronological order.
        """
        entries = []
        
        for block in self.chain:
            for entry in block.entries:
                # Apply filters
                if start_time and entry.timestamp < start_time:
                    continue
                if end_time and entry.timestamp > end_time:
                    continue
                if entry_types and entry.entry_type not in entry_types:
                    continue
                entries.append(entry)
        
        # Include pending entries
        for entry in self.pending_entries:
            if start_time and entry.timestamp < start_time:
                continue
            if end_time and entry.timestamp > end_time:
                continue
            if entry_types and entry.entry_type not in entry_types:
                continue
            entries.append(entry)
        
        return entries
    
    def export_chain(self) -> Dict[str, Any]:
        """Export the entire chain as a dictionary."""
        return {
            "metadata": {
                "version": "1.0.0",
                "difficulty": self.difficulty,
                "block_count": len(self.chain),
                "pending_entries": len(self.pending_entries),
                "exported_at": datetime.now().isoformat(),
            },
            "chain": [
                {
                    "index": block.index,
                    "timestamp": block.timestamp,
                    "hash": block.hash,
                    "previous_hash": block.previous_hash,
                    "nonce": block.nonce,
                    "entries": [asdict(e) for e in block.entries],
                }
                for block in self.chain
            ],
            "pending_entries": [asdict(e) for e in self.pending_entries],
        }
    
    def get_chain_summary(self) -> str:
        """Get a summary of the chain."""
        total_entries = sum(len(b.entries) for b in self.chain) + len(self.pending_entries)
        
        # Count by type
        type_counts = {}
        for block in self.chain:
            for entry in block.entries:
                type_counts[entry.entry_type] = type_counts.get(entry.entry_type, 0) + 1
        for entry in self.pending_entries:
            type_counts[entry.entry_type] = type_counts.get(entry.entry_type, 0) + 1
        
        lines = [
            f"📒 LEDGER SUMMARY",
            f"{'=' * 50}",
            f"Blocks: {len(self.chain)}",
            f"Total Entries: {total_entries}",
            f"Pending Entries: {len(self.pending_entries)}",
            f"Difficulty: {self.difficulty}",
            f"",
            f"📊 ENTRIES BY TYPE:",
        ]
        
        for entry_type, count in sorted(type_counts.items()):
            lines.append(f"  • {entry_type}: {count}")
        
        # Verify and report
        is_valid, error = self.verify_chain()
        lines.append(f"\n🔐 INTEGRITY: {'✅ VERIFIED' if is_valid else f'❌ COMPROMISED - {error}'}")
        
        return "\n".join(lines)
    
    def get_entry_report(self, entry: LedgerEntry) -> str:
        """Get a detailed report of a single entry."""
        lines = [
            f"📒 LEDGER ENTRY",
            f"{'─' * 40}",
            f"ID: {entry.id}",
            f"Type: {entry.entry_type}",
            f"Timestamp: {entry.timestamp}",
            f"Actor: {entry.actor}",
            f"Action: {entry.action}",
            f"",
            f"Details:",
        ]
        
        for key, value in entry.details.items():
            lines.append(f"  {key}: {value}")
        
        lines.append(f"\n🔗 Hash: {entry.hash[:32]}...")
        lines.append(f"🔗 Prev: {entry.previous_hash[:32]}...")
        
        if entry.related_entries:
            lines.append(f"\n📎 Related: {', '.join(entry.related_entries)}")
        
        return "\n".join(lines)




if __name__ == "__main__":
    # Test the Ledger
    ledger = Ledger(difficulty=2)
    
    # Record various entries
    ledger.record_event(
        source="Detective",
        event="Detected supplier disruption news",
        severity="high",
        data={"query": "semiconductor supply", "results": 5}
    )
    
    ledger.record_decision(
        decision_maker="Council",
        decision="Activate contingency protocol Alpha",
        rationale="High severity supply chain risk requires immediate action",
        alternatives_considered=["Wait and monitor", "Partial response"]
    )
    
    ledger.record_action(
        actor="Hand",
        action="Generated emergency purchase order",
        result="PO-2024-0001 created",
        metadata={"vendor": "Backup Supplies Inc", "value": 250000}
    )
    
    ledger.record_communication(
        sender="Town Crier",
        recipients=["customers@list.com", "partners@list.com"],
        subject="Important Service Update",
        channel="email"
    )
    
    ledger.record_document(
        creator="Hand",
        document_type="purchase_order",
        document_id="PO-2024-0001",
        title="Emergency Component Order"
    )
    
    # Force commit
    ledger.commit()
    
    # Print summary
    print("\n" + ledger.get_chain_summary())
    
    # Get audit trail
    print("\n--- AUDIT TRAIL ---")
    trail = ledger.get_audit_trail(entry_types=["decision", "action"])
    for entry in trail:
        print(f"  [{entry.entry_type}] {entry.actor}: {entry.action}")
