import random
from Compass import *

Coords = tuple[int, int]


class RoomStyleBase:
    def __init__(self, corner: str = "+",
                 wall_n: str = "-----", wall_s: str = None,
                 door_n: str = "--H--", door_s: str = None,
                 wall_w: str = "|", wall_e: str = None,
                 door_w: str = "=", door_e: str = None,
                 coords: bool = False):
        self.corner = corner
        # N/S walls
        self.wall_n = wall_n
        if wall_s:
            self.wall_s = wall_s
        else:
            self.wall_s = self.wall_n
        # N/S doors
        self.door_n = door_n
        if door_s:
            self.door_s = door_s
        else:
            self.door_s = self.door_n
        # W/E walls
        self.wall_w = wall_w
        if wall_e:
            self.wall_e = wall_e
        else:
            self.wall_e = self.wall_w
        # W/E doors
        self.door_w = door_w
        if door_e:
            self.door_e = door_e
        else:
            self.door_e = self.door_w
        # Show coords instead of contents
        self.coords = coords


RoomStyleDefault = RoomStyleBase()

RoomStyle = RoomStyleDefault

RoomStyleOpen = RoomStyleBase(door_n="     ", door_w=" ")

RoomStyleCoords = RoomStyleBase(coords=True)

RoomStyleTom = RoomStyleBase(corner="*",
                             wall_n="*****", wall_w="*",
                             door_n=" --- ", door_w="|")


class RoomStyles:
    base = RoomStyle
    default = RoomStyleDefault
    open = RoomStyleOpen
    coords = RoomStyleCoords
    tom = RoomStyleTom


class RoomStr:
    """
    Builds a ASCII-text representation of room.
    Boundaries are single char wide, with wall and door represented differently.
    In cCenter, single char that represents what the room contains.
    M - Multiple Items
    X - Pit
    i - Entrance (In)
    O - Exit (Out)
    V - Vision Potion
    H - Healing Potion
    <space> - Empty Room
    A, E, I, P - Pillars

    Example:  Room 1,1 might look like
    *-*
    |P|
    *-*
    """

    def __init__(self, _room, skip_north=None, skip_west=None, style=RoomStyleDefault):
        self.room = _room
        self.lines = []
        skip_north = bool(skip_north)
        skip_west = bool(skip_west)

        # top
        if not skip_north:
            line = ""
            if not skip_west:
                line += style.corner
            if _room.has_door(North):
                line += style.door_n
            else:
                line += style.wall_n
            line += style.corner
            self.lines.append(line)

        # west/middle/east
        line = ""
        if not skip_west:
            if _room.has_door(West):
                line += style.door_w
            else:
                line += style.wall_w
        if style.coords:
            r = self.room_coords()
        else:
            r = self.room_contents()
        line += f" {r:<3} "
        if _room.has_door(East):
            line += style.door_e
        else:
            line += style.wall_e
        self.lines.append(line)

        # bottom
        line = ""
        if not skip_west:
            line += style.corner
        if _room.has_door(South):
            line += style.door_s
        else:
            line += style.wall_s
        line += style.corner
        self.lines.append(line)

    # reporting only coords, rather than contents, is useful for testing
    def room_coords(self) -> str:
        _r = self.room
        if _r.coords is not None:
            return f"{_r.coord_x},{_r.coord_y}"
        else:
            return "#,#"

    def room_contents(self) -> str:
        _r = self.room
        if _r.has_mixed_contents:
            return 'M'
        elif _r.is_entrance:
            return 'i'
        elif _r.is_exit:
            return 'O'
        elif _r.has_pit:
            return 'X'
        elif _r.vision_potions:
            return 'V'
        elif _r.healing_potions:
            return 'H'
        elif _r.pillar:
            return _r.pillar
        else:
            return ' '

    def __str__(self):
        return "".join([f"{line}\n" for line in self.lines])


