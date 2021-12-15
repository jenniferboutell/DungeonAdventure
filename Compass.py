from typing import Optional, Union

Coords = tuple[int, int]


class CompassDirection:
    def __init__(self, name: str, mask: int, vector: Coords, abbr: str = None):
        self.__name: str = name.capitalize()
        self.__abbr: str = self.name[0]
        if abbr is not None:
            self.__abbr = abbr.upper()
        self.__mask: int = mask
        self.__vector: Coords = vector

    def diag(self, dir2):
        if self.mask & ~self.mask != 0 or dir2.mask & ~dir2.mask != 0:
            raise ValueError(f"can only create diagonal direction from two perpendicular directions")
        return CompassDirection(name=self.name + dir2.name,
                                abbr=self.abbr + dir2.abbr,
                                mask=self.mask | dir2.mask,
                                vector=(self.vector[0] + dir2.vector[0], self.vector[1] + dir2.vector[1]))

    @property
    def name(self) -> str:
        return self.__name

    @property
    def abbr(self) -> str:
        return self.__abbr

    @property
    def mask(self) -> int:
        return self.__mask

    @property
    def vector(self) -> Coords:
        return self.__vector

    @property
    def vect_x(self) -> int:
        return self.__vector[0]

    @property
    def vect_y(self) -> int:
        return self.__vector[1]


class Compass:
    north = CompassDirection(name='North', mask=0b1000, vector=(0, -1))
    south = CompassDirection(name='South', mask=0b0100, vector=(0, +1))
    west = CompassDirection(name='West', mask=0b0010, vector=(-1, 0))
    east = CompassDirection(name='East', mask=0b0001, vector=(+1, 0))
    dirs: list = [north, south, west, east]

    northwest = north.diag(west)
    southwest = south.diag(west)
    northeast = north.diag(east)
    southeast = south.diag(east)
    diags: list = [northwest, southwest, northeast, southeast]

    # Map from string representations of each direction to its instance.
    # Lookups are case-insensitive and works for full name or first letter.
    # So for example, these all work: "North", "NORTH", "north", "N", "n".
    # This might be better implemented with collections.Mapping subclass;
    # but dict with overloaded keys is quick-n-easy.
    names: dict = {}
    names.update([(_d.name.lower(), _d) for _d in dirs])
    names.update([(_d.name.lower()[0], _d) for _d in dirs])
    # If lookup always lower-cases target first -- which dir() does --
    # then don't need to add dict keys for any other case combinations.
    # names.update([(_d.name, _d) for _d in dirs])
    # names.update([(_d.name[0], _d) for _d in dirs])
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
    def dirs2mask(dirs: list) -> int:
        """
        :param dirs: List of zero or more CompassDirection instances or string names
        :return: Integer mask representing zero to multiple directions
        """
        out = 0
        for _d in dirs:
            out |= Compass.dir(_d).mask
        return out

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

    print(f"\nPrimary directions:")
    for _d in Compass.dirs:
        print(f"name:{_d.name:6} abbr:{_d.abbr} mask:{_d.mask}/{_d.mask:04b} vector:{_d.vector}")

    print(f"\nDiagonal directions:")
    for _d in Compass.diags:
        print(f"name:{_d.name} abbr:{_d.abbr} mask:{_d.mask}/{_d.mask:04b} vector:{_d.vector}")

# END
