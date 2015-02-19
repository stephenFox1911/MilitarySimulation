#!/usr/bin/python

from soldier import Soldier
from usRifleman import USrifleman
from talibanRifleman import TalibanRifleman

def moveNorth(soldier, distance):
	soldier.posy -= distance
def moveSouth(soldier, distance):
	soldier.posy += distance
def moveWest(soldier, distance):
	soldier.posx -= distance
def moveEast(soldier, distance):
	soldier.posx += distance


def main():
	print "testing"
	print Soldier.soldierCount
	# (self, name, posx, posy, orientation, suppression, hits):
	s1 = Soldier("s1", 20, 10, 180, 50, 0)
	s1.displaySoldier()
	print Soldier.soldierCount
	
	# (self, name, posx, posy, orientation, suppression, hits, test):
	us1 = USrifleman("us1", 50, 50, 0, 0, 0, "USrifleman")
	print Soldier.soldierCount

	# (self, name, posx, posy, orientation, suppression, hits, test):
	t1 = TalibanRifleman("t1", 100, 50, 0, 0, 0, "TalibanRifleman")
	t1.displaySoldier()
	print Soldier.soldierCount

	#US soldier attack taliban 10 times (simple 50% chance of hitting)
	for x in xrange(1,10):
		us1.attack(t1)
		t1.displaySoldier()

	# This moves USrifleman 1 south in increments of 5, 10 times.
	for x in xrange(1,10):
		moveSouth(us1, 5)
		us1.displaySoldier()

if  __name__ =='__main__':main()