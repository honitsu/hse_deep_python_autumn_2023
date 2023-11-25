import re


class CustomMeta(type):
    def __new__(cls, name, bases, dct, **kwargs):
        def _setattr_(self, name, value):
            custom_name = "custom_" + name
            object.__setattr__(self, custom_name, value)

        new_dct = {}

        pattern = re.compile(r"(^__([A-Za-z_0-9]*)__$)")
        for method in dct:
            if pattern.match(method):
                new_dct[method] = dct[method]
            else:
                custom_method = "custom_" + method
                new_dct[custom_method] = dct[method]

        new_dct["__setattr__"] = _setattr_
        return super().__new__(cls, name, bases, new_dct, **kwargs)

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)

    @classmethod
    def __prepare__(cls, *args, **extra_kwargs):
        return super().__prepare__(cls, *args, **extra_kwargs)
