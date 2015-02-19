#!/usr/bin/python

from soldier import Soldier

class TalibanRifleman(Soldier):
	'USrifleman with M16'

	def __init__(self, name, posx, posy, orientation, suppression, hits, test):
		# subclass specific arguments go here
		Soldier.__init__(self, name, posx, posy, orientation, suppression, hits)
		self.test = test

	def observe(self):
		print "TalibanRifleman observe"

	def decide(self):
		print "TalibanRifleman Deciding"
	
	def act(self):
		print "TalibanRifleman acting"

	def displaySoldier(self):
		Soldier.displaySoldier(self)
		print "\ttest: ",self.test

