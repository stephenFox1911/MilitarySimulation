#!/usr/bin/python

from soldier import Soldier
import math

class USfireteamLeader(Soldier):
    'Fireteam Leader with M16'

    def __init__(self, name, team, fireteam, posx, posy, orientation, aggression):
        # subclass specific arguments go here
        Soldier.__init__(self, name, team, fireteam, posx, posy, orientation, aggression)
        

    def observe(self):
        Soldier.observe(self)

    def decide(self):
        Soldier.decide(self)
    
    def act(self):
        isShot = False
        target = None
        shotSuccess = False

        if self.currentAction == "SimpleAttack" :
            print self.name + " Simple Attack"

            isShot = True
            self.coverQuality -= 10
            #Finds target with least amount of cover and fires one shot
            worstCover = 1000
            
            for enemy in self.enemyList :
                if enemy.coverQuality <= worstCover :
                    target = enemy
            
            #Attack enemy 3 times
            shotQuality = 50
            Soldier.output.write("Simple Attack: TARGET: " + target.name + " \n")
            for x in xrange(1,3):
                if self.attack(target, shotQuality) :
                    shotSuccess = True

        elif self.currentAction == "Move" :
            print self.name + " Move"
            self.coverQuality = 0
            coverRank = 99999
            bestCover = None
            #will choose cover with lowest score
            for c in self.closestCover:
                #get distance
                score = math.hypot(c.center[0] - self.posx, c.center[1] - self.posy)
                score -= 3*c.quality
                score += 10*c.current_occupancy
                if c.cover_available and score < coverRank:
                    bestCover = c
            Soldier.output.write("Moving to Cover at Xval: " + str(bestCover.center[0]) + "Yval: " + str(bestCover.center[1]) + "\n")
            #cover decision has been made, now orient and move towards it
            diffX = self.posx - bestCover.center[0]
            diffY = self.posy - bestCover.center[1]
            if (bestCover.center[0] > self.posx + diffY) and (bestCover.center[0] < self.posx - diffY) and (bestCover.center[1] < self.posy):
                self.orientation = 0
            elif (bestCover.center[0] > self.posx - diffY) and (bestCover.center[1] > self.posy - diffX) and (bestCover.center[0] > self.posx) and (bestCover.center[1] < self.posy):
                self.orientation = 1
            elif (bestCover.center[1] > self.posy - diffY) and (bestCover.center[1] < self.posy + diffY) and (bestCover.center[0] > self.posx):
                self.orientation = 2
            elif (bestCover.center[1] > self.posy + diffX) and (bestCover.center[0] > self.posx + diffY) and (bestCover.center[0] > self.posx) and (bestCover.center[1] > self.posy):
                self.orientation = 3
            elif (bestCover.center[0] > self.posx - diffY) and (bestCover.center[0] < self.posx + diffY) and (bestCover.center[1] > self.posy):
                self.orientation = 4
            elif (bestCover.center[0] < self.posx - diffY) and (bestCover.center[1] > self.posy - diffX) and (bestCover.center[0] < self.posx) and (bestCover.center[1] > self.posy):
                self.orientation = 5
            elif (bestCover.center[1] < self.posy - diffX) and (bestCover.center[1] > self.posy + diffX) and (bestCover.center[0] < self.posx):
                self.orientation = 6
            elif (bestCover.center[1] < self.posy + diffX) and (bestCover.center[0] < self.posx + diffY) and (bestCover.center[0] < self.posx) and (bestCover.center[1] < self.posy):
                self.orientation = 7
            
            distance = math.hypot(c.center[0] - self.posx, c.center[1] - self.posy)
            #Currently the soldier moves to the middle of the cover mostly because I'm feeling lazy
            #Needs to be updated to stick the soldier behind cover
            if distance < self.moveSpeed:
                self.posx = bestCover.center[0]
                self.posy = bestCover.center[1]
                Soldier.output.write("I WANT COVER: X: " + str(bestCover.center[0]) + " Y: " + str(bestCover.center[1]) + "\n")
                self.coverQuality = bestCover.quality
                self.state = "Cover"
            else :
                if bestCover.center[0] > self.posx + (self.moveSpeed/2) :
                    self.posx += self.moveSpeed/2
                if bestCover.center[1] > self.posy + (self.moveSpeed/2) :
                    self.posy += self.moveSpeed/2
            
        elif self.currentAction == "Cover" :
            print self.name + " Taking Cover"
            #get value of cover if in use
            inCover = False
            for c in self.closestCover :
                if c.in_cover(self.posx, self.posy) :
                    self.coverQuality = c.quality
                    inCover = True
            #if there is no cover, the soldier goes prone
            if not inCover :
                self.coverQuality = 20
            Soldier.output.write("Taking Cover, Quality = " + str(self.coverQuality) + "\n")
        return (isShot, target, shotSuccess)
        
    def displaySoldier(self):
        Soldier.displaySoldier(self)


