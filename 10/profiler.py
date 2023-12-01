# Запустите скрипт с аргументом PROFILE,
# чтобы просмотреть данные cProfile

import cProfile
import io
import pstats
import sys
import time
import weakref


class SubClass:  # pylint: disable=too-few-public-methods
    def __init__(self, name):
        self.name = name


class PlainClass:  # pylint: disable=too-few-public-methods
    def __init__(self, title, subcl):
        self.title = title
        self.loopback = subcl


class SlottedClass:  # pylint: disable=too-few-public-methods
    __slots__ = ["title", "loopback"]

    def __init__(self, title, subcl):
        self.title = title
        self.loopback = subcl


class WeakRefClass:  # pylint: disable=too-few-public-methods
    def __init__(self, title, subcl):
        self.title = title
        self.loopback = weakref.ref(subcl)

#@profile # для профилирования памяти
def create_plain(total_run):
    return [PlainClass(f"Parent{_}", subclass) for _ in range(total_run)]


#@profile # для профилирования памяти
def create_slotted(total_run):
    return [SlottedClass(f"Parent{_}", subclass) for _ in range(total_run)]


#@profile # для профилирования памяти
def create_weakref(total_run):
    return [WeakRefClass(f"Parent{_}", subclass) for _ in range(total_run)]


#@profile # для профилирования памяти
def create_timing(total_run, subcl):
    start_time = time.time()
    plain_child = create_plain(total_run)
    plain_time = time.time() - start_time

    start_time = time.time()
    slotted_child = create_slotted(total_run)
    slotted_time = time.time() - start_time

    start_time = time.time()
    weakref_child = create_weakref(total_run)
    weakref_time = time.time() - start_time

    print(f"Число повторов: {N}")
    print("Класс                    Время создания")
    print("---------------------------------------")
    print(f"С обычными атрибутами    {plain_time:.6f}")
    print(f"Со слотами               {slotted_time:.6f}")
    print(f"С атрибутами weakref     {weakref_time:.6f}\n\n")
    return plain_child, slotted_child, weakref_child


#@profile # для профилирования памяти
def read_edit_timing(num_to_run):
    # замер времени доступа и чтения атрибутов для каждого экземпляра
    start_time = time.time()
    for parent in plain_child:
        getattr(parent.loopback, "name")
    plain_read = time.time() - start_time

    start_time = time.time()
    for parent in plain_child:
        setattr(parent.loopback, "name", "New name pln")
    plain_edit = time.time() - start_time

    start_time = time.time()
    for parent in slotted_child:
        getattr(parent.loopback, "name")
    slotted_read = time.time() - start_time

    start_time = time.time()
    for parent in slotted_child:
        setattr(parent.loopback, "name", "New name slt")
    slotted_edit = time.time() - start_time

    start_time = time.time()
    for parent in weakref_child:
        getattr(parent.loopback(), "name")
    weakref_read = time.time() - start_time

    start_time = time.time()
    for parent in weakref_child:
        setattr(parent.loopback(), "name", "New name wkr")
    weakref_edit = time.time() - start_time

    print(f"Число повторов: {num_to_run}")
    print("Класс                     Чтение        Изменение")
    print("-------------------------------------------------")
    print(f"С обычными атрибутами     {plain_read:.6f}      {plain_edit:.6f}")
    print(f"Со слотами                {slotted_read:.6f}      {slotted_edit:.6f}")
    print(f"С атрибутами weakref      {weakref_read:.6f}      {weakref_edit:.6f}\n\n")


if __name__ == "__main__":
    PROFILE = False
    if len(sys.argv) > 1:
        for x in sys.argv:
            if x == "PROFILE":
                PROFILE = True
    N = 200000

    subclass = SubClass("num_to_run")
    if PROFILE:
        pr = cProfile.Profile()
        pr.enable()
    plain_child, slotted_child, weakref_child = create_timing(N, subclass)
    if PROFILE:
        pr.disable()
        st = io.StringIO()
        ps = pstats.Stats(pr, stream=st).sort_stats("cumulative")
        ps.print_stats()
        print(st.getvalue())

    if PROFILE:
        pr2 = cProfile.Profile()
        pr2.enable()
    read_edit_timing(N)
    if PROFILE:
        pr2.disable()
        st2 = io.StringIO()
        ps2 = pstats.Stats(pr2, stream=st2).sort_stats("cumulative")
        ps2.print_stats()
        print(st2.getvalue())
