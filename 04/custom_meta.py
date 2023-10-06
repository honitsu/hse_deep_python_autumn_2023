class CustomMeta(type):
    @staticmethod
    def keyname(key) -> str:
        if not key.startswith("__") and not key.endswith("__"):
            key = "custom_" + key
        return key

    def _new_setattr(cls, key, value):
        cls.__class__.__base__.__setattr__(cls, CustomMeta.keyname(key), value)

    def __new__(cls, name, bases, dct):
        new_dct = {}
        for key in dct:
            new_dct[CustomMeta.keyname(key)] = dct[key]
        new_dct["__setattr__"] = cls._new_setattr
        return super().__new__(cls, name, bases, new_dct)

    def __setattr__(cls, key, value):
        super().__setattr__(CustomMeta.keyname(key), value)
