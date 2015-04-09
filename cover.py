import math

class Cover:
    def __init__(self, x, y, quality, occupancy, direction='-', passable=True, fireable=True):
        '''
        @summary: a class to represent cover
        @param posx: the x-coord for the cover
        @param posy: the y-coord for the cover
        @param quality: int, ranges from 0 to 1, represents quality of cover
        @param occupancy: maximum occupancy
        @param direction: direction in which the cover faces. '-' means east to west, '|' means north to south, '/' means southwest to northeast, '\\' means northwest to southeast
        @param passable: Boolean, determines if soldier can pass though (or over) the cover (defaults to true)
        @param fireable: Boolean, determines if the soldier can fire from cover (defaults to true)
        '''
        self.posx = x
        self.posy = y
        if quality == 1:
            self.quality = 45
        elif quality == 0:
            self.quality = 35
        self.occupancy = occupancy
        self.current_occupancy = 0
        self.passable = passable
        self.fireable = fireable
        self.center = (x,y) #legacy code
    def in_cover(self,x,y):
        '''
        @summary: takes in the soldier's x,y corrdinates to determine if he is in this particular cover
        '''
        return x == self.posx and y == self.posy
    def cover_available(self):
        return self.current_occupancy < self.occupancy
    def add_to_cover(self):
        self.current_occupancy += 1
    def remove_from_cover(self):
        self.current_occupancy -= 1
    def is_flanking_shot(self, source_x, source_y): #In progress
        '''
        @summary: determines if a shot from the given source would be flanking those using this cover
        '''
        atan_degrees = math.atan((self.center[1]-source_y)/(self.center[0]-source_x)) * 180 / math.pi
        if self.direction == '-':
            if atan_degrees >= -45 and atan_degrees <= 45:
                return True
            else:
                return False
        elif self.direction == '|':
            if atan_degrees >= 45 and atan_degrees <= -45:
                return True
            else:
                return False
        elif self.direction == '/':
            if atan_degrees:
                return True
            else:
                return False
        elif self.direction == '\\':
            if atan_degrees:
                return True
            else:
                return False
