import json
from transaction import Transaction
from blockchain import Block, Blockchain
from wallet import WalletManager
from light_wallet import LightWallet

def load_transactions_from_json(file_path):
    with open(file_path, 'r') as f:
        raw_data = json.load(f)
    transactions = []
    for tx in raw_data:
        transaction = Transaction(
            sender=tx["sender"],
            recipient=tx["recipient"],
            amount=tx["amount"],
            base_fee=2,
            priority_fee=3
        )
        transactions.append(transaction)
    return transactions

def create_blocks_from_transactions(transactions, blockchain, wallet_manager, block_size=4):
    i = 0
    while i < len(transactions):
        chunk = []
        miner_address = f"Miner{len(blockchain.chain)}"
        tx_group = transactions[i:i + block_size]

        for tx in tx_group:
            success = wallet_manager.process_transaction(tx, miner_address)
            if success:
                chunk.append(tx)

        if chunk:
            block = Block(
                index=len(blockchain.chain),
                transactions=chunk,
                previous_hash=blockchain.get_latest_block().hash
            )
            blockchain.add_block(block)
            wallet_manager.reward_miner(miner_address)

        i += block_size

def print_blockchain_summary(blockchain):
    print("\n Blockchain Summary:")
    for block in blockchain.chain:
        print(block)

if __name__ == "__main__":
    mempool_path = "mempool.json"
    transactions = load_transactions_from_json(mempool_path)
    blockchain = Blockchain()
    wallet_manager = WalletManager()

    create_blocks_from_transactions(transactions, blockchain, wallet_manager)

    print_blockchain_summary(blockchain)
    wallet_manager.print_balances()
    wallet_manager.print_summary()

    my_wallet = LightWallet(blockchain, "Alice")
    my_wallet.scan_blocks()

    bob_wallet = LightWallet(blockchain, "Bob")
    bob_wallet.scan_blocks()

