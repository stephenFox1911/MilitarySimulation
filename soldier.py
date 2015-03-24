#!/usr/bin/python
from random import randint

class Soldier:
	'Common base class for all soldiers'
	soldierCount = 0
	#list of all soldiers
	soldiers = []

	'Common base class for all soldiers'
	soldierCount = 0

	def __init__(self, name, team, posx, posy, orientation, aggression):
		self.name = name
		self.team = team
		self.posx = posx
		self.posy = posy
		#orientation 0=north, 2=east, 4=south, 6=west. Plus inbetweens
		self.orientation = orientation
		self.suppression = 0
		#This value should be between -50 and 50 
		self.aggression = aggression
		self.state = "Neutral"
		self.coverQuality = 0
		self.currentAction = "None"
		self.hits = 0
		self.enemyList = []
		Soldier.soldierCount += 1
		Soldier.soldiers.append(self)

	def attack(self, enemy, quality):
		shotMod = quality - self.suppression - enemy.coverQuality
		hit = randint(0,100) + shotMod
		if hit > 100:
			print "successful hit"
			enemy.hits += 1
		else:
			print "shot misses"
			enemy.suppression += 10

	def observe(self):
		#decrement suppression
		self.suppression -= 5

		#reset enemy list
		self.enemyList = []
		
		print self.name + " Observing at orientation " + str(self.orientation) 

		point1 = [self.posx, self.posy]
		point2 = [self.posx, self.posy]

		if self.orientation == 0:
			while point1[1] >= 0:
				#update searching points
				point1[1] -= 1
				if point1[0] == 0:
					pass
				else :
					point1[0] -= 1

				point2[1] -= 1
				if point2[0] == 100:
					pass
				else :
					point2[0] += 1

				#search inbetween these points for an enemy
				for x in xrange(point1[0],point2[0]):
					y = point1[1]
					for s in Soldier.soldiers:
						if (s.posx == x) & (s.posy == y) & (s.team != self.team):
							self.enemyList.append(s)
							print("Found enemy: " + s.name)

		elif self.orientation == 1:
			while (point2[0] < 100) | (point1[1] > 0):
				#update searching points
				if point1[1] == 0:
					pass
				else:
					point1[1] -= 1

				if point2[0] == 100:
					pass
				else:
					point2[0] += 1

				#search inbetween the points for an enemy
				for x in xrange(point1[0],point2[0]):
					y = point1[1]
					for s in Soldier.soldiers:
						if (s.posx == x) & (s.posy == y) & (s.team != self.team):
							self.enemyList.append(s)
							print("Found enemy: " + s.name + " AT: " + str(x) + " " + str(y))

				for y in xrange(point1[1],point2[1]):
					x = point2[0]
					for s in Soldier.soldiers:
						if (s.posx == x) & (s.posy == y) & (s.team != self.team):
							self.enemyList.append(s)
							print("Found enemy: " + s.name + " AT: " + str(x) + " " + str(y))

		elif self.orientation == 2:
			while point1[0] <= 100:
				#update searching points
				point1[0] += 1
				if point1[1] == 0:
					pass
				else :
					point1[1] -= 1

				point2[0] += 1
				if point2[1] == 100:
					pass
				else :
					point2[1] += 1

				#search inbetween these points for an enemy
				for y in xrange(point1[1],point2[1]):
					x = point1[0]
					for s in Soldier.soldiers:
						if (s.posx == x) & (s.posy == y) & (s.team != self.team):
							self.enemyList.append(s)
							print("Found enemy: " + s.name)

		elif self.orientation == 3:
			while (point2[1] < 100) | (point1[0] < 100):
				#update searching points
				if point1[0] == 100:
					pass
				else:
					point1[0] += 1

				if point2[1] == 100:
					pass
				else:
					point2[1] += 1

				#search inbetween the points for an enemy
				for x in xrange(point2[0],point1[0]):
					y = point2[1]
					for s in Soldier.soldiers:
						if (s.posx == x) & (s.posy == y) & (s.team != self.team):
							self.enemyList.append(s)
							print("Found enemy: " + s.name)

				for y in xrange(point1[1],point2[1]):
					x = point1[0]
					for s in Soldier.soldiers:
						if (s.posx == x) & (s.posy == y) & (s.team != self.team):
							self.enemyList.append(s)
							print("Found enemy: " + s.name)

		elif self.orientation == 4:
			while point1[1] <= 100:
				#update searching points
				point1[1] += 1
				if point1[0] == 100:
					pass
				else :
					point1[0] += 1

				point2[1] += 1
				if point2[0] == 0:
					pass
				else :
					point2[0] -= 1

				#search inbetween these points for an enemy
				for x in xrange(point2[0],point1[0]):
					y = point1[1]
					for s in Soldier.soldiers:
						if (s.posx == x) & (s.posy == y) & (s.team != self.team):
							self.enemyList.append(s)
							print("Found enemy: " + s.name)

		elif self.orientation == 5:
			while (point2[0] > 0) | (point1[1] < 100):
				#update searching points
				if point1[1] == 100:
					pass
				else:
					point1[1] += 1

				if point2[0] == 0:
					pass
				else:
					point2[0] -= 1

				#search inbetween the points for an enemy
				for x in xrange(point2[0],point1[0]):
					y = point2[1]
					for s in Soldier.soldiers:
						if (s.posx == x) & (s.posy == y) & (s.team != self.team):
							self.enemyList.append(s)
							print("Found enemy: " + s.name)

				for y in xrange(point2[1],point1[1]):
					x = point1[0]
					for s in Soldier.soldiers:
						if (s.posx == x) & (s.posy == y) & (s.team != self.team):
							self.enemyList.append(s)
							print("Found enemy: " + s.name)

		elif self.orientation == 6:
			while point1[0] >= 0:
				#update searching points
				point2[0] -= 1
				if point2[1] == 0:
					pass
				else :
					point2[1] -= 1

				point1[0] -= 1
				if point1[1] == 100:
					pass
				else :
					point1[1] += 1

				#search inbetween these points for an enemy
				for y in xrange(point2[1],point1[1]):
					x = point1[0]
					for s in Soldier.soldiers:
						if (s.posx == x) & (s.posy == y) & (s.team != self.team):
							self.enemyList.append(s)
							print("Found enemy: " + s.name)

		elif self.orientation == 7:
			while (point2[1] > 0) | (point1[0] > 0):
				#update searching points
				if point1[0] == 0:
					pass
				else:
					point1[0] -= 1

				if point2[1] == 0:
					pass
				else:
					point2[1] -= 1

				#search inbetween the points for an enemy
				for x in xrange(point1[0],point2[0]):
					y = point2[1]
					for s in Soldier.soldiers:
						if (s.posx == x) & (s.posy == y) & (s.team != self.team):
							self.enemyList.append(s)
							print("Found enemy: " + s.name)

				for y in xrange(point2[1],point1[1]):
					x = point1[0]
					for s in Soldier.soldiers:
						if (s.posx == x) & (s.posy == y) & (s.team != self.team):
							self.enemyList.append(s)
							print("Found enemy: " + s.name)

	def decide(self):
		
		# Higher numbers represent the "more aggressive" decision
		decisionInt = randint(0,100) + self.aggression - self.suppression
		
		if self.state == "Neutral" :			
			# 30% chance that the soldier chooses to attack (before modifiers)
			if decisionInt >= 66 & len(self.enemyList) > 0 :
				self.state = "Engage"
				#Logic for choosing different types of attacks goes here
				self.currentAction = "SimpleAttack"
			# 30% chance (or 60% if no targets)
			elif decisionInt >= 33 :
				self.state = "Move"
				self.currentAction = "Move"
					
			else :
				self.state = "Cover"
				self.currentAction = "Cover"
		
		elif self.state == "Cover" :
			# 30% chance that the soldier chooses to attack (before modifiers)
			if decisionInt >= 66 & len(self.enemyList) > 0 :
				self.state = "Engage"
				#Logic for choosing different types of attacks goes here
				self.currentAction = "SimpleAttack"
			# 30% chance (or 60% if no targets)
			elif decisionInt >= 33 :
				self.state = "Move"
				self.currentAction = "Move"
					
			else :
				self.state = "Cover"
				self.currentAction = "Cover"
		
		elif self.state == "Engage" :
			# 30% chance that the soldier chooses to attack (before modifiers)
			if decisionInt >= 66 & len(self.enemyList) > 0 :
				self.state = "Engage"
				#Logic for choosing different types of attacks goes here
				self.currentAction = "SimpleAttack"
			# 30% chance (or 60% if no targets)
			elif decisionInt >= 33 :
				self.state = "Move"
				self.currentAction = "Move"					
			else :
				self.state = "Cover"
				self.currentAction = "Cover"
		
		elif self.state == "Move" :
			# 10% chance that the soldier chooses to attack (before modifiers)
			if decisionInt >= 90 & len(self.enemyList) > 0 :
				self.state = "Engage"
				#Logic for choosing different types of attacks goes here
				self.currentAction = "SimpleAttack"
			# 10% chance
			elif decisionInt <= 10 :
				self.state = "Cover"
				self.currentAction = "Cover"
					
			else :
				self.state = "Move"
				self.currentAction = "Move"
				
	def act(self):
		if self.currentAction == "SimpleAttack" :
			print self.name + " Simple Attack"
			self.coverQuality -= 10
			#Finds target with least amount of cover and fires one shot
			target = None
			worstCover = 1000
			
			for enemy in self.enemyList :
				if enemy.coverQuality <= worstCover :
					target = enemy
			
			#Attack enemy once
			shotQuality = 50
			self.attack(target, shotQuality)

		elif self.currentAction == "Move" :
			print self.name + " Move"
			self.coverQuality = 0
			self.orientation = randint(0,7)

		elif self.currentAction == "Cover" :
			print self.name + " Taking Cover"
			self.coverQuality = 30
			
	def displaySoldier(self):
		print "Name: ", self.name,  ", Position:(", self.posx, ",", self.posy, "), orientation:", self.orientation
	
	def findCover(self, coverList):
		#returns the three closest pieces of cover
		minDistances = [99999, 99998, 99997]
		closestCover = [None, None, None]
		
		for c in coverList:
			distance = math.hypot(c.center[0] - self.posx, c.center[1] - self.posy)
			currentMax = max(minDistances)
			if distance < currentMax :
				index = minDistances.index(currentMax)
				minDistances[index] = distance
				closestCover[index] = c
		return closestCover