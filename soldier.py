#!/usr/bin/python
from random import randint

class Soldier:
   'Common base class for all soldiers'
   soldierCount = 0

   def __init__(self, name, posx, posy, orientation, suppression, hits):
      self.name = name
      self.posx = posx
      self.posy = posy
      self.orientation = orientation
      self.suppression = suppression
      self.hits = hits
      Soldier.soldierCount += 1

   def attack(self, enemy):
      hit = randint(0,100)
      if hit > 50:
         print "successful hit"
         enemy.hits += 1
      else:
         print "shot misses"

   def observe(self):
      print "Observing"

   def decide(self):
      print "Deciding"

   def act(self):
      print "acting"
   
   def displayCount(self):
      print "Total Soldier %d" % Soldier.soldierCount

   def displaySoldier(self):
      print "Name: ", self.name,  ", Position:(", self.posx, ",", self.posy, "), orientation:", self.orientation, "hits:", self.hits

