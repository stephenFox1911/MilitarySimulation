#!/usr/bin/python
from random import randint

class Soldier:
   'Common base class for all soldiers'
   soldierCount = 0
   #list of all soldiers
   soldiers = []

   def __init__(self, name, team, posx, posy, orientation, suppression, hits):
      self.name = name
      self.team = team
      self.posx = posx
      self.posy = posy
      #orientation 0=north, 2=east, 4=south, 6=west. Plus inbetweens
      self.orientation = orientation
      self.suppression = suppression
      self.hits = hits
      self.enemyList = []
      Soldier.soldierCount += 1
      Soldier.soldiers.append(self)

   def attack(self, enemy, quality):
      shotMod = quality - self.suppression 
      hit = randint(0,100) + shotMod
      if hit > 100:
         print "successful hit"
         enemy.hits += 1
      else:
         print "shot misses"
         enemy.suppression += 10

   def observe(self):
      print "Observing"
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
                     print("Found enemy: " + s.name)

            for y in xrange(point1[1],point2[1]):
               x = point2[0]
               for s in Soldier.soldiers:
                  if (s.posx == x) & (s.posy == y) & (s.team != self.team):
                     self.enemyList.append(s)
                     print("Found enemy: " + s.name)

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
      print "Deciding"

   def act(self):
      print "acting"
   
   def displayCount(self):
      print "Total Soldier %d" % Soldier.soldierCount

   def displaySoldier(self):
      print "Name: ", self.name,  ", Position:(", self.posx, ",", self.posy, "), orientation:", self.orientation, "hits:", self.hits

