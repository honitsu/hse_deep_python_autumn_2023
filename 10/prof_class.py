import weakref


class ParentClass:  # pylint: disable=too-few-public-methods
    def __init__(self, name, child_name, class_name):
        self.name = name
        self.child = class_name(child_name, self)


class PlainClass:  # pylint: disable=too-few-public-methods
    def __init__(self, title, parent):
        self.title = title
        self.loopback = parent


class SlottedClass:  # pylint: disable=too-few-public-methods
    __slots__ = ["title", "loopback"]

    def __init__(self, title, parent):
        self.title = title
        self.loopback = parent


class WeakRefClass:  # pylint: disable=too-few-public-methods
    def __init__(self, title, parent):
        self.title = title
        self.loopback = weakref.ref(parent)
