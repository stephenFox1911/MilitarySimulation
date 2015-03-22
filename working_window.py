#!/usr/bin/python

# ZetCode PyGTK tutorial 
#
# This is a simple snake game
# clone
#
# author: jan bodnar
# website: zetcode.com 
# last edited: February 2009

import sys
import gtk
import cairo
import random
import math
import glib
from soldier import Soldier
from usRifleman import USrifleman
from talibanRifleman import TalibanRifleman
import shotline

#Global Window Parameters
WIDTH = 800
HEIGHT = 700

class SimArea(gtk.DrawingArea):

    def __init__(self):
        super(SimArea, self).__init__()

        #class variables
        self.inSim = False #whether or not the simulation is in progress
        self.red_combatants = [] #list of all red soldier objects
        self.blue_combatants = [] #list of all blue soldiers objects
        self.shots = [] #list of all active ShotLine objects
        ######TEMP VARIABLES#####START
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.rLeft = False
        self.rRight = False
        ######TEMP VARIABLES#####END

        #sets the size of the drawing area
        self.set_size_request(WIDTH, HEIGHT)#TODO change according to new picture
        #event listener that determines how SimArea displays itself
        self.connect("expose-event", self.expose)
        self.init_sim(2, 3)#TODO TEMP

    def on_timer(self):
        #called for each tick of the simulation
        if self.inSim:
            #check simulation processes
            #self.observe() #TODO implement
            #self.orient()
            #self.decide() #TODO implement
            #self.act() #TODO implement
            self.move()#TODO TEMP?
            self.queue_draw() #gtk function to draw all queued actions
            return True
        else:
            return False

    def init_sim(self, red, blue):
        #initializes the simulation bby reading all data from a csv
        #TODO reimplement to read info from csv
        self.inSim = True
        for i in xrange(red):
            self.red_combatants.append(TalibanRifleman("red"+str(i), 50+i*10, 50+i*10, 0, 0, 0, "TalibanRifleman"))
        for i in xrange(blue):
            self.blue_combatants.append(USrifleman("blue"+str(i), 400+i*10, 400+i*10, 0, 0, 0, "USrifleman"))

        glib.timeout_add(10, self.on_timer)

    def expose(self, widget, event):
        #method to draw all objects
        cr = widget.window.cairo_create() #creates a cairo object (used for all drawing)

        if self.inSim:
            #sets the background of the window to be the satellite image of the battlefield
            pixbuf = gtk.gdk.pixbuf_new_from_file('GUI/temp.png')
            widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], pixbuf, 0, 0, 0,0)

            for red in self.red_combatants:
                cr.set_line_width(1) #border width
                cr.set_source_rgb(0, 0, 0) #border color black
                cr.arc(red.posx, red.posy, 5, 0, 2*math.pi) #border shape and position (circle)
                cr.stroke_preserve() #draw border
                cr.set_source_rgb(1, 0, 0) #set color to red
                cr.fill() #fill border
                cr.set_source_rgb(0, 0, 0) #set color to black
                cr.move_to(red.posx, red.posy) #move to center of circle
                cr.line_to(red.posx + (5*math.cos(red.orientation)), red.posy + (5*math.sin(red.orientation))) #create line from center of circle to border in direction of soldier orientation
                cr.set_line_width(2)
                cr.stroke() #draw line indicating soldier orientation
            for blue in self.blue_combatants:
                cr.set_line_width(1)
                cr.set_source_rgb(0, 0, 0)
                cr.arc(blue.posx, blue.posy, 5, 0, 2*math.pi)
                cr.stroke_preserve()
                cr.set_source_rgb(0, 0, 1)
                cr.fill()
                cr.set_source_rgb(0, 0, 0)
                cr.move_to(blue.posx, blue.posy)
                cr.line_to(blue.posx + (5*math.cos(blue.orientation)), blue.posy + (5*math.sin(blue.orientation)))
                cr.set_line_width(2)
                cr.stroke()
            for shot in self.shots:
                cr.set_line_width(2)
                if shot.hit:
                    cr.set_source_rgba(0, 0, 0, shot.alpha) #shot is black if hit
                else:
                    cr.set_source_rgba(1, 1, 1, shot.alpha) #white if miss
                cr.move_to(shot.source_x, shot.source_y)
                cr.line_to(shot.target_x, shot.target_y)
                cr.stroke()
                shot.degrade() #increases the transparency for future ticks
            self.shots = [shot for shot in self.shots if shot.alpha > 0]
        else:
            self.sim_over(cr)

    def sim_over(self, cr):
        #TODO currently an unused method, may use later though
        w = self.allocation.width / 2
        h = self.allocation.height / 2

        (x, y, width, height, dx, dy) = cr.text_extents("Simulation Over")

        cr.set_source_rgb(65535, 65535, 65535)
        cr.move_to(w - width/2, h)
        cr.show_text("Simulation Over")
        self.inSim = False

    def move(self): #TODO TEMP: implements temporary keyboard movement
        if self.left:
            for red in self.red_combatants:
                red.posx -= 1
            for blue in self.blue_combatants:
                blue.posx -= 1

        if self.right: 
            for red in self.red_combatants:
                red.posx += 1
            for blue in self.blue_combatants:
                blue.posx += 1

        if self.up:
            for red in self.red_combatants:
                red.posy -= 1
            for blue in self.blue_combatants:
                blue.posy -= 1

        if self.down:
            for red in self.red_combatants:
                red.posy += 1
            for blue in self.blue_combatants:
                blue.posy += 1

        if self.rRight:
            for red in self.red_combatants:
                red.orientation -= 0.1
            for blue in self.blue_combatants:
                blue.orientation += 0.1

        if self.rLeft:
            for red in self.red_combatants:
                red.orientation += 0.1
            for blue in self.blue_combatants:
                blue.orientation -= 0.1

    #####TEMP METHODS?######START
    def on_key_down(self, event):
        key = event.keyval
        if key == gtk.keysyms.a:
            self.left = True
        elif key == gtk.keysyms.d:
            self.right = True
        elif key == gtk.keysyms.w:
            self.up = True
        elif key == gtk.keysyms.s:
            self.down = True
        elif key == gtk.keysyms.q:
            self.rLeft = True
        elif key == gtk.keysyms.e:
            self.rRight = True
        elif key == gtk.keysyms._1:
            b = self.blue_combatants[0]
            r = self.red_combatants[0]
            shot = ShotLine(b.posx, b.posy, r.posx, r.posy, True)
            self.shots.append(shot)
        elif key == gtk.keysyms._2:
            b = self.blue_combatants[1]
            r = self.red_combatants[1]
            shot = ShotLine(b.posx, b.posy, r.posx, r.posy, False)
            self.shots.append(shot)
        elif key == gtk.keysyms._3:
            b = self.blue_combatants[0]
            r = self.red_combatants[0]
            shot = ShotLine(r.posx, r.posy, b.posx, b.posy, False)
            self.shots.append(shot)
        elif key == gtk.keysyms._4:
            b = self.blue_combatants[1]
            r = self.red_combatants[1]
            shot = ShotLine(r.posx, r.posy, b.posx, b.posy, True)
            self.shots.append(shot)

    def on_key_up(self, event):
        key = event.keyval
        if key == gtk.keysyms.a:
            self.left = False
        elif key == gtk.keysyms.d:
            self.right = False
        elif key == gtk.keysyms.w:
            self.up = False
        elif key == gtk.keysyms.s:
            self.down = False
        elif key == gtk.keysyms.q:
            self.rLeft = False
        elif key == gtk.keysyms.e:
            self.rRight = False
    #####TEMP METHODS?######END

class Simulation(gtk.Window):

    def __init__(self):
        #inherits from the gtk.Window class
        super(Simulation, self).__init__()

        self.set_title('Simulation')
        self.set_size_request(WIDTH, HEIGHT)
        #doesn't allow the user to resize the window
        self.set_resizable(False)
        #centers the window on the screen
        self.set_position(gtk.WIN_POS_CENTER)

        #create a SimArea object
        self.sim_area = SimArea()
        #create a key press event listener
        self.connect("key-press-event", self.on_key_down)#TODO TEMP?
        #create a key release event listener
        self.connect("key-release-event", self.on_key_up)#TODO TEMP?
        #adds the SimArea to the Simulation window
        self.add(self.sim_area)

        #creates an event listener that kills the process when the window is detroyed
        self.connect("destroy", gtk.main_quit)
        #displays all gtk elements
        self.show_all()

    #####TEMP METHODS?######START
    def on_key_down(self, widget, event):
        key = event.keyval
        self.sim_area.on_key_down(event)

    def on_key_up(self, widget, event):
        key = event.keyval
        self.sim_area.on_key_up(event)
    #####TEMP METHODS?######END

if __name__ == "__main__":
    Simulation()
    gtk.main()
