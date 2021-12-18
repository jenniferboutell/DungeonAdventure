from Room import Room
from Grid import Grid
from Maze import Maze


class Dungeon(Maze):
    """
    TODO docs
    """

    def __init__(self, *args, **kwargs):
        """
        TODO docs
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

        # TODO confirm has Entrance and Exit; either imported map
        # or Maze.generate() should have taken care to include those.

        # TODO check for pillars, add ANY that are missing

        # TODO check for other items, add if NONE are present


if __name__ == '__main__':
    print("Greetings from Dungeon!\n")

    print("randomly generated:")
    Grid.set_style_default(Room.styles.open)
    g_d = Dungeon()
    print(f"{g_d}")

# END
