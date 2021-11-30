import random

class Room:

    def __init__(self, healing_potion = False, pit = False, entrance = False, exit = False, pillars = [], \
                 doors = ["N", "S", "E", "W"], vision_potion = False, x = 0, y = 0):
        self.pillars = []
        """Contains default constructor and all methods you deem necessary -- modular design is CRUCIAL """


    def count_contents(self, contents = 0):
        if self.healing_potion == True:
            contents += 1
        if self.pit == True:
            contents += 1
        if self.vision_potion == True:
            contents += 1
        if self.pillars != []:
            contents += 1

        print(contents)
        if contents > 1:
            print("Multiple objects example")
        else:
            print("All the if statements will be needed for this one")


    def __str__(self):
        pass

    def set_room(self, percent = 10):
        self.healing_potion = random.randrange(100) < percent
        self.pit = random.randrange(100) < percent
        self.vision_potion = random.randrange(100) < percent
        self.pillars = ["I"]
        print(str(self.healing_potion) + " Healing Potion \n" + str(self.pit) + " Pit\n" + str(self.vision_potion) + \
              " Vision Potion \n" + self.pillars[0] )

room = Room()
room.set_room()
room.count_contents()
room.__str__()












"""
o (Possibly an) Entrance - only one room will have an entrance and the room that contains the entrance will contain 
NOTHING else 
o (Possibly an) Exit - only one room will have an exit and the room that contains the exit will contain NOTHING 
else 
o (Possibly a) Pillar of OO - four pillars in game and they will never be in the same room 
o Doors - N, S, E, W 
o 10% possibility (this is a constant that you can modify) room will contain a healing potion, vision potion, and pit 
(each of these are independent of one another) 
o Vision Potion - can be used to allow user to see eight rooms surrounding current room as well as current room 
(location in maze may cause less than 8 to be displayed) 
• Must contain a _ _ str _ _ () method that builds a 2D Graphical representation of the room (NOTE: you may use any 
graphical components that you wish).  The (command line) representation is as follows:  
o * - * will represent a north/south door (the - represents the door).  If the room is on a boundary of the maze (upper 
or lower), then that will be represented with *** 
o East/west doors will be represented in a similar fashion with the door being the | character as opposed to a -. 
o In the center of the room you will display a letter that represents what the room contains.  
Here are the letters to use and what they represent:  
▪ M - Multiple Items 
▪ X - Pit 
▪ i - Entrance (In) 
▪ O - Exit (Out) 
▪ V - Vision Potion 
▪ H - Healing Potion 
▪ <space> - Empty Room 
▪ A, E, I, P - Pillars 
Example:  Room 1,1 might look like  
* - * 
| P  | 
* - * 
"""
