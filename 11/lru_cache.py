import setup_logger


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
    def __init__(self, limit=42, use_stdout=False, use_filter=False):
        self.logger = setup_logger.startup(__name__)
        self.limit = limit
        self.cache = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.use_stdout = use_stdout
        self.use_filter = use_filter
        self.logger.debug("LRUCache object created")

    def __del__(self):
        self.logger.debug("LRUCache object deleted")

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            _remove(node)
            self._add(node)
            self.logger.debug("get() Existing key (%s) has value: %s", key, node.value)
            return node.value
        self.logger.warning("get() Missing key: %s", key)
        return None

    def set(self, key, value):
        if self.limit > 0:
            if key in self.cache:
                node = self.cache[key]
                _remove(node)
                self.logger.info("set() The value of the %s key has been updated in the cache.", key)
            elif len(self.cache) >= self.limit:
                self.logger.info("set() The cache is full. The new key %s will replace the oldest one (%s).", key, self.tail.prev.key)

                del self.cache[self.tail.prev.key]
                _remove(self.tail.prev)
            else:
                self.logger.info("set() New key %s added to cache.", key)

            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add(new_node)
        else:
            self.logger.error("set() Cannot set value for key %s: cache has zero size", key)

    def _add(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.logger.debug("New node added")
