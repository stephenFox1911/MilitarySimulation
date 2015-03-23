class ShotLine:
    def __init__(self, source_x, source_y, target_x, target_y, hit):
        '''
        @summary: a class to hold data for each shot fired
        @param source_x: the x-coord for the source soldier
        @param source_y: the y-coord for the source soldier
        @param target_x: the x-coord for the target soldier
        @param target_y: the y-coord for the target soldier
        @param hit: boolean, true for a hit, false for a miss
        '''
        self.source_x = source_x
        self.source_y = source_y
        self.target_x = target_x
        self.target_y = target_y
        self.hit = hit
        self.alpha = 1
    def degrade(self):
        #reduces alpha to increase the ShotLine's transparency
        self.alpha -= 0.1 #rate of degradation
