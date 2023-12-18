# test_log.py

import argparse
import setup_logger
from lru_cache import LRUCache


def main():
    parser = argparse.ArgumentParser(description="This module implements the LRUCache class, which logs rows of different levels in 'cache.log'.")
    parser.add_argument("-s", action="store_true", help="Log messages to file and console")
    parser.add_argument("-f", action="store_true", help="Do not log messages with word 'updated'")
    args = parser.parse_args()
    setup_logger.USE_STDOUT = args.s
    setup_logger.USE_FILTER = args.f

    cache = LRUCache(1, setup_logger.USE_STDOUT, setup_logger.USE_FILTER)
    cache.get(1)
    cache.set(1, "One")
    cache.get(1)

    cache = LRUCache(0, setup_logger.USE_STDOUT, setup_logger.USE_FILTER)
    cache.set(1, "One")
    cache.get(1)

    cache = LRUCache(1, setup_logger.USE_STDOUT, setup_logger.USE_FILTER)
    cache.set(1, "One")
    cache.set(2, "Two")
    cache.set(3, "Three")
    cache.set(3, "Три")
    cache.set(3, "03")
    cache.set(3, "_3_")
    cache.set(3, "(3)")
    cache.set(3, "-=< 3 >=-")
    cache.get(3)
    cache.get(2)
    cache.get(1)


if __name__ == "__main__":
    main()
