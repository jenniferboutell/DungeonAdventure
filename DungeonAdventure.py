from Compass import Compass
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

    @property
    def name(self) -> str:
        return self.hero.name

    @property
    def maze(self) -> Maze:
        return self.__maze

    @property
    def room(self) -> Room:
        return self.__room

    @property
    def continues(self) -> bool:
        return self.__continues

    def start(self):
        start_option = input("Shall we play a game? (Y/N)\n")
        if start_option == "N":
            print("Commence global thermonuclear war in 3... 2... 1...")
            print(".....haha, not really. That is scheduled for tomorrow.")

        print("Huzzah! Welcome to Dungeon Adventure, Adventurer")
        name = input("What is your name, brave warrior?\n")
        # FIXME basic validation of name
        # TODO strip() surrounding whitespace
        self.hero.name = name
        self.menu()
        self.prompt()

    def finish(self):
        print(f"Brave Sir {self.name} is at The End.")
        # TODO report what kind of ending
        # TODO sys.exit() ...?

    @staticmethod
    def menu():
        print("\n".join(["Here are your options...",
                         "Move (N)orth, (S)outh, (E)ast, or (W)est;",
                         "Use (V)ision Potion or (H)ealing Potion;",
                         "Show (I)nventory; Show (M)ap;",
                         "(Q)uit the game; or (?) to get help"]))
        # Do NOT reveal the hidden options:
        # (*) show full map, (@) describe current room

    def prompt(self):
        # Will need to pass in map here, or at least the four surrounding squares
        option = input(f"What would you like to do, brave Sir {self.name}?\n")

        if option == '?':
            self.menu()

        elif option == "Q":
            print(f"Brave Sir {self.name} ran away. Brave Brave Brave Brave Sir {self.name}.")
            self.__continues = False

        elif option == 'M':
            # TODO show visible map
            pass

        elif option == '@':
            # Hidden option! Describe current room
            print(f"{self.room.describe()}")

        elif option == '*':
            # Hidden option! Print full maze
            print(f"{self.maze}")

        elif option in [_dir.abbr for _dir in Compass.dirs]:
            # Try going that direction; move returns False if cannot.
            if not self.hero.move(option):
                print("There is no door in that direction.")
                print(f"And lo, for Brave, Brave, Brave Sir {self.name} did stand still.")
            print(f"You take a step to the {option}...")

        elif option == 'H':
            print("You guzzle down the sweet, sweet elixir or life.")
            self.__hero.use_healing_potion()

        elif option == 'V':
            print("You guzzle down the crystal clear fluid.")
            self.__hero.use_vision_potion()
            # TODO: finish ues vision potion method in Adventurer

        elif option == "Joshua":
            print("A strange game. The only winning move is not to play.")
            # no-op

        elif option == 'I':
            self.__hero.display_inventory()

        elif option in ('N', 'S', 'E', 'W'):
            next_room = self.__room.neighbor(option)
            if next_room is None:
                print("There is no room in this direction.")
                print(f"And lo, for Brave, Brave, Brave Sir {self.name} did stand still.")
                return
            print(f"You take a step to the {option}...")
            self.__room = next_room
            # self.__room.set_room()  # FIXME nope, rely on loaded map!
            print(self.__room)
            if self.__room.healing_potions:
                self.find_healing_potion()
            if self.__room.vision_potions:
                self.find_vision_potion()
            if self.__room.has_pit:
                self.fall_into_pit()
            if self.__hero.hit_points <= 0:
                self.__continues = False
            if self.__room.is_exit:
                self.find_exit()  # TODO: add pillar logic
        else:
            print("These words that you are using... I do not think they mean\n",
                  "what you think they mean. Please try again.")
            # no-op

    def play(self):
        self.start()
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
        print("You now have " + str(self.__hero.hit_points) + " hit points. Ouch.")
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
