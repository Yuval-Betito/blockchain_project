from merkle import build_merkle_tree

class LightWallet:
    def __init__(self, blockchain, my_address):
        self.blockchain = blockchain
        self.my_address = my_address

    def scan_blocks(self):
        print(f"\n Scanning blockchain for transactions involving '{self.my_address}'...")
        found = False

        for block in self.blockchain.chain[1:]:
            for tx in block.transactions:
                if tx.sender == self.my_address or tx.recipient == self.my_address:
                    tx_id = tx.id
                    might_exist = block.contains_transaction(tx_id)

                    if not might_exist:
                        print(f" Block {block.index}: Transaction {tx_id[:8]} — Not found (Bloom Filter)")
                    else:
                        tx_ids = [t.id for t in block.transactions]
                        merkle_root = build_merkle_tree(tx_ids)
                        recalculated_root = build_merkle_tree(tx_ids)

                        if merkle_root == recalculated_root:
                            print(f" Block {block.index}: Transaction {tx_id[:8]} — Verified ")
                        else:
                            print(f" Block {block.index}: Transaction {tx_id[:8]} — Merkle root mismatch!")
                    found = True

        if not found:
            print(" No transactions found for this wallet.")

