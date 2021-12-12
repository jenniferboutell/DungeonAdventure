from Room import Room

class AdventurerInput:

    def __init__(self, name):
        self.name = None

    def start(self):
        start_option = input("Would you like to play a game? (yes/no)")
        if start_option == "yes":
            print("Huzzah! Welcome to Dungeon Adventure, Adventurer")
            self.name = input("What is your name, brave warrior?")
            self.move(self)
        else:
            print("Commence global thermonuclear war")
            print(". \n. \n. \n. \n. \n. \n. \n. \n. \n. \n. \n. \n. \n. \n. \n. \n tick")
            print(".....just kidding")
            self.start(self)



    def move(self):
        print("Menu: Go North = N, Go South = S, Go East = E, Go West = W, Use Vision Potion = V, Use Healing Potion = H, Help = help, Q = Quit Game")
        #Will need to pass in map here, or at least the four surrounding squares
        move_option = input("What would you like to do, brave Sir " + self.name + "?")
        #help
        #showmap
        #showfullmap - create funny command option for this
        #or - just print the full menu for each move.

        if move_option == "N":
            print("There is no room North of your position")
            print("Brave, Brave, Brave Brave Sir " + self.name + " did stand still.")
            self.move(self)
        #checks to see if there is a room 1 space north of adventurer's position, if so, checks to see if room is
        #accessible, if yes, sets room to that location.

        elif move_option == "S":
            print("There is no room South of your position")
            print("Brave, Brave, Brave Brave Sir " + self.name + " did stand still.")
            self.move(self)
        # checks to see if there is a room 1 space south of adventurer's position, if so, checks to see if room is
        #         #accessible, if yes, sets room to that location.

        elif move_option == "E":
            print("There is no room East of your position")
            print("Brave, Brave, Brave Brave Sir " + self.name + " did stand still.")
            self.move(self)
        # checks to see if there is a room 1 space East of adventurer's position, if so, checks to see if room is
        #         #accessible, if yes, sets room to that location.

        elif move_option == "W":
            print("There is no room West of your position")
            print("Brave, Brave, Brave Brave Sir " + self.name + " did stand still.")
            self.move(self)
        # checks to see if there is a room 1 space West of adventurer's position, if so, checks to see if room is
        #         #accessible, if yes, sets room to that location.

        elif move_option == "Joshua":
            print("A strange game. The only winning move is not to play.")
            self.move(self)

        elif move_option == "Q":
            print("Brave Sir " + self.name + " ran away. Brave Brave Brave Brave Sir " + self.name + ".")
            exit()

        else:
            print("These words that you are using, they do not mean what I think you think they mean. Please try again.")
            self.move(self)

"""Other checks to do: contents of room. If room contains healing, vision, etc, write those strings."""

adventurer = AdventurerInput
adventurer.start(adventurer)
