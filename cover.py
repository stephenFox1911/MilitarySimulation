class Cover:
    def __init__(self, nw_x, nw_y, se_x, se_y, quality, occupancy, direction, passable=True, fireable=True):
        '''
        @summary: a class to represent cover
        @param nw_x: the x-coord for the northwest corner of cover
        @param nw_y: the y-coord for the northwest corner of cover
        @param se_x: the x-coord for the southeast corner of cover
        @param se_y: the y-coord for the southeast corner of cover
        @param quality: int, ranges from 0 to 2, represents quality of cover
        @param occupancy: maximum occupancy
        @param direction: direction in which the cover faces. '-' means east to west, '|' means north to south, '/' means southwest to northeast, '\\' means northwest to southeast
        @param passable: Boolean, determines if soldier can pass though (or over) the cover (defaults to true)
        @param fireable: Boolean, determines if the soldier can fire from cover (defaults to true)
        '''
        self.nw_x = nw_x
        self.nw_y = nw_y
        self.se_x = se_x
        self.se_y = se_y
        self.quality = quality
        self.occupancy
        self.current_occupancy = 0
        self.passable = passable
        self.fireable = fireable
        self.center = ((nw_x+se_x)/2, (nw_y+se_y)/2)
    def in_cover(self,x,y):
        '''
        @summary: takes in the soldier's x,y corrdinates to determine if he is in this particular cover
        '''
        return x >= self.nw_x and x <= self.se_x and y <= self.nw_y and self.y >= se_y
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
        if self.direction == '-':

