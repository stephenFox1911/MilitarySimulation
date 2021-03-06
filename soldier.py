#!/usr/bin/python
from random import randint
import random
import math

class Soldier:
    'Common base class for all soldiers'
    soldierCount = 0
    #list of all soldiers
    soldiers = []
    output = open("output.txt", "a+")

    def __init__(self, name, team, fireteam, posx, posy, orientation, aggression):
        self.name = name
        self.team = team
        self.posx = posx
        self.posy = posy
        #orientation 0=north, 2=east, 4=south, 6=west. Plus inbetweens
        self.orientation = orientation
        self.suppression = 0
        #This value should be between -50 and 50 
        self.aggression = aggression
        self.state = "Neutral"
        self.coverQuality = 0
        self.currentAction = "None"
        self.enemyList = []
        self.closestCover = []
        self.objectiveX = 0
        self.objectiveY = 0
        self.isDead = False
        self.isVisible = True
        self.fireteam = fireteam
        Soldier.soldierCount += 1
        Soldier.soldiers.append(self)
        self.moveSpeed = 30
        self.targetCover = None

    def attack(self, enemy, quality):
        distance = math.hypot(enemy.posx - self.posx, enemy.posy - self.posy)
        # if enemy is within 30 yards, ignore their cover
        if distance < 120 :
            shotMod = quality - self.suppression
        else: 
            #approximately 10% less likely to hit per 100 yards of distance
            shotMod = quality - self.suppression - enemy.coverQuality - (distance/60)
        hit = randint(0,100) + shotMod
        if hit > 100:
            print "successful hit"
            enemy.isDead = True
            return True
        else:
            print "shot misses"
            #this needs to be mitigated by aggression somehow
            #also modified by quality of shot
            enemy.suppression += 5
            return False

    def updateObjective(self, x, y):
        self.objectiveX = x
        self.objectiveY = y

    def observe(self):
        #decrement suppression
        if self.suppression <= 10:
            self.suppression = 0
        else:
            self.suppression -= 10

        #reset enemy list
        self.enemyList = []

        for s in Soldier.soldiers:
            if s.team != self.team and not s.isDead :
                self.enemyList.append(s)

    def decide(self):
        
        # Higher numbers represent the "more aggressive" decision
        decisionInt = randint(0,100) + self.aggression - self.suppression
        
        if self.state == "Neutral" :        
            self.state = "Move"
            self.currentAction = "Move"
        
        elif self.state == "Cover" :
            # 30% chance that the soldier chooses to attack (before modifiers)
            if decisionInt >= 50 and len(self.enemyList) > 0 :
                self.state = "Engage"
                #Logic for choosing different types of attacks goes here
                self.currentAction = "SimpleAttack"
            # 30% chance (or 60% if no targets)
            elif decisionInt >= 35 :
                self.state = "Move"
                self.currentAction = "Move"
                    
            else :
                self.state = "Cover"
                self.currentAction = "Cover"
        
        elif self.state == "Engage" :
            # 30% chance that the soldier chooses to attack (before modifiers)
            if decisionInt >= 50 and len(self.enemyList) > 0 :
                self.state = "Engage"
                #Logic for choosing different types of attacks goes here
                self.currentAction = "SimpleAttack"
            # 30% chance (or 60% if no targets)
            elif decisionInt >= 35 :
                self.state = "Move"
                self.currentAction = "Move"               
            else :
                self.state = "Cover"
                self.currentAction = "Cover"
        
        elif self.state == "Move" :
            # 10% chance that the soldier chooses to attack (before modifiers)
            if decisionInt >= 90 and len(self.enemyList) > 0 :
                self.state = "Engage"
                #Logic for choosing different types of attacks goes here
                self.currentAction = "SimpleAttack"
            # 10% chance
            elif decisionInt <= 10 :
                self.state = "Cover"
                self.currentAction = "Cover"
                    
            else :
                self.state = "Move"
                self.currentAction = "Move"
                
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

        elif self.currentAction == "MachineGunAttack" :
            isShot = True
            self.coverQuality -= 10
            self.isVisible = True
            lowSuppression = float("inf")

            for enemy in self.enemyList:
                if not enemy.isDead and enemy.suppression <= lowSuppression :
                    target = enemy
                    lowSuppression = enemy.suppression

            if target is None :
                isShot = False
                self.currentAction = "Move"
                self.state = "Move"
                self.act()
            else: 
                #Attack enemy multiple times
                shotQuality = 25
                Soldier.output.write(self.name + "- Machine Gun Attack: TARGET: " + target.name + " \n")
                for x in xrange(1,10):
                    if self.attack(target, shotQuality) :
                        shotSuccess = True
                    else:
                        misses += 1

        elif self.currentAction == "Move" :
            print self.name + " Move"
            self.coverQuality = 0
            self.isVisible = True
            
            bestCover = self.closestCover[randint(0,len(self.closestCover)-1)]

            Soldier.output.write(self.name + "- Moving to Cover \n")
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
                if c is None :
                    continue
                if c.in_cover(self.posx, self.posy) :
                    self.coverQuality = c.quality
                    inCover = True
                    self.isVisible = False
            #if there is no cover, the soldier goes prone
            if not inCover :
                Soldier.output.write(self.name+" Laying Down\n")
                self.coverQuality = 20
            Soldier.output.write(self.name + "- Taking Cover, Quality = " + str(self.coverQuality) + "\n")

        random.shuffle(Soldier.soldiers)
        return (isShot, target, shotSuccess, misses)

    def update(self):
        if self.state == "Move":
            distance = math.hypot(self.targetCover.posx - self.posx, self.targetCover.posy - self.posy)
            if distance < self.moveSpeed/20 and self.targetCover.current_occupancy < self.targetCover.occupancy: #TODO change from magic number
                self.posx, self.posy = self.targetCover.center
                self.coverQuality = self.targetCover.quality
                self.state = "Cover"
                self.targetCover.current_occupancy += 1
                self.targetCover = None
            else :
                dx = self.posx - self.targetCover.posx
                dy = self.posy - self.targetCover.posy
                theta = math.atan2(dy, dx)
                self.posx -= math.cos(theta) * self.moveSpeed / 20 #TODO remove magic number
                self.posy -= math.sin(theta) * self.moveSpeed / 20 #TODO remove magic number

    def displaySoldier(self):
        out = "Name: " + self.name +  ", Position:(" + str(self.posx) + "," + str(self.posy) + "), orientation:" + str(self.orientation) + "\n"
        print out
        Soldier.output.write(out)
    
    def findCover(self, coverList):
        Soldier.output.write(self.name + " Looking for Cover\n")
        #returns the three closest pieces of cover
        minDistances = [99999, 99998, 99997, 99996, 99995, 99994, 99993, 99992]
        closeCover = [None, None, None, None, None, None, None, None]
        
        for c in coverList:
            coverDistance = math.hypot(c.center[0] - self.objectiveX, c.center[1] - self.objectiveY)
            selfDistance = math.hypot(self.posx - self.objectiveX, self.posy - self.objectiveY)
            distance = math.hypot(c.center[0] - self.posx, c.center[1] - self.posy)
            currentMax = max(minDistances)

            if distance < currentMax and coverDistance <= selfDistance:
                index = minDistances.index(currentMax)
                minDistances[index] = distance
                closeCover[index] = c

        bestCover = []
        scoreList = []
        #approximately 5 yards
        FIRETEAM_IDEAL_DISTANCE = 30
        friendScore = 0
        #will choose cover with lowest score
        for c in closeCover:
            if c is None :
                continue
            if c.posx == self.posx and c.posy == self.posy :
                bestCover.append((c, 0))
            for s in Soldier.soldiers :
                if s.fireteam == self.fireteam and s.team == self.team and not s.isDead:
                    #find distance between fireteam member and cover
                    dist = math.hypot(c.center[0] - s.posx, c.center[1] - s.posy)
                    if dist >= FIRETEAM_IDEAL_DISTANCE :
                        friendScore += dist - FIRETEAM_IDEAL_DISTANCE
                    else :
                        friendScore += FIRETEAM_IDEAL_DISTANCE - dist
            #get distance
            score = math.hypot(c.center[0] - self.posx, c.center[1] - self.posy)/60
            score -= 3*c.quality
            score += 20*c.current_occupancy
            score += friendScore
            if c.cover_available and not c.in_cover(self.posx, self.posy) and (len(bestCover) < 4 or score < max(scoreList)):
                if len(bestCover) < 4 :
                    bestCover.append((c, score))
                    scoreList = [tup[1] for tup in bestCover]
                else:
                    scoreList = [tup[1] for tup in bestCover]
                    scoreList[scoreList.index(max(scoreList))] = (c, score)

        self.closestCover = [tup[0] for tup in bestCover]
