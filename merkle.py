import hashlib

def hash_data(data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()

def build_merkle_tree(transaction_ids):
    if not transaction_ids:
        return None

    current_level = [hash_data(tx_id) for tx_id in transaction_ids]

    while len(current_level) > 1:
        next_level = []

        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else current_level[i]
            combined = hash_data(left + right)
            next_level.append(combined)

        current_level = next_level

    return current_level[0]
