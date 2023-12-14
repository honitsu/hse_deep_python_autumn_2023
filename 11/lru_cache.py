import logging
import sys
import locale


class CustomFormatter(logging.Formatter):

    # Цвета для вывода журнала на консоль
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
        # Чт 14.12.2023 11:55:10
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
        locale.setlocale(locale.LC_TIME, locale="ru_RU.utf8")
        is_set = logging.getLogger(__name__).hasHandlers()
        formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        handler = logging.FileHandler("cache.log", mode="a")
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        if self.use_filter:
            logger.addFilter(NoParsingFilter())
            logger.debug("Log filtering is enabled.")
        if not is_set:
            logger.addHandler(handler)
        if self.use_stdout:
            screen_handler = logging.StreamHandler(stream=sys.stdout)
            screen_handler.setFormatter(CustomFormatter())
            if not is_set:
                logger.addHandler(screen_handler)
            logger.debug("Console output of logs is enabled.")

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
