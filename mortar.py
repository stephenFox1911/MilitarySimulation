#!/usr/bin/python
from soldier import Soldier
import math
import random

class Mortar(object):
    
    def __init__(self, maxAmmo=10, fireRate=1):
        self.maxAmmo = maxAmmo
        self.currentAmmo = maxAmmo

    def attack(self, posx, posy):

        #Adding error to intial landing position, which is posx and posy
        #If we want to we can change this to some other mathematical distribution
        landingX = posx + randint(-10, 10)
        landingY = posy + randint(-10, 10)

        #Actual radius of mortar damage; r1 = dead; r2 = heavy; r3 = light
        #7.5 foot radius
        r1 = 15
        #15 foot radius
        r2 = 30
        #30 foot radius
        r3 = 60

        heavySuppression = 90
        lightSuppression = 45

        #Looking for solider to hit
        for soldier in Soldier.soldiers:
            d = math.sqrt(math.pow((soldier.posx - landingX),2) - math.pow((soldier.posy - landingY),2))
            if d <= 5:
                soldier.isDead = True 
            if d >5 and d <=15:
                soldier.suppression += 5/d * heavySuppression
            if d >15 and d <=50:
                soldier.suppression += 5/d * lightSuppression

        #reduce ammo
        self.currentAmmo -= 1
