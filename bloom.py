import hashlib

class BloomFilter:
    def __init__(self, size=1000, hash_count=3):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * size

    def _hashes(self, item):
        results = []
        for i in range(self.hash_count):
            hash_input = f"{item}_{i}".encode()
            hash_result = int(hashlib.sha256(hash_input).hexdigest(), 16)
            results.append(hash_result % self.size)
        return results

    def add(self, item):
        for index in self._hashes(item):
            self.bit_array[index] = 1

    def might_contain(self, item):
        return all(self.bit_array[index] == 1 for index in self._hashes(item))
