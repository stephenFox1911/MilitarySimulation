#!/usr/bin/python

from soldier import Soldier
from usRifleman import USrifleman
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
    cover1 = Cover(1, 1, 3, 3, 50, 3, "|")
    cover2 = Cover(48, 48, 52, 52, 50, 3, "|")
    cover3 = Cover(95, 95, 97, 97, 50, 3, "|")
    
    coverList = [cover1, cover2, cover3]
    
    # (self, name, team, posx, posy, orientation, aggression):
    us1 = USrifleman("us1", "blue", "b1", 90, 100, 5, 50)
    us1.displaySoldier()

    # (self, name, team, posx, posy, orientation, aggression):
    t1 = TalibanRifleman("t1", "red", "r1", 0, 0, 6, -50)
    t1.displaySoldier()

    for x in xrange(0,10):
        us1.findCover(coverList)
        t1.findCover(coverList)
        us1.observe()
        us1.decide()
        t1.observe()
        t1.decide()
        t1.act()
        us1.act()
        moveNorth(us1, 10)
        moveSouth(t1, 10)
        us1.displaySoldier()
        t1.displaySoldier()

    print "Complete!"
    print "t1 hits: " + str(t1.hits)
    print "us1 hits: " + str(us1.hits)
    
if  __name__ =='__main__':main()