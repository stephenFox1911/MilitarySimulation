#!/usr/bin/python

from soldier import Soldier

class TalibanRifleman(Soldier):
	'USrifleman with M16'

	def __init__(self, name, team, posx, posy, orientation, aggression):
		# subclass specific arguments go here
		Soldier.__init__(self, name, team, posx, posy, orientation, aggression)
		

	def observe(self):
		Soldier.observe(self)
		print "TalibanRifleman observe"

	def decide(self):
		Soldier.decide(self)
		print "TalibanRifleman Deciding"
	
	def act(self):
		Soldier.act(self)
		print "TalibanRifleman acting"

	def displaySoldier(self):
		Soldier.displaySoldier(self)


