class Rating:
    def __init__(self):
        self.name = ""

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, 0.0)

    def __set__(self, instance, value):
        if isinstance(value, bool) or not isinstance(value, (float, int)):
            raise TypeError("The value of rating should be a number")

        if not 0 <= value <= 10:
            raise ValueError("The value of rating must be in interval [0;10]")

        instance.__dict__[self.name] = round(float(value), 1)


class Director:  # pylint: disable=too-few-public-methods
    def __init__(self):
        self.name = ""

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError("Name of the director must be a string")

        allowed_chars = " '.,"
        if not (
            value.translate(str.maketrans("", "", allowed_chars)).isalpha()
            and value.istitle()
        ):
            raise ValueError(
                "Director's name must start with capital letter"
                "and consist of alphabetic characters "
            )
        instance.__dict__[self.name] = value


class Actors:
    def __init__(self):
        self.name = ""

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, [])

    def __set__(self, instance, value):
        if not isinstance(value, list):
            raise TypeError("Actors must be a list")
        for name in value:
            if not isinstance(name, str):
                raise TypeError("All actors' names must be strings")
            allowed_chars = " '.,"
            if (
                not name.translate(
                    str.maketrans("", "", allowed_chars)
                ).isalpha()
                or not name.istitle()
            ):
                raise ValueError(
                    "All actors' names must consist of "
                    "alphabetic characters and start "
                    "with a capital letter"
                )
        instance.__dict__[self.name] = value
