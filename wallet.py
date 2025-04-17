from collections import defaultdict

class WalletManager:
    def __init__(self, starting_balance=300):
        self.balances = defaultdict(lambda: starting_balance)
        self.burned = 0
        self.mined = 0

    def process_transaction(self, tx, miner_address):
        sender = tx.sender
        recipient = tx.recipient
        total = tx.total_cost

        if self.balances[sender] < total:
            print(f" {sender} has insufficient funds for transaction {tx.id[:8]}")
            return False

        self.balances[sender] -= total
        self.balances[recipient] += tx.amount
        self.burned += tx.base_fee
        self.balances[miner_address] += tx.priority_fee

        return True

    def reward_miner(self, miner_address, reward=50):
        self.balances[miner_address] += reward
        self.mined += reward

    def get_balance(self, address):
        return self.balances[address]

    def print_balances(self):
        print("\n Wallet Balances:")
        for address, balance in sorted(self.balances.items()):
            print(f"{address}: {balance} coins")

    def print_summary(self):
        total_supply = sum(self.balances.values())
        print(f"\n Network Summary:")
        print(f"Total coins in network: {total_supply}")
        print(f"Total mined: {self.mined}")
        print(f"Total burned: {self.burned}")
