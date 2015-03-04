#!/usr/bin/python

from soldier import Soldier

class USrifleman(Soldier):
	'USrifleman with M16'

	def __init__(self, name, team, posx, posy, orientation, suppression, hits, test):
		# subclass specific arguments go here
		Soldier.__init__(self, name, team, posx, posy, orientation, suppression, hits)
		self.test = test

	def observe(self):
		Soldier.observe(self)
		print "USrifleman observe"

	def decide(self):
		Soldier.decide(self)
		print "USrifleman Deciding"
	
	def act(self):
		Soldier.act(self)
		print "USrifleman acting"

	def displaySoldier(self):
		Soldier.displaySoldier(self)
		print "\ttest: ",self.test

