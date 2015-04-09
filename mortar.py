#!/usr/bin/python
from soldier import Soldier
import math
import random

class Mortar(object):
    
    def __init__(self, maxAmmo=10, fireRate=1):
        self.maxAmmo = maxAmmo
        self.currentAmmo = maxAmmo
        self.fireRate = fireRate

    def attack(self, target):

        #Adding error to intial landing position, which is posx and posy
        #If we want to we can change this to some other mathematical distribution
        landingX = target[0] + random.randint(-20, 20)
        landingY = target[1] + random.randint(-20, 20)

        # #Actual radius of mortar damage; r1 = dead; r2 = heavy; r3 = light
        # #7.5 foot radius
        # r1 = 5
        # #15 foot radius
        # r2 = 15
        # #30 foot radius
        # r3 = 50

        # heavySuppression = 90
        # lightSuppression = 45

        # #Looking for solider to hit
        # for soldier in Soldier.soldiers:
        #     d = math.sqrt(math.pow((soldier.posx - landingX),2) - math.pow((soldier.posy - landingY),2))
        #     if d <= r1:
        #         soldier.isDead = True 
        #     if d >r1 and d <=r2:
        #         soldier.suppression += 5/d * heavySuppression
        #     if d >r2 and d <=r3:
        #         soldier.suppression += 5/d * lightSuppression

        #reduce ammo
        self.currentAmmo -= 1
        return (landingX, landingY)