class Room:
    styles = RoomStyles

    """
    - (0/1) Entrance - only one room is an entrance, and that room contains NOTHING else
    - (0/1) Exit - only one room is an exit, and that room contains NOTHING else
    - (0/1) Pillar of OO - one of four unique Pillars of Object Oriented Programming
    - (0-4) Doors - N, S, E, W
    - 10% possibility (constant, but can modify) any item-bearing room will contain
      a healing potion, vision potion, or pit -- independent of one another
    - (0+) Vision Potion - can be used to allow user to see eight rooms surrounding
      current room as well as current room (if on maze edge, less than 8)

    - __str__() that builds an ASCII-art representation of the room; see RoomStr.
    """

    def __init__(self, grid=None, coords: Coords = None,
                 is_entrance: bool = False,
                 is_exit: bool = False,
                 doors_mask: int = 0,
                 doors_list: list = None,
                 has_pit: bool = False,
                 healing_potions: int = 0,
                 vision_potions: int = 0,
                 pillar: str = None) -> None:
        self.__grid = grid
        self.__coords: Coords = coords
        self.__is_entrance: bool = is_entrance
        self.__is_exit: bool = is_exit
        self.__has_pit: bool = has_pit
        self.__healing_potions: int = healing_potions
        self.__vision_potions: int = vision_potions
        self.__pillar: str = pillar
        self.__doors_mask: int = 0
        if doors_mask and doors_list:
            raise ValueError("init Room with doors_mask or doors_list, not both")
        elif doors_list and not doors_mask:
            self.__doors_mask = Compass.dirs2mask(doors_list)
        else:
            self.__doors_mask = doors_mask

    @property
    def grid(self):
        return self.__grid

    @property
    def coords(self) -> Optional[Coords]:
        """ Get coordinates of room within grid, assuming part of one.
            Returned value is a tuple of ints (x,y) in a Cartesian system.
            x-coord runs West-to-East (rightward), most Westward column at x=0.
            x-coord runs North-to-South (downward), most Northward row at y=0. """
        return self.__coords

    @property
    def coord_x(self) -> Optional[int]:
        if self.coords is not None:
            return self.coords[0]
        return None

    @property
    def coord_y(self) -> Optional[int]:
        if self.coords is not None:
            return self.coords[1]
        return None

    @coords.setter
    def coords(self, coords: Coords) -> None:
        """ Set coordinates of room within grid, assuming part of one.
            Same tuple format as returned by getter. """
        if not isinstance(coords, tuple) or len(coords) != 2 or \
                not isinstance(coords[0], int) or \
                not isinstance(coords[1], int):
            raise TypeError(f"expected coords to be tuple of two ints")
        if coords[0] < 0 or coords[1] < 0:
            raise ValueError(f"expected coords to both be zero or greater")
        g = self.grid
        if g is not None and (coords[0] >= g.width or coords[1] >= g.height):
            raise ValueError(f"expected coords within grid bounds ({g.width}x{g.height})")
        self.__coords = coords

    def neighbor(self, direction):
        """ Get neighboring room in specified direction from self room.
        :param direction: Direction of neighboring room wrt self room.
        :return: Neighboring room, if there is one; otherwise None.

        Exception only raised for direction; attempting to fetch a hypothetical
        neighbor that would lie outside the grid returns None.
        """
        _dir = Compass.dir(direction)
        if _dir is None:
            raise ValueError(f"neighbor got invalid direction {direction}")
        _grid = self.grid
        if _grid is None:
            return None
        x = self.coord_x + _dir.vect_x
        y = self.coord_y + _dir.vect_y
        if not 0 <= x < _grid.width or not 0 <= y < _grid.height:
            # print(f"neighbor: room({self.coords}) {_dir.name} -!- ({x},{y}) outside grid")
            return None
        # print(f"neighbor: room({self.coords}) {_dir.name} --> ({x},{y})")
        return _grid.room(x, y)

    @property
    def doors_mask(self) -> int:
        return self.__doors_mask

    # TODO merge doors setters into single method that accepts all formats
    @doors_mask.setter
    def doors_mask(self, doors_mask: int) -> None:
        self.__doors_mask = doors_mask

    @property
    def doors(self) -> list:
        return Compass.mask2dirs(self.__doors_mask)

    # @doors.setter
    # def doors(self, doors_list: list) -> None:
    #     self.__doors_mask = # TODO

    @property
    def doors_str(self) -> str:
        return ','.join([d.name[0] for d in self.doors])

    # @doors_str.setter
    # def doors_str(self, doors_str: str) -> None:
    #     self.__doors_mask = # TODO

    def has_door(self, direction) -> bool:
        return bool(self.__doors_mask & Compass.dir(direction).mask)

    def add_door(self, direction) -> None:
        """ Add a door in specified direction from self room, and likewise
        from corresponding neighboring room, if one exists in that direction.

        Since doors are represented within rooms via bitmask, rather than
        a ref to neighboring room; thus when a door connects two rooms,
        each room must have that door marked in its respective bitmask.

        Allowed to add a door that leads outside the grid, i.e. no neighboring
        room exists in that direction; though depending upon the context,
        perhaps not what you want.

        :param direction: Outward direction from room
        :return None
        :exception ValueError if direction is not recognized
        """
        _d = Compass.dir(direction)
        # print(f"add_door: > room({self.coords}) {_d.name}")
        self.__doors_mask |= _d.mask
        _r = self.neighbor(direction)
        if _r is not None:
            _d = _d.opposite
            # print(f"add_door: < room({_r.coords}) {_d.name}")
            _r.doors_mask |= _d.mask

    def del_door(self, direction) -> None:
        """ Remove door (if any) in specified direction from self room, and likewise
        from corresponding neighboring room, if one exists in that direction.
        Exact opposite of add_door().

        :param direction: Outward direction from room
        :return None
        :exception ValueError if direction is not recognized
        """
        _d = Compass.dir(direction)
        # print(f"del_door: > room({self.coords}) {_d.name}")
        self.__doors_mask &= ~_d.mask
        _r = self.neighbor(direction)
        if _r is not None:
            _d = _d.opposite
            # print(f"del_door: < room({_r.coords}) {_d.name}")
            _r.doors_mask &= ~_d.mask

    def add_wall(self, direction) -> None:
        self.del_door(direction)

    def del_wall(self, direction) -> None:
        self.add_door(direction)

    @property
    def is_entrance(self) -> bool:
        return self.__is_entrance

    @is_entrance.setter
    def is_entrance(self, val: bool) -> None:
        self.__is_entrance = val

    @property
    def is_exit(self) -> bool:
        return self.__is_exit

    @is_exit.setter
    def is_exit(self, val: bool) -> None:
        self.__is_exit = val

    @property
    def has_pit(self) -> bool:
        return self.__has_pit

    @has_pit.setter
    def has_pit(self, val: bool) -> None:
        self.__has_pit = val

    @property
    def healing_potions(self) -> int:
        return self.__healing_potions

    @healing_potions.setter
    def healing_potions(self, val: int) -> None:
        self.__healing_potions = val

    @property
    def vision_potions(self) -> int:
        return self.__vision_potions

    @vision_potions.setter
    def vision_potions(self, val: int) -> None:
        self.__vision_potions = val

    @property
    def pillar(self) -> str:
        return self.__pillar

    @pillar.setter
    def pillar(self, val: str) -> None:
        self.__pillar = val

    def set_room(self, percent: int = 10):
        # FIXME probably get rid of this; randomized contents are hard to test.
        # Maze load_map() is almost always what you should be using instead.
        self.has_pit = random.randrange(100) < percent
        self.healing_potions = random.randrange(100) < percent
        self.vision_potions = random.randrange(100) < percent
        # self.pillar = "I"  # FIXME Dungeon should place Pillars, not Room

    @property
    def has_mixed_contents(self) -> bool:
        count: int = 0
        if self.vision_potions > 0:
            count += 1
        if self.healing_potions > 0:
            count += 1
        if self.has_pit:
            count += 1
        if self.pillar is not None:
            count += 1
        return count > 1

    def describe(self):
        return '\n'.join([
            f"Coords:  {self.coords}",
            f"Doors:   {self.doors_str}",
            f"Pit:     {self.has_pit}",
            f"Healing: {self.healing_potions}",
            f"Vision:  {self.vision_potions}",
            f"Pillar:  {self.pillar}",
        ])

    def str(self, *args, **kwargs) -> str:
        return str(RoomStr(self, *args, **kwargs))

    def __str__(self) -> str:
        return self.str()

    def __repr__(self) -> str:
        return RoomStr(self).room_coords()


if __name__ == '__main__':
    print(f"Greetings from Room!\n")

    print(f"standalone room, empty and sealed:")
    g_r = Room()
    print(f"{g_r}")
    print(f"...with coords-style contents, but hey no coords:")
    print(f"{g_r.str(style=Room.styles.coords)}")

    print(f"grid room, empty and sealed:")
    g_r = Room(coords=(2, 3))
    print(f"{g_r}")
    print(f"...with coords-style contents:")
    print(f"{g_r.str(style=Room.styles.coords)}")

    print(f"room with doors and a potion:")
    g_r.add_door('N')
    g_r.add_door('west')
    g_r.healing_potions += 2
    print(f"{g_r}")
    print(f"...description thereof:")
    print(g_r.describe())
    print("...rendered with 'open' style doors:")
    print(f"{g_r.str(style=Room.styles.open)}")
    print("...rendered with Tom's janky style:")
    print(f"{g_r.str(style=Room.styles.tom)}")

# END
