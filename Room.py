import random
from typing import Optional
from compass import *


class RoomStyle:
    corner = "+"
    wall_n = "-----"
    wall_s = wall_n
    door_n = "--H--"
    door_s = door_n
    wall_w = "|"
    wall_e = wall_w
    door_w = "="
    door_e = door_w


class RoomStyleTom:
    corner = "*"
    wall_n = "*****"
    wall_s = wall_n
    door_n = "* - *"
    door_s = door_n
    wall_w = "*"
    wall_e = wall_w
    door_w = "|"
    door_e = door_w


class RoomStr:

    def __init__(self, _room, skip_north=None, skip_west=None, style=RoomStyle):
        skip_north = bool(skip_north)
        skip_west = bool(skip_west)
        self.lines = []

        # top
        if not skip_north:
            line = ""
            if not skip_west:
                line += style.corner
            if _room.has_door(North):
                line += style.door_n
            else:
                line += style.wall_n
            line += style.corner
            self.lines.append(line)

        # west/middle/east
        line = ""
        if not skip_west:
            if _room.has_door(West):
                line += style.door_w
            else:
                line += style.wall_w
        r = str(_room)
        line += f" {r:<3} "
        if _room.has_door(East):
            line += style.door_e
        else:
            line += style.wall_e
        self.lines.append(line)

        # bottom
        line = ""
        if not skip_west:
            line += style.corner
        if _room.has_door(South):
            line += style.door_s
        else:
            line += style.wall_s
        line += style.corner
        self.lines.append(line)

    def __str__(self):
        return "".join([f"{line}\n" for line in self.lines])


class Room:

    def __init__(self, grid=None, x=None, y=None) -> None:
        self.__grid = grid
        self.__x = x
        self.__y = y
        self.__doors = [False] * 4

    @property
    def grid(self):
        return self.__grid

    @property
    def x(self) -> Optional[int]:
        """ East-west position of room within grid, if any.
            Zero-based from west. None if not in grid. """
        if self.grid is None:
            return None
        return self.__x

    @property
    def y(self) -> Optional[int]:
        """ North-south position of room within grid, if any.
            Zero-based from north. None if not in grid. """
        if self.grid is None:
            return None
        return self.__y

    def has_door(self, direction) -> bool:
        return self.__doors[direction.ordinal]

    def add_door(self, direction):
        self.__doors[direction.ordinal] = True

    def __str__(self) -> str:
        if self.grid is not None:
            return f"{self.x},{self.y}"
        else:
            return "?"

    def __repr__(self) -> str:
        return self.__str__()


if __name__ == '__main__':
    print(f"Greetings from Room!")
    room = Room()
    print(f"solo room: {room}")
    room = Room(x=2, y=3)
    print(f"grid room: {room}")


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
