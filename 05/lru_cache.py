class Node:  # pylint: disable=too-few-public-methods
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


def _remove(node):
    prev_node = node.prev
    next_node = node.next
    prev_node.next = next_node
    next_node.prev = prev_node


class LRUCache:
    def __init__(self, limit=42):
        self.limit = limit
        self.cache = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            _remove(node)
            self._add(node)
            return node.value
        return None

    def set(self, key, value):
        if self.limit > 0:
            if key in self.cache:
                node = self.cache[key]
                _remove(node)
            elif len(self.cache) >= self.limit:
                del self.cache[self.tail.prev.key]
                _remove(self.tail.prev)

            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add(new_node)

    def _add(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
