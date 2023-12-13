import argparse
from lru_cache import LRUCache


def main():
    parser = argparse.ArgumentParser(description="LRUCache arg parser")
    parser.add_argument("-s", action="store_true", help="This is the 's' variable")
    parser.add_argument("-f", action="store_true", help="This is the 'f' variable")
    args = parser.parse_args()
    use_stdout = args.s
    use_filter = args.f

    cache = LRUCache(1, use_stdout, use_filter)
    cache.get(1)
    cache.set(1, "One")
    cache.get(1)

    cache = LRUCache(0, use_stdout, use_filter)
    cache.set(1, "One")
    cache.get(1)

    cache = LRUCache(1, use_stdout, use_filter)
    cache.set(1, "One")
    cache.set(2, "Two")
    cache.set(3, "Three")
    cache.set(3, "Три")
    cache.get(3)
    cache.get(2)
    cache.get(1)


if __name__ == "__main__":
    main()