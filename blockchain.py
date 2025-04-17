import hashlib
import json
import time
from merkle import build_merkle_tree
from bloom import BloomFilter

class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.merkle_root = self.compute_merkle_root()
        self.bloom_filter = self.build_bloom_filter()
        self.hash = self.calculate_hash()

    def compute_merkle_root(self):
        tx_ids = [tx.id for tx in self.transactions]
        root = build_merkle_tree(tx_ids)
        return root if root else ""

    def build_bloom_filter(self):
        bf = BloomFilter()
        for tx in self.transactions:
            bf.add(tx.id)
        return bf

    def contains_transaction(self, tx_id):
        return self.bloom_filter.might_contain(tx_id)

    def calculate_hash(self):
        block_content = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'merkle_root': self.merkle_root
        }
        block_string = json.dumps(block_content, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def __repr__(self):
        return f"<Block {self.index} | {len(self.transactions)} tx | Merkle: {self.merkle_root[:10]}... | Hash: {self.hash[:10]}...>"

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 2
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], "0")
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

