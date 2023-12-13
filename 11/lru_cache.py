import logging
import sys


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s %(levelname)s %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):  # pylint: disable=function-redefined
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%a %d.%m.%Y %H:%M:%S")
        return formatter.format(record)


class NoParsingFilter(logging.Filter):
    def filter(self, record):
        return "updated" not in record.getMessage()


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
    def setup_custom_logger(self, name):
        is_set = logging.getLogger(__name__).hasHandlers()
        formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        handler = logging.FileHandler("cache.log", mode="a")
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        if self.use_filter:
            logger.addFilter(NoParsingFilter())
        if not is_set:
            logger.addHandler(handler)
        if self.use_stdout:
            screen_handler = logging.StreamHandler(stream=sys.stdout)
            screen_handler.setFormatter(CustomFormatter())
            if not is_set:
                logger.addHandler(screen_handler)
            logger.debug("Stdout logging activated")

        return logger

    def __init__(self, limit=42, use_stdout=False, use_filter=False):
        self.limit = limit
        self.cache = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.use_stdout = use_stdout
        self.use_filter = use_filter
        self.logger = self.setup_custom_logger(__name__)

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            _remove(node)
            self._add(node)
            self.logger.debug("Existing key (%s) has value: %s", key, node.value)
            return node.value
        self.logger.warning("Missing key: %s", key)
        return None

    def set(self, key, value):
        if self.limit > 0:
            if key in self.cache:
                node = self.cache[key]
                _remove(node)
                self.logger.info("Key %s cache updated.", key)
            elif len(self.cache) >= self.limit:
                self.logger.info("Cache full. New key %s will push out the oldest one.", key)
                del self.cache[self.tail.prev.key]
                _remove(self.tail.prev)
            else:
                self.logger.info("New key %s added to cache.", key)

            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add(new_node)
        else:
            self.logger.error("Cannot set value for key %s: cache has zero size", key)

    def _add(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
