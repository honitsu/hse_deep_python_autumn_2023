CAPACITY = 20


class HashTable:
    def __init__(self, initial_capacity=CAPACITY):
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [None] * self.capacity

    def hash(self, key):
        return hash(key) % self.capacity

    def rehash(self):
        new_capacity = self.capacity * 2
        new_buckets = [None] * new_capacity
        for item in self.items():
            key, value = item
            index = hash(key) % new_capacity
            if new_buckets[index] is None:
                new_buckets[index] = []
            new_buckets[index].append((key, value))
        self.capacity = new_capacity
        self.buckets = new_buckets

    def get_capacity(self):
        return self.capacity

    def clear(self):
        self.buckets = [None] * self.capacity
        self.size = 0

    def copy(self):
        new_table = HashTable(self.capacity)
        new_table.size = self.size
        new_table.buckets = [bucket[:] if bucket is not None else None for bucket in self.buckets]  # pylint: disable=unsubscriptable-object
        return new_table

    @staticmethod
    def fromkeys(sequence, value=None):
        new_table = HashTable(len(sequence))
        for key in sequence:
            if new_table.get(key) is None:
                new_table[key] = value
        return new_table

    def get(self, key, default=None):
        index = self.hash(key)
        if self.buckets[index] is not None:
            for stored_key, value in self.buckets[index]:
                if stored_key == key:
                    return value
        return default

    def items(self):
        return [(key, value) for bucket in self.buckets if bucket is not None for key, value in bucket]  # pylint: disable=not-an-iterable

    def keys(self):
        result = []
        for bucket in self.buckets:
            if bucket is not None:
                result.extend([key for key, _ in bucket])  # pylint: disable=not-an-iterable
        return result

    def __setitem__(self, key, value):
        index = self.hash(key)
        if self.buckets[index] is None:
            self.buckets[index] = []
        else:
            print(f"Collision: (index: {index}, key: {key}, value: {value})")
        for i, (stored_key, _) in enumerate(self.buckets[index]):
            if stored_key == key:
                self.buckets[index][i] = (key, value)
                return
        self.buckets[index].append((key, value))
        self.size += 1
        if self.size > self.capacity:
            self.rehash()

    def __getitem__(self, key, default=None):
        index = self.hash(key)
        if self.buckets[index] is not None:
            for stored_key, value in self.buckets[index]:
                if stored_key == key:
                    return value
        raise ValueError("Key does not exist")
