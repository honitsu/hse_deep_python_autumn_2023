import cProfile
from functools import wraps
import pstats


def f8_alt(data):
    return "%12.8f" % data  # pylint: disable=consider-using-f-string


pstats.f8 = f8_alt


def profile_deco(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(wrapper, "profiler"):
            wrapper.profiler = cProfile.Profile()
        wrapper.profiler.enable()
        result = func(*args, **kwargs)
        wrapper.profiler.disable()
        wrapper.print_stat = wrapper.profiler.print_stats
        return result

    return wrapper


@profile_deco
def add(arg_a, arg_b):
    return arg_a + arg_b


@profile_deco
def sub(arg_a, arg_b):
    return arg_a - arg_b


if __name__ == "__main__":

    add(1, 2)
    add(4, 5)
    sub(4, 5)

    add.print_stat()
    sub.print_stat()
