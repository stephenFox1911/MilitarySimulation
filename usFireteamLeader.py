#!/usr/bin/python

from soldier import Soldier
import math

class USfireteamLeader(Soldier):
    'Fireteam Leader with M16'

    def __init__(self, name, team, fireteam, posx, posy, orientation, aggression):
        # subclass specific arguments go here
        Soldier.__init__(self, name, team, fireteam, posx, posy, orientation, aggression)
        
    def observe(self):
        return Soldier.observe(self)

    def decide(self):
        return Soldier.decide(self)
    
    def act(self):
        isShot = False
        target = None
        shotSuccess = False
        misses = 0

        if self.currentAction == "SimpleAttack" :
            print self.name + " Simple Attack"

            isShot = True
            self.isVisible = True
            self.coverQuality -= 10
            #Finds target with least amount of cover and fires one shot
            worstScore = float("inf")
            
            for enemy in self.enemyList :
                distance = math.hypot(enemy.posx - self.posx, enemy.posy - self.posy)
                if distance < 120 :
                    if (enemy.coverQuality + distance/60) <= worstScore and not enemy.isDead :
                        target = enemy  
                else :  
                    if (enemy.coverQuality + distance/60) <= worstScore and not enemy.isDead and enemy.isVisible:
                        target = enemy
            
            if target is None :
                isShot = False
                self.currentAction = "Move"
                self.state = "Move"
                self.act()
            else:
                #Attack enemy 3 times
                shotQuality = 50
                Soldier.output.write(self.name + "- Simple Attack: TARGET: " + target.name)
                for x in xrange(1,4):
                    if self.attack(target, shotQuality) :
                        shotSuccess = True
                    else:
                        misses += 1
                if shotSuccess :
                    Soldier.output.write(": Successful Hit\n")
                else : 
                    Soldier.output.write(": Shot Missed\n")

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
            
            self.targetCover = bestCover
            
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
        return (isShot, target, shotSuccess, misses)
        
    def displaySoldier(self):
        return Soldier.displaySoldier(self)


