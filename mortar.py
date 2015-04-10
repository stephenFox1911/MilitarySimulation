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
        landingX = target[0] + random.randint(-45, 45)
        landingY = target[1] + random.randint(-45, 45)

        #reduce ammo
        self.currentAmmo -= 1
        return (landingX, landingY)
