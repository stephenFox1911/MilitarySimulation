#!/usr/bin/python
from soldier import Soldier

class Mortar(object):
    
    def __init__(self, maxAmmo=10, fireRate=1):
        self.maxAmmo = maxAmmo
        self.currentAmmo = maxAmmo

    def attack(self, posx, posy):
        #generate an amount of aiming error for x and y

        #calculate a kill, heavy suppression, and weak suppression radius

        #find which soldiers were affected
        for soldier in Soldier.soldiers:
            #use soldier.posx and soldier.posy to get it's position
            #update soldier.suppression when necessary
            #I haven't figured out how to represent death yet. 

        self.currentAmmo -= 1
        
        