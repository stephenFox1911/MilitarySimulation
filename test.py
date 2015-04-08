#!/usr/bin/python

from soldier import Soldier
from usRifleman import USrifleman
from usMachineGunner import USmachineGunner
from talibanRifleman import TalibanRifleman
from cover import Cover

def moveNorth(soldier, distance):
    soldier.posy -= distance
def moveSouth(soldier, distance):
    soldier.posy += distance
def moveWest(soldier, distance):
    soldier.posx -= distance
def moveEast(soldier, distance):
    soldier.posx += distance


def main():
    output = open("output.txt", "a+")

    #cover1 = Cover(1, 1, 50, 3,)
    cover2 = Cover(48, 48, 50, 3)
    cover3 = Cover(95, 95, 50, 3)
    
    coverList = [cover2, cover3]
    
    # (self, name, team, posx, posy, orientation, aggression):
    us1 = USrifleman("us1", "blue", "b1", 0, 0, 0, 0)
    us1.objectiveX = 100
    us1.objectiveY = 100

    # (self, name, team, posx, posy, orientation, aggression):
    t1 = TalibanRifleman("t1", "red", "r1", 90, 90, 4, 0)
    t1.objectiveX = 0
    t1.objectiveY = 0

    for x in xrange(0,10):
        us1.findCover(coverList)
        t1.findCover(coverList)

        us1.displaySoldier()
        us1.observe()
        us1.decide()
        us1.act()
        
        t1.displaySoldier()
        t1.observe()
        t1.decide()
        t1.act()

    print "Complete!"
    print "t1 hits: " + str(t1.hits)
    print "us1 hits: " + str(us1.hits)
    output.write("Complete!\n")
    output.write("t1 hits: " + str(t1.hits) + "\n")
    output.write("us1 hits: " + str(us1.hits) + "\n\n")

if  __name__ =='__main__':main()