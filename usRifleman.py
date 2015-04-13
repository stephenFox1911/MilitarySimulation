#!/usr/bin/python

from soldier import Soldier
import math

class USrifleman(Soldier):
    'USrifleman with M16'

    def __init__(self, name, team, fireteam, posx, posy, orientation, aggression):
        # subclass specific arguments go here
        Soldier.__init__(self, name, team, fireteam, posx, posy, orientation, aggression)
        
    def observe(self):
        return Soldier.observe(self)

    def decide(self):
        return Soldier.decide(self)

    def act(self):
        return Soldier.act(self)

    def displaySoldier(self):
        return Soldier.displaySoldier(self)


