#!/usr/bin/python
from soldier import Soldier
from random import randint
import random
import math

class TalibanMachineGunner(Soldier):
    'Taliban soldier with machine gun'

    def __init__(self, name, team, fireteam, posx, posy, orientation, aggression):
        # subclass specific arguments go here
        Soldier.__init__(self, name, team, fireteam, posx, posy, orientation, aggression)
        

    def observe(self):
        return Soldier.observe(self)

    def decide(self):
        # Higher numbers represent the "more aggressive" decision
        decisionInt = randint(0,100) + self.aggression - self.suppression
        
        if self.state == "Neutral" :        
            if decisionInt >= 300 and len(self.enemyList) > 0 :
                self.state = "Engage"
                #Logic for choosing different types of attacks goes here
                self.currentAction = "MachineGunAttack"                    
            else :
                self.state = "Cover"
                self.currentAction = "Cover"
        
        elif self.state == "Cover" :
            if decisionInt >= 50 and len(self.enemyList) > 0 :
                self.state = "Engage"
                #Logic for choosing different types of attacks goes here
                self.currentAction = "MachineGunAttack"
            else :
                self.state = "Cover"
                self.currentAction = "Cover"
        
        elif self.state == "Engage" :
            if decisionInt >= 50 and len(self.enemyList) > 0 :
                self.state = "Engage"
                #Logic for choosing different types of attacks goes here
                self.currentAction = "MachineGunAttack"

            else :
                self.state = "Cover"
                self.currentAction = "Cover"
        
        elif self.state == "Move" :
            if decisionInt >= 50 and len(self.enemyList) > 0 :
                self.state = "Engage"
                #Logic for choosing different types of attacks goes here
                self.currentAction = "MachineGunAttack"

            else :
                self.state = "Cover"
                self.currentAction = "Cover"

    
    def act(self):
        return Soldier.act(self)

    def displaySoldier(self):
        return Soldier.displaySoldier(self)


