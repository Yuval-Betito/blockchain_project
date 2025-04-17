import uuid
import time
import hashlib

class Transaction:
    def __init__(self, sender, recipient, amount, base_fee=2, priority_fee=3):
        self.id = str(uuid.uuid4())
        self.timestamp = time.time()
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.base_fee = base_fee
        self.priority_fee = priority_fee
        self.total_cost = amount + base_fee + priority_fee
        self.signature = self.generate_signature()

    def generate_signature(self):
        data = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "base_fee": self.base_fee,
            "priority_fee": self.priority_fee,
            "total_cost": self.total_cost
        }

    def __repr__(self):
        return f"<Transaction {self.id[:8]} | {self.sender} → {self.recipient} | {self.amount} coins>"

