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

	# (self, name, team, posx, posy, orientation, aggression):
	us1 = USrifleman("us1", "blue", 90, 100, 5, 50)
	us1.displaySoldier()

	# (self, name, team, posx, posy, orientation, aggression):
	t1 = TalibanRifleman("t1", "red", 0, 0, 6, -50)
	t1.displaySoldier()

	for x in xrange(0,10):
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