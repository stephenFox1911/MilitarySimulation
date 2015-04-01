#!/usr/bin/python

from soldier import Soldier

class USrifleman(Soldier):
    'USrifleman with M16'

    def __init__(self, name, team, fireteam, posx, posy, orientation, aggression):
        # subclass specific arguments go here
        Soldier.__init__(self, name, team, fireteam, posx, posy, orientation, aggression)
        

    def observe(self):
        Soldier.observe(self)

    def decide(self):
        Soldier.decide(self)
    
    def act(self):
        Soldier.act(self)

    def displaySoldier(self):
        Soldier.displaySoldier(self)


