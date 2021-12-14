from typing import Optional, Union

Coords = tuple[int, int]


class CompassDirection:
    def __init__(self, name: str, mask: int, vector: Coords):
        self.__name: str = name
        self.__mask: int = mask
        self.__vector: Coords = vector

    @property
    def name(self) -> str:
        return self.__name

    @property
    def mask(self) -> int:
        return self.__mask

    @property
    def vector(self) -> Coords:
        return self.__vector


class Compass:
    north = CompassDirection(name='North', mask=0b1000, vector=(0, +1))
    south = CompassDirection(name='South', mask=0b0100, vector=(0, -1))
    west = CompassDirection(name='West', mask=0b0010, vector=(-1, 0))
    east = CompassDirection(name='East', mask=0b0001, vector=(+1, 0))
    dirs: list = [north, south, west, east]

    # Map from string representations of each direction to its instance.
    # Lookups are case-insensitive and works for full name or first letter.
    # So for example, these all work: "North", "NORTH", "north", "N", "n".
    # This might be better implemented with collections.Mapping subclass;
    # but dict with overloaded keys is quick-n-easy.
    names: dict = {}
    # names.update([(_d.name, _d) for _d in dirs])
    # names.update([(_d.name[0], _d) for _d in dirs])
    names.update([(_d.name.lower(), _d) for _d in dirs])
    names.update([(_d.name.lower()[0], _d) for _d in dirs])
    # names.update([(_d.name.upper(), _d) for _d in dirs])

    # Map from bitmask representation of each direction to its instance.
    # This might be better implemented with collection.Sequence subclass,
    # but list grokking sparse array is quick-n-easy.
    masks: list = [None] * ((1 << len(dirs)) + 1)
    for _d in dirs:
        masks[_d.mask] = _d

    @staticmethod
    def name2dir(name: str) -> Optional[CompassDirection]:
        """ Lookup direction by name (string).
        :param name: String corresponding to one direction.
        :return: CompassDirection instance, or None.
        """
        name = name.lower()
        out = Compass.names.get(name)
        return out

    @staticmethod
    def mask2dir(mask: int) -> Optional[CompassDirection]:
        """ Lookup direction by bitmask (integer).
        :param mask: Integer mask corresponding to one direction.
        :return: CompassDirection instance, or None.
        """
        if 0 < mask < len(Compass.masks):
            return Compass.masks[mask]
        return None

    @staticmethod
    def dir(val: Union[CompassDirection, str, int]) -> Optional[CompassDirection]:
        """ Lookup direction by bitmask (integer).
        :param val: Value corresponding to one direction.
        :return: CompassDirection instance, or None.
        """
        if isinstance(val, CompassDirection) and val in Compass.dirs:
            return val
        if isinstance(val, int):
            return Compass.mask2dir(val)
        if isinstance(val, str):
            return Compass.name2dir(val)
        raise TypeError(f"Compass.dir() does not accept that type")

    @staticmethod
    def mask2dirs(mask: int) -> list:
        """
        :param mask: Integer mask representing zero to multiple directions.
        :return: List of CompassDirection instances
        """
        out = []
        for _d2 in Compass.dirs:
            if mask & _d2.mask:
                out.append(_d2)
        return out


North = Compass.north
South = Compass.south
West = Compass.west
East = Compass.east


if __name__ == '__main__':
    print(f"Greetings from Compass!")
    for _d in Compass.dirs:
        print(f"{_d.name:6} mask:{_d.mask}/{_d.mask:04b} vector:{_d.vector}")

# END
