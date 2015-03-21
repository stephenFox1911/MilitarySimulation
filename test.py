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
	print "Soldiers:", Soldier.soldierCount
	
	# (self, name, team posx, posy, orientation, suppression, hits, test):
	us1 = USrifleman("us1", "blue", 50, 100, 1, 0)
	us1.displaySoldier()

	# (self, name, posx, posy, orientation, suppression, hits, test):
	t1 = TalibanRifleman("t1", "red", 70, 1, 6, 0)
	t1.displaySoldier()

	us1.observe()

	
if  __name__ =='__main__':main()