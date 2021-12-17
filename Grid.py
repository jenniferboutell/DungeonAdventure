from Room import *

Coords = tuple[int, int]


class GridStr:
    __style_default = Room.styles.default

    @classmethod
    def set_style_default(cls, style: RoomStyleBase):
        cls.__style_default = style

    def __init__(self, grid, style=None):
        self.style = self.__style_default
        if style is not None:
            self.style = style
        style = self.style  # just shorter to type
        self.lines = []
        for y in range(grid.height):
            # When starting new row, initialize each of row_lines to "".
            # But defer initialization until processing first room in row,
            # from which will then know how many lines.
            row_lines = []
            for x in range(grid.width):
                r = grid.room(x, y)
                rs = RoomStr(r, skip_north=y, skip_west=x, style=style)
                room_lines = rs.lines
                for i in range(len(room_lines)):
                    # New row, so initialize each of row_lines.
                    if len(row_lines) == i:
                        row_lines.append('')
                    row_lines[i] += room_lines[i]
            self.lines += row_lines

    def __str__(self):
        return "".join([f"{line}\n" for line in self.lines])


class Grid:

    @staticmethod
    def set_style_default(style):
        GridStr.set_style_default(style=style)

    def __init__(self, width=2, height=2, from_grid=None, from_coords: Coords = None):
        if from_coords is not None:
            if not isinstance(from_coords[0], int) or not isinstance(from_coords[1], int):
                raise TypeError(f"from_coords must be tuple of int pair")
        self.__width = width
        self.__height = height
        self.__rooms = []
        for y in range(self.height):
            if from_grid is None:
                row = []
                self.__rooms.append(row)
                for x in range(self.width):
                    r = Room(grid=self, coords=(x, y))
                    row.append(r)
            else:
                from_x = from_coords[0]
                from_y = from_coords[1]
                row = from_grid.rooms[from_y + y][from_x:from_x + width]
                self.__rooms.append(row)

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def rooms(self) -> list:
        return self.__rooms

    def room(self, x: int, y: int) -> Room:
        # If coords are out-of-bounds, just let resulting IndexError bubble up
        return self.__rooms[y][x]

    def str(self, *args, **kwargs) -> str:
        return str(GridStr(self, *args, **kwargs))

    def __str__(self) -> str:
        return self.str()

    def __repr__(self) -> str:
        return "".join([f"{row}\n" for row in self.__rooms])

    def empty(self):
        for y in range(self.height):
            for x in range(self.width):
                r = self.room(x, y)
                if y > 0:
                    r.add_door(North)
                if y + 1 < self.height:
                    r.add_door(South)
                if x > 0:
                    r.add_door(West)
                if x + 1 < self.width:
                    r.add_door(East)


if __name__ == '__main__':
    print(f"Greetings from Grid!\n")

    g = Grid()
    print(f"default grid is {g.width}x{g.height}:")
    print(f"{g}")

    GridStr.set_style_default(Room.styles.coords)
    g_w = 4
    g_h = 5
    print(f"parent {g_w}x{g_h} grid:")
    g1 = Grid(g_w, g_h)
    print(f"{g1}")
    g_w = 2
    g_h = 3
    g_x = 2
    g_y = 1
    print(f"...and {g_w}x{g_h} subgrid with origin at parent coords ({g_x},{g_y})")
    g2 = Grid(g_w, g_h, from_grid=g1, from_coords=(g_x, g_y))
    print(f"{g2}")

    print("...and empty parent interior")
    g1.empty()
    print(f"{g1}")
    print("...and render with open-door style")
    print(f"{g1.str(style=Room.styles.open)}")

# END
