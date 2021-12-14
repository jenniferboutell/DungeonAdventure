from typing import Any
# import random

from Room import RoomStyle
from Grid import Grid, GridStr


g_dbg_enabled = False


def dbg_print(*args, **kwargs):
    if g_dbg_enabled:
        print(*args, **kwargs)


class Maze(Grid):

    def __init__(self, width: int = 4, height: int = 4, map_str: str = None) -> None:
        if map_str is not None:
            width, height = Maze.parse_map(map_str=map_str)
        super().__init__(width=width, height=height)
        if map_str is not None:
            Maze.parse_map(map_str=map_str, grid=self)
        # Initialization of other fields deferred to separate methods.
        self.__path: list[Any] = []

    @staticmethod
    def parse_map(map_str: str = None, grid=None, style=RoomStyle):
        wall_len: int = len(style.wall_n)
        line_len: int = 0
        in_grid: bool = False
        want_lat: bool = True
        num_cols: int = 0
        num_rows: int = 0
        grid_row: int = 0
        line_num: int = 0  # 1-indexed, unlike everything else
        lines = map_str.splitlines()
        for line in lines:
            line_num += 1
            line = line.rstrip()
            dbg_print(f"L{line_num}: '{line}'")

            # skip header comment/whitespace lines
            if not in_grid and (len(line) == 0 or line.startswith('#')):
                continue
            if not in_grid:
                in_grid = True

                # Initial dimensions assessment, before grid has been created.
                # Do quick math sanity-check, conversion to grid dimensions.
                # Parses only first line of grid, then returns result.
                if grid is None:
                    if len(line) % (wall_len+1) != 1:
                        raise ValueError(f"L{line_num}: expected line len of form {wall_len+1}*N+1, got {len(line)}")
                    num_cols = (len(line)-1)//(wall_len+1)
                    if (len(lines)-line_num) % 2 != 0:
                        raise ValueError(f"expected line count 2*N+1, got {len(lines)-line_num}")
                    num_rows = (len(lines)-line_num)//2
                    dbg_print(f"measured grid dims={num_cols}x{num_rows}")
                    return num_cols, num_rows
                else:
                    num_cols = grid.width
                    num_rows = grid.height
                    line_len = num_cols * (wall_len + 1) + 1
                    dbg_print(f"estimated grid dims={num_cols}x{num_rows} line_len={line_len}")

            dbg_print(f"L{line_num}: length={len(line)}")
            # sanity check, for errant line unexpectedly longer than first line
            if len(line) != line_len:
                raise ValueError(f"L{line_num}: does not match expected len_len {line_len}")
            dbg_print(f"L{line_num}: want_lat={want_lat}")

            # walk the line
            char_num = 0
            grid_col: int = 0
            while char_num < len(line):

                # on a vertical wall, either west side of room OR far-east wall of grid
                dbg_print(f"L{line_num}C{char_num}: grid_col={grid_col}")
                c = line[char_num]
                if want_lat:
                    if c != style.corner:
                        raise ValueError(f"L{line_num}C{char_num}: expected corner '{style.corner}', got '{c}'")
                    dbg_print(f"L{line_num}C{char_num}: corner")
                else:
                    if c != style.wall_w and c != style.door_w:
                        raise ValueError(f"L{line_num}C{char_num}: expected wall '{style.wall_w}'" +
                                         f" or door '{style.door_w}', got '{c}'")
                    dbg_print(f"L{line_num}C{char_num}: wall/door")
                # if last char in line, then completing room from previous round
                if char_num == len(line) - 1:
                    dbg_print(f"L{line_num}C{char_num}: last char in line")
                    break
                char_num += 1

                # between vertical walls
                if want_lat:
                    # horizontal wall/door
                    wall = line[char_num:char_num+wall_len]
                    if wall != style.wall_n and wall != style.door_n:
                        raise ValueError(f"L{line_num}C{char_num}: expected north wall '{style.wall_n}'" +
                                         f" or door '{style.door_n}', but got '{wall}'")
                    dbg_print(f"L{line_num}C{char_num}: wall/door")
                else:
                    # TODO interpret contents?
                    # contents = line[char_num:char_num+wall_len]
                    dbg_print(f"L{line_num}C{char_num}: contents")
                    pass
                char_num += wall_len
                grid_col += 1
                dbg_print(f"L{line_num}C{char_num}: next grid_col={grid_col} if any")

            dbg_print(f"prep for next line...")

            # if last line, then completing room on bottom row
            if line_num == len(lines):
                dbg_print(f"last line, assume solid (no doors) wall")
                break

            # increment in preparation for next row
            grid_row += 1
            want_lat = not want_lat
            dbg_print(f"grid_row={grid_row} want_lat={want_lat}")


if __name__ == '__main__':
    print("Greetings from Maze!\n")

    # Default 4x4 grid, no doors yet
    m = Maze()
    print(f"default maze is {m.width}x{m.height}:")
    print(m)

    # Measure canned
    print(f"canned dungeon:")
    g_map_str = """
# This is my dungeon
+-----+-----+-----+
| E   |     =     |
+--H--+--H--+--H--+
|     =     | O   |
+-----+-----+-----+
""".lstrip()
    print(g_map_str)
    g_width, g_height = Maze.parse_map(g_map_str)
    print("measure-only estimates as {g_width}x{g_height}\n")

    # Full init from canned maze
    print(f"another canned dungeon:")
    g_map_str = """
# This is my other dungeon
+-----+-----+-----+
| E   |     = O   |
+--H--+--H--+-----+
|     =     =     |
+-----+-----+-----+
""".lstrip()
    print(g_map_str)
    print(f"...now do full load...")
    m = Maze(map_str=g_map_str)
    print(f"...reports dimensions {m.width}x{m.height}")
    print(f"...and re-render:")
    print(f"{m}")

# END
