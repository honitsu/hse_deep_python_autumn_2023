# custom_meta.py

import re


class CustomMeta(type):
    def __new__(cls, name, bases, dct, **kwargs):
        _pattern = re.compile(r"(^__([A-Za-z_\d]*)__$)")

        def __setattr__(self, name, value):
            if not _pattern.match(name):
                custom_name = "custom_" + name
            else:
                custom_name = name
            object.__setattr__(self, custom_name, value)

        new_dct = {}

        for method in dct:
            if not _pattern.match(method):
                custom_method = "custom_" + method
                new_dct[custom_method] = dct[method]
            else:
                new_dct[method] = dct[method]

        new_dct["__setattr__"] = __setattr__
        return super().__new__(cls, name, bases, new_dct, **kwargs)
