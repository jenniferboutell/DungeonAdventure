from typing import Protocol


class CompassDirection(Protocol):
    mask: int = 0
    vector: tuple = (0, 0)

    @classmethod
    @property
    def name(cls):  # ignore PyCharm warning, does not grok classmethod + property
        return cls.__name__.upper()


class North(CompassDirection):
    mask: int = 0b1000
    vector: tuple = (0, +1)


class South(CompassDirection):
    mask: int = 0b0100
    vector: tuple = (0, -1)


class West(CompassDirection):
    mask: int = 0b0010
    vector: tuple = (-1, 0)


class East(CompassDirection):
    mask: int = 0b0001
    vector: tuple = (+1, 0)


class Compass:
    dirs: list = [North, South, West, East]

    # Map from string representations of each direction to its instance.
    # Multiple representations accepted, e.g.: "North", "N", "north", "n".
    # This might be better implemented with collections.Mapping subclass;
    # but dict with overloaded keys is quick-n-easy.
    names: dict = dict([(_d.__name__, _d) for _d in dirs])
    names.update([(_d.__name__[0], _d) for _d in dirs])
    names.update([(_d.__name__.lower(), _d) for _d in dirs])
    names.update([(_d.__name__.lower()[0], _d) for _d in dirs])
    names.update([(_d.__name__.upper(), _d) for _d in dirs])

    # Map from bitmask representation of each direction to its instance.
    # This might be better implemented with collection.Sequence subclass,
    # but list grokking sparse array is quick-n-easy.
    masks: list = [None] * ((1 << len(dirs)) + 1)
    for _d in dirs:
        masks[_d.mask] = _d

    @staticmethod
    def mask2dirs(mask: int) -> list:
        out = []
        for _d2 in Compass.dirs:
            if mask & _d2.mask:
                out.append(_d2)
        return out

    @staticmethod
    def name2dir(name: str) -> CompassDirection:
        name = name.lower()
        out = Compass.names.get(name)
        return out

    @staticmethod
    def name2mask(name: str) -> int:
        name = name.lower()
        out = Compass.names.get(name)
        if out is not None:
            out = out.mask
        return out


if __name__ == '__main__':
    print(f"Greetings from Compass!")
    for _d in [North, South, West, East]:
        print(f"{_d.__name__:6} name:{_d.name:6} mask:{_d.mask}/{_d.mask:04b} vector:{_d.vector}")

# END
