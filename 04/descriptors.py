class Integer:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        instance.__dict__[self.name] = value

    def __init__(self, name):
        self.name = name


class String:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError("Value must be a string")
        instance.__dict__[self.name] = value

    def __init__(self, name):
        self.name = name


class PositiveInteger:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Value must be a positive integer")
        instance.__dict__[self.name] = value

    def __init__(self, name):
        self.name = name
