from Compass import Compass, CompassDirection
from Room import Room
from Maze import Maze
from Adventurer import Adventurer
# from random import randrange


class DungeonAdventure:
    pillars = {'A', 'E', 'I', 'P'}
    default_hit_points_initial = 20     # start kinda weak
    default_hit_points_max = 100        # the strength of ten (wo)men!
    pit_damage = 10

    def __init__(self, map_str: str = None):
        self.__maze = Maze(map_str=map_str)
        # TODO populate maze with entrance/exit, items
        self.__room = self.maze.room(0, 0)  # FIXME set to entrance
        self.__hero = Adventurer(game=self,
                                 hit_points=self.default_hit_points_initial,
                                 hit_points_max=self.default_hit_points_max)
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
        if not self.hero.is_alive:
            return False
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
        print(f"Oh my. Your parents had some strange ideas, Sir {self.name}.")
        print()  # Blank line for visual separation

        print("Very well then, you have entered a Dungeon, in which there is a Maze.")
        print("There are perilous Pits, potent Potions to purloin, and four Pillars to perceive.")
        self.enter_room(self.room)
        print(str(self.room))
        self.display_menu()

    def finish(self):
        print(f"Brave Sir {self.name} is at The End.")
        # TODO report what kind of ending
        # TODO sys.exit() ...?

    @staticmethod
    def display_menu():
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
            self.display_menu()

        elif match(option, 'Q', 'quit'):
            print("Discretion is the better part of valor.")
            print(f"Three cheers for brave Sir {self.name}!")
            self.continues = False

        elif match(option, 'I', 'inventory'):
            print("Thine Bag of Holding doth weigh upon you most ponderously...")
            self.hero.display_inventory()

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
            print(self.maze.str(style=Room.styles.tracker))

        elif match(option, 'H', 'healing', 'health'):
            if self.hero.healing_potions <= 0:
                print("Did you suffer a head injury? You do not have any Healing Potions.")
            else:
                print("You guzzle down the sweet, sweet elixir or life.")
                self.hero.use_healing_potion()
                print(f"You have {self.hero.hit_points} hit points now.")

        elif match(option, 'V', 'vision'):
            if self.hero.vision_potions <= 0:
                print("Oblivious as always, you failed to note your lack of Vision Potions.")
            else:
                print("You swig the crystal clear fluid, gasp, then stare in amazement...")
                self.hero.use_vision_potion()
                # TODO: finish use_vision_potion method in Adventurer
                # TODO fetch 3x3 subgrid centered at current room, and display

        elif Compass.dir(option):
            _dir: CompassDirection = Compass.dir(option)
            print(f"You take a step to the {_dir.name}... ", end='')
            can_move, next_room = self.maze.can_move(self.room, direction=_dir)
            next_room = self.room.neighbor(option)
            if not can_move:
                print("but are thwarted.")
                print(f"Brave Sir {self.name} didst stare defiantly at his shoes.")
                return
            if next_room is None:
                print("but discover there is void on the other side.")
                print(f"Brave Sir {self.name} steps back from the precipice.")
                return
            print("sailing gracefully into the next room.")
            print(next_room)
            self.enter_room(next_room)

        else:
            print()  # empty line for visual separation
            print("These words that you are using...")
            print("I do not think they mean what you think they mean.")
            print("Perhaps your response should be in the form of a '?'...")
            # no-op

    def play(self):
        self.prelude()
        # TODO populate maze with items
        # TODO set self.room=Entrance (if not 0,0)
        while self.continues:
            self.prompt()
        self.finish()

    def find_healing_potion(self):
        print("You find a Healing Potion. Use this to restore some lost hit-points.")
        self.room.healing_potions -= 1
        self.hero.gain_healing_potion()

    def find_vision_potion(self):
        print("You find a Vision Potion. Use this to see surrounding rooms.")
        self.room.vision_potions -= 1
        self.hero.gain_vision_potion()

    def find_pillar(self, pillar: str = None):
        if pillar is None and self.room.pillar is not None:
            pillar = self.room.pillar
        if self.hero.has_pillar(pillar):
            print(f"Oh look, the Pillar '{pillar}'. Already seen it. So boring.")
        else:
            print(f"You find the Pillar '{pillar}'. Good job, you!")
            self.hero.gain_pillar(self.room.pillar)

    def fall_into_pit(self):
        print("You fall into a Pit. The fall is merely frightening... ", end='')
        # TODO: damage is randomly set (?)
        self.hero.take_damage(damage=self.pit_damage)
        if not self.hero.is_alive:
            print("but the landing is fatal.  x_x")
        else:
            print("but the landing hurts. Oof!  >_<")
            print(f"You now have {self.hero.hit_points} hit-points.")

    def find_exit(self):
        if not self.room.is_exit:
            return
        if not self.room.has_crumb:
            print(f"Dilly Dilly! Brave Sir {self.name} has found the Exit!")
        else:
            print(f"Brave Sir {self.name} once again arrives at the exit.")
        if self.hero.pillars == self.pillars:
            self.__continues = False
        else:
            print("But the mission is not complete! Find the remaining Pillars,")
            print("then return here to the Exit... if you can!")

    def enter_room(self, room) -> None:
        """ Enter a room. Stuff happens and/or is found.
        """
        if self.room is not None:
            self.room.has_hero = False
        self.room = room
        self.room.has_hero = True
        # Falling into pit occurs first. If fatal, do not find other contents.
        if room.has_pit:
            self.fall_into_pit()
        if not self.hero.is_alive:
            return
        # Collect items
        if room.healing_potions:
            self.find_healing_potion()
        if room.vision_potions:
            self.find_vision_potion()
        # Pillars and Exit are each supposed to be sole item in room, if present.
        # Ergo, cannot have both, so order of the following does not matter.
        if room.pillar:
            self.find_pillar()
        if room.is_exit:
            self.find_exit()
        # Drop breadcrumb AFTER finding Pillar or Exit, so announce differently.
        room.has_crumb = True


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
