class Room:

    def __init__(self, healing_potion, pit, entrance, exit, pillars, doors, vision_potion):
        """Contains default constructor and all methods you deem necessary -- modular design is CRUCIAL """
        self.healing_potion = False
        self.pit = False
        self.entrance = False
        self.exit = False
        self.pillars = []
        self.doors = ["N","S","E","W"]
        self.vision_potion = False

    def __str__(self):
        pass









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
