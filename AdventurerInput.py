from Room import Room

class AdventurerInput:

    def start(self):
        start_option = input("Would you like to play a game? (yes/no)")
        if start_option == "yes":
            print("Huzzah! Welcome to Dungeon Adventure, Adventurer")
            self.move(self)
        else:
            print("Commence thermonuclear war")
            print(". \n. \n. \n. \n. \n. \n. \n. \n. \n. \n. \n. \n. \n. \n. \n. \n tick")
            print(".....just kidding")
            self.start(self)



    def move(self):
        #Will need to pass in map here, or at least the four surrounding squares
        move_option = input("Would you like to go North, South, East, or West?")

        if move_option == "North":
            print("There is no room North of your position")
            self.move(self)
        #checks to see if there is a room 1 space north of adventurer's position, if so, checks to see if room is
        #accessible, if yes, sets room to that location.

        elif move_option == "South":
            print("There is no room South of your position")
            self.move(self)
        # checks to see if there is a room 1 space south of adventurer's position, if so, checks to see if room is
        #         #accessible, if yes, sets room to that location.

        elif move_option == "East":
            print("There is no room East of your position")
            self.move(self)
        # checks to see if there is a room 1 space East of adventurer's position, if so, checks to see if room is
        #         #accessible, if yes, sets room to that location.

        elif move_option == "West":
            print("There is no room West of your position")
            self.move(self)
        # checks to see if there is a room 1 space West of adventurer's position, if so, checks to see if room is
        #         #accessible, if yes, sets room to that location.

        else:
            print("I don't understand the words that are coming out of your mouth. Please try again.")
            self.move(self)

"""Other checks to do: contents of room. If room contains healing, vision, etc, write those strings."""

adventurer = AdventurerInput
adventurer.start(adventurer)
