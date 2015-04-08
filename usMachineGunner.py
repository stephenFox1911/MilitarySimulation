#!/usr/bin/python

from soldier import Soldier
from random import randint
import math

class USmachineGunner(Soldier):
    'USrifleman with SAW'

    def __init__(self, name, team, fireteam, posx, posy, orientation, aggression):
        # subclass specific arguments go here
        Soldier.__init__(self, name, team, fireteam, posx, posy, orientation, aggression)
        self.moveSpeed = 20

    def observe(self):
        return Soldier.observe(self)

    def decide(self):
        
        # Higher numbers represent the "more aggressive" decision
        decisionInt = randint(0,100) + self.aggression - self.suppression
        
        if self.state == "Neutral" :        
            # 30% chance that the soldier chooses to attack (before modifiers)
            if decisionInt >= 50 and len(self.enemyList) > 0 :
                self.state = "Engage"
                #Logic for choosing different types of attacks goes here
                self.currentAction = "MachineGunAttack"
            # 30% chance (or 60% if no targets)
            elif decisionInt >= 35 :
                self.state = "Move"
                self.currentAction = "Move"
                    
            else :
                self.state = "Cover"
                self.currentAction = "Cover"
        
        elif self.state == "Cover" :
            # 30% chance that the soldier chooses to attack (before modifiers)
            if decisionInt >= 50 and len(self.enemyList) > 0 :
                self.state = "Engage"
                #Logic for choosing different types of attacks goes here
                self.currentAction = "MachineGunAttack"
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
                self.currentAction = "MachineGunAttack"
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
        return Soldier.act(self)

    def displaySoldier(self):
        return Soldier.displaySoldier(self)


