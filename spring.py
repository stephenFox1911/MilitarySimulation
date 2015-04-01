import math

class Spring:
    def __init__(self, s1, s2, length=20, strength=1):
        '''
        @summary: represents a spring between two soldiers
        @param s1: the first soldier object
        @param source_y: the y-coord for the source soldier
        @param target_x: the x-coord for the target soldier
        @param target_y: the y-coord for the target soldier
        @param hit: boolean, true for a hit, false for a miss
        '''
        self.s1 = s1
        self.s2 = s2
        self.length = length
        self.strength = strength
    
    def update(self):
        dx = self.s1.posx - self.s2.posx
        dy = self.s1.posy - self.s2.posy
        dist = math.hypot(dx, dy)
        theta = math.atan2(dy, dx)
        force = (self.length - dist) * self.strength

        self.p1.accelerate((theta + 0.5 * math.pi, force/self.p1.mass))
        self.p2.accelerate((theta - 0.5 * math.pi, force/self.p2.mass))
