#!/usr/bin/python
from soldier import Soldier

class Mortar(object):
    
    def __init__(self, maxAmmo=10, fireRate=1):
        self.maxAmmo = maxAmmo
        self.currentAmmo = maxAmmo

    def attack(self, posx, posy):

        #Adding error to intial landing position, which is posx and posy
        landingX = posx + randint(-10, 10)
        landingY = posy + randint(-10, 10)

        #Actual radius of mortar damage; r1 = dead; r2 = heavy; r3 = light
        r1 = 5
        r2 = 15
        r3 = 50

        heavySuppression = 90
        lightSuppression = 45

        #Looking for solider to hit
        for soldier in Soldier.soldiers:
            if soldier.posx < landingX + r1 and soldier.posx > landingX - r1 and soldier.posy < landingY + r1 and soldier.posy > landingY - r1:
                soldier.isDead = True
            if soldier.posx < landingX + r2 and soldier.posx > landingX - r2 and soldier.posy < landingY + r2 and soldier.posy > landingY - r2:
                soldier.suppression += 5/soldier.posx * heavySuppression
            if soldier.posx < landingX + r3 and soldier.posx > landingX - r3 and soldier.posy < landingY + r3 and soldier.posy > landingY - r3:
                soldier.suppression +=  5/soldier.posx * lightSuppression
            else:
                soldier.suppression = soldier.suppression

        #reduce ammo
        self.currentAmmo -= 1