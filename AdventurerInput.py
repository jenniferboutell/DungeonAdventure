from random import randrange

# from DungeonAdventure import DungeonAdventure
from Adventurer import Adventurer
from Compass import *
from Room import Room


class AdventurerInput:

    def __init__(self, game):
        self.__game = game
        self.__hero = Adventurer(game)
        self.__room = Room()


    @property
    def game(self):
        return self.__game

    @property
    def hero(self):
        return self.game.hero

    @property
    def name(self):
        return self.hero.name

    def set_name(self, val):
        self.hero.set_name(val)

    def start(self):
        start_option = input("Shall we play a game? (Y/N)\n")
        if start_option == "no":
            print("Commence global thermonuclear war in 3... 2... 1...")
            print(".....haha, not really. That is scheduled for tomorrow.")

        print("Huzzah! Welcome to Dungeon Adventure, Adventurer")
        name = input("What is your name, brave warrior?\n")
        # FIXME basic validation of name
        # TODO strip() surrounding whitespace
        self.set_name(name)
        self.menu()
        self.prompt()

    def finish(self):
        print(f"Brave Sir {self.name} is at The End.")
        # TODO report what kind of ending

    @staticmethod
    def menu():
        print("Here are your options...\n",
              "Move (N)orth, (S)outh, (E)ast, or (W)est;\n",
              "Use (V)ision Potion or (H)ealing Potion;\n"
              "Show (M)ap; (Q)uit the game; or (?) to get help")
        # Do NOT reveal the hidden '@' option to show full map

    def prompt(self):
        # Will need to pass in map here, or at least the four surrounding squares
        option = input(f"What would you like to do, brave Sir {self.name}?\n")

        if option == '?':
            self.menu()

        elif option == "Q":
            print(f"Brave Sir {self.name} ran away. Brave Brave Brave Brave Sir {self.name}.")
            self.game.quit()
            # exit()  # TODO do sys.exit() in main class, not here

        elif option == 'M':
            # TODO show visible map
            pass

        elif option == '@':
            # TODO show full map
            pass

        elif option in ('put directions back here when real traversal ready'):
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

        elif option == "Joshua":
            print("A strange game. The only winning move is not to play.")
            # no-op

        elif option in ('N', 'S', 'E', 'W'):
            print(f"You take a step to the {option}...")
            nextroom = self.__room.neighbor(option)
            if nextroom is None:
                print("There is no room in this direction.")
                return
            self.__room = nextroom
            self.__room.set_room()
            print(self.__room)
            if self.__room.healing_potions:
                self.find_healing_potion()
            if self.__room.vision_potions:
                self.find_vision_potion()
            if self.__room.has_pit:
                self.fall_into_pit()
        else:
            print("These words that you are using... I do not think they mean\n",
                  "what you think they mean. Please try again.")
            # no-op

    def find_healing_potion(self):
        print("You find a healing potion. Use this to restore some lost hit-points.")

    def find_vision_potion(self):
        print("You find a vision potion. Use this to see surrounding rooms.")

    def fall_into_pit(self):
        print("You fall into a pit. The fall is merely frightening; the landing hurts.")


class MockAdventurer:

    def __init__(self):
        self.__name = None

    @property
    def name(self):
        return self.__name

    def set_name(self, val):
        self.__name = val

    @staticmethod
    def move(_):
        return randrange(4) % 4 == 1

    @staticmethod
    def use_healing_potion():
        pass

    @staticmethod
    def use_vision_potion():
        pass


class MockGame:

    def __init__(self, rounds: int = 10):
        self.__rounds = rounds
        self.__hero = MockAdventurer()
        self.__io = AdventurerInput(self)

    @property
    def hero(self):
        return self.__hero

    def quit(self):
        self.__rounds = 0

    def continues(self):
        if self.__rounds > 0:
            self.__rounds -= 1
        return bool(self.__rounds)

    def play(self):
        self.__io.start()

        while self.continues():
            self.__io.prompt()
        self.__io.finish()


if __name__ == "__main__":
    g_game = MockGame()
    g_game.play()

# END
