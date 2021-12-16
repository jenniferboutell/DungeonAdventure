from Compass import Compass, CompassDirection
from Room import Room
from Maze import Maze
from Adventurer import Adventurer
# from random import randrange


class DungeonAdventure:

    def __init__(self, map_str: str = None):
        self.__hero = Adventurer(self)
        self.__maze = Maze(map_str=map_str)
        self.__room = self.__maze.room(0, 0)
        self.__continues: bool = True

    @property
    def hero(self) -> Adventurer:
        return self.__hero

    @hero.setter
    def hero(self, hero: Adventurer) -> None:
        self.__hero = hero

    @property
    def name(self) -> str:
        """ Name of Adventurer.
        Not actually a property of DungeonAdventure class itself.
        But used so often in dialogue, covenient to shorten the path to it.
        Only set once though, so corresponding setter not really warranted.
        """
        return self.hero.name

    @property
    def maze(self) -> Maze:
        return self.__maze

    @maze.setter
    def maze(self, maze: Maze) -> None:
        self.__maze = maze

    @property
    def room(self) -> Room:
        return self.__room

    @room.setter
    def room(self, room: Room) -> None:
        self.__room = room

    @property
    def continues(self) -> bool:
        # TODO check for other failing conditions? e.g. hero.hit_points <= 0
        return self.__continues

    @continues.setter
    def continues(self, tallyho: bool) -> None:
        self.__continues = tallyho

    def prelude(self):
        # intro gag, no actual effect
        option = input("Shall we play a game? (Y/N)\n")
        if option.upper() in ("N", 'NO'):
            print("Commence global thermonuclear war in 3... 2... 1...")
            print(".....haha, not really! That is scheduled for tomorrow.")
            print()
        # actual preamble
        print("Huzzah! Welcome to Dungeon Adventure!")
        name = input("What is your name, brave adventurer?\n")
        # FIXME basic validation of name
        # TODO strip() surrounding whitespace
        self.hero.name = name
        self.menu()
        # self.prompt()

    def finish(self):
        print(f"Brave Sir {self.name} is at The End.")
        # TODO report what kind of ending
        # TODO sys.exit() ...?

    @staticmethod
    def menu():
        print("\n".join(["Here are your options...",
                         "- Show (I)nventory or (M)ap",
                         "- Move (N)orth, (S)outh, (E)ast, or (W)est",
                         "- Use (V)ision Potion or (H)ealing Potion",
                         "- (Q)uit game in disgust",
                         "- (?) show these options again"]))
        # Do NOT reveal the hidden options:
        # (*) show full map, (@) describe current room

    def prompt(self):
        print()  # empty line to visually separate from preceding stanza
        option = input(f"What would you like to do, brave Sir {self.name}?\n")

        def match(got: str, *wants) -> bool:
            for want in wants:
                if got.lower() == want.lower():
                    return True
            return False

        if option == '?':
            self.menu()

        elif match(option, 'Q', 'quit'):
            print("Discretion is the better part of valor.")
            print(f"Three cheers for brave Sir {self.name}!")
            self.continues = False

        elif match(option, 'I', 'inventory'):
            print("Thine Bag of Holding doth weigh upon you most ponderously...")
            self.__hero.display_inventory()

        elif match(option, 'M', 'map'):
            print("Drat. Your map appears to have smeared and is now unreadable.")
            # TODO show map of visited/seen rooms

        elif match(option, '@', 'describe'):
            # Hidden option! Describe current room
            print("There is something about this room...")
            print(str(self.room.describe()))

        elif match(option, '*', 'joshua'):
            # Hidden option! Print full maze
            if match(option, 'joshua'):
                print("A strange game. The only winning move is not to play...")
            else:
                print("There is a sharp pain behind your eyes, then all is revealed...")
            print(str(self.maze))

        elif match(option, 'H', 'healing', 'health'):
            print("You guzzle down the sweet, sweet elixir or life.")
            self.__hero.use_healing_potion()

        elif match(option, 'V', 'vision'):
            print("You swig the crystal clear fluid, gasp, then stare in amazement...")
            self.__hero.use_vision_potion()
            # TODO: finish use_vision_potion method in Adventurer
            # TODO fetch 3x3 subgrid centered at current room, and display

        elif Compass.dir(option):
            _dir: CompassDirection = Compass.dir(option)
            # Try going that direction
            # TODO was this supposed to go into self.hero.move(_dir)...?
            # If so, move() returns False if cannot traverse that direction.
            next_room = self.__room.neighbor(option)
            if next_room is None:
                print(f"You take a step to the {_dir.name}... but are thwarted.")
                print(f"Brave Sir {self.name} didst stare defiantly at his shoes.")
                return
            print(f"You bound jauntily to the {_dir.name}...")
            print(next_room)
            self.room = next_room
            # self.room.set_room()  # FIXME nope, rely on loaded map!
            if self.room.healing_potions:
                self.find_healing_potion()
            if self.room.vision_potions:
                self.find_vision_potion()
            if self.room.has_pit:
                self.fall_into_pit()
            if self.hero.hit_points <= 0:
                self.continues = False
            if self.room.is_exit:
                self.find_exit()  # TODO: add pillar logic

        else:
            print()  # empty line for visual separation
            print("These words that you are using...")
            print("I do not think they mean what you think they mean.")
            print("Perhaps your response should be in the form of a '?'...")
            # no-op

    def play(self):
        self.prelude()
        while self.continues:
            self.prompt()
        self.finish()

    def find_healing_potion(self):
        print("You find a healing potion. Use this to restore some lost hit-points.")
        self.__hero.gain_healing_potion()

    def find_vision_potion(self):
        print("You find a vision potion. Use this to see surrounding rooms.")
        self.__hero.gain_vision_potion()

    def fall_into_pit(self):
        print("You fall into a pit. The fall is merely frightening; the landing hurts.")
        self.__hero.take_damage()
        print("You now have " + str(self.__hero.hit_points) + " hit-points. Ouch.")
        # TODO: fix adventurer so that damage is randomly set, and hit points statement set there as well.

    def find_exit(self):
        # TODO: add this logic: if current room is exit
        print("Dilly Dilly! Brave Brave Brave Brave Sir " + self.name + " has found the exit.")
        self.__continues = False


if __name__ == "__main__":

    g_map_str = """
# This is my fine dungeon
+-----+-----+-----+
| i   |     = O   |
+--H--+--H--+-----+
| P   = XV  = HH  |
+-----+-----+-----+
"""

    g_game = DungeonAdventure(map_str=g_map_str)
    g_game.play()

# END
