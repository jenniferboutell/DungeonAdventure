from room import *


class GridStr:

    def __init__(self, grid, style=RoomStyle):
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

    def __init__(self, width=2, height=2, from_grid=None, from_x=None, from_y=None):
        if from_grid is not None:
            if not isinstance(from_x, int) or not isinstance(from_y, int):
                raise TypeError(f"from_x and from_y must be type int")
        self.__width = width
        self.__height = height
        self.__rooms = []
        for y in range(self.height):
            if from_grid is None:
                row = []
                self.__rooms.append(row)
                for x in range(self.width):
                    r = Room(self, x, y)
                    row.append(r)
            else:
                row = from_grid.rooms[from_y+y][from_x:from_x+width]
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

    def room(self, x, y) -> Room:
        return self.__rooms[y][x]

    def __str__(self) -> str:
        return "".join([f"{row}\n" for row in self.__rooms])

    def __repr__(self) -> str:
        return self.__str__()


if __name__ == '__main__':
    print(f"Greetings from Grid!")

    print(f"\nDefault 2x2 grid...")
    g = Grid()
    print(f"width={g.width} height={g.height}\n{g}")

    print(f"\nParent 4x5 grid, and 2x3 subgrid from (2,1)")
    g1 = Grid(4, 5)
    print(f"g1...\n{g1}")
    g2 = Grid(2, 3, from_grid=g1, from_x=2, from_y=1)
    print(f"g2...\n{g2}")

# END
