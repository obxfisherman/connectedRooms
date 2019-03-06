from random import randint, choice
import numpy as np

# based on: https://gist.github.com/munificent/b1bcd969063da3e6c298be070a22b604 Robert Nystrom @munificentbob for Ginny 2008-2019
# and also from https://gist.github.com/Joker-vD/cc5372a349559b9d1a3b220d5eaf2b01

TILE_VOID        = 0 #' '
TILE_FLOOR       = 1 #'.'
TILE_WALL        = 2 #'#'
TILE_CORNER      = 3 #'!'
TILE_OPEN_DOOR   = 4 #'+'
TILE_CLOSED_DOOR = 5 #'*'
TILE_PLAYER      = 6 #'@'

#-----------------------------------------------------------------------------------------------
class ConnectedRooms(object):
    """build a map of interconnected rooms"""
    def __init__(self, width=80, height=40):
        self.map_width=width
        self.map_height=height
        self.dmap=np.zeros((width, height), dtype=np.uint8)

    #-----------------------------------------------------------------------------------------------
    def generate(self):
        for i in range(1000):
            self.cave(i==0)

    #-----------------------------------------------------------------------------------------------
    def cave(self, first_room):
        width=randint(5,15)
        height=randint(3,9)
        x0=randint(2,self.map_width - width - 1) - 2
        y0=randint(2,self.map_height - height -1) - 2
        x1=x0 + width + 2
        y1=y0 + height + 2

        for y in range(y0, y1):
            for x in range(x0, x1):
                if self.dmap[x,y]==TILE_FLOOR:      #if the new room toches any other floor then this room is invalid
                    return

        doors=[]    #list of potential doors
        if not first_room:
            for y in range(y0, y1):
                for x in range(x0, x1):
                    s=(x==x0 or x==x1-1)
                    t=(y==y0 or y==y1-1)
                    if not (s and t):           #dont make a door on a corner
                        if (s or t) and (self.dmap[x,y]==TILE_WALL):  #only make a door on the perimeter and where it intesects another wall
                            doors.append((x,y))     #build list of potential doors
            if len(doors)==0:   #if we didnt find any doors then this is not valid room attached to another room
                return

        #if we got this far we have a valid room so carve it out of the void
        for y in range(y0, y1):
            for x in range(x0, x1): 
                if self.dmap[x,y]!=TILE_CORNER:     #dont over write another corner
                    s=(x==x0 or x==x1-1)
                    t=(y==y0 or y==y1-1)
                    if s and t:
                        self.dmap[x,y]=TILE_CORNER
                    elif s or t:
                        self.dmap[x,y]=TILE_WALL
                    else:
                        self.dmap[x,y]=TILE_FLOOR

        if first_room:
            h=randint(0,width-1)+x0+1
            v=randint(0,height-1)+y0+1
            self.dmap[h,v]=TILE_PLAYER
        else:
            door=choice(doors)
            dtype=choice([TILE_OPEN_DOOR, TILE_CLOSED_DOOR, TILE_OPEN_DOOR])
            self.dmap[door[0], door[1]]=dtype
            #add any other items or npcs to the rooms here. see player random location for example

    #-----------------------------------------------------------------------------------------------
    def print_map(self):
        #change the TILE_CORNER to another character such as ! to see the corners in the map.
        icons={TILE_VOID:' ', TILE_FLOOR:'.', TILE_WALL:'#', TILE_CORNER:'#', TILE_OPEN_DOOR:'+', TILE_CLOSED_DOOR:'*', TILE_PLAYER:'@'}
        for v in range(self.map_height):
            ln=''
            for h in range(self.map_width):
                ln+=icons[self.dmap[h,v]]
            print(ln)


#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    cr=ConnectedRooms()
    cr.generate()
    cr.print_map()

