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

    cover1 = Cover(1, 1, 3, 3, 50, 3, "|")
    cover2 = Cover(48, 48, 52, 52, 50, 3, "|")
    cover3 = Cover(95, 95, 97, 97, 50, 3, "|")
    
    coverList = [cover1, cover2, cover3]
    
    # (self, name, team, posx, posy, orientation, aggression):
    us1 = USmachineGunner("us1", "blue", "b1", 60, 60, 0, 50)

    # (self, name, team, posx, posy, orientation, aggression):
    t1 = TalibanRifleman("t1", "red", "r1", 60, 40, 4, -50)

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