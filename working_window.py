#!/usr/bin/python
import sys
import gtk
import cairo
import random
import math
import glib
from soldier import Soldier
from usRifleman import USrifleman
from usMachineGunner import USmachineGunner
from talibanRifleman import TalibanRifleman
from talibanMachineGunner import TalibanMachineGunner
from usFireteamLeader import USfireteamLeader
from shotline import ShotLine
from cover import Cover
from mortar import Mortar
import csv

#Global Window Parameters
WIDTH = 1128
HEIGHT = 846
TIME_BETWEEN_FRAMES = 1 #in milliseconds

class SimArea(gtk.DrawingArea):

    def __init__(self, input_file):
        super(SimArea, self).__init__()

        #class variables
        self.inSim = False #whether or not the simulation is in progress
        self.input_file = input_file
        self.red_combatants = [] #list of all red soldier objects
        self.blue_combatants = [] #list of all blue soldiers objects
        self.red_casualties = []
        self.blue_casualties = []
        self.mortars = []
        self.shots = [] #list of all active ShotLine objects
        self.mortar_shots = []
        self.cover_objects = []
        self.mortar = None
        self.mortar_rate_of_fire = None
        self.count = 0
        #self.objectives = [(741,670), (799,153)]
        self.objectives = [(671,593), (799,153)]
        #self.objectives = [(750,350), (0,0)]
        self.reached_turn = False
        self.danger_close = False
        ######TEMP VARIABLES#####START
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.rLeft = False
        self.rRight = False
        ######TEMP VARIABLES#####END

        #sets the size of the drawing area
        self.set_size_request(WIDTH, HEIGHT)
        #event listener that determines how SimArea displays itself
        self.connect("expose-event", self.expose)
        self.init_sim()

    def on_timer(self):
        #called for each tick of the simulation
        #print self.count
        if self.inSim:
            if len(self.red_combatants) == 0 or len(self.blue_combatants) == 0:
                self.inSim == False
                #Soldier.output.write("END SIM")
                return True
            #check simulation processes
            if self.count%20 == 0:
                Soldier.output.write("Tick Number: "+str(self.count)+"\n")
                #randomly shuffle combatants for decision making process
                random.shuffle(self.red_combatants)
                random.shuffle(self.blue_combatants)
                self.observe()
                self.decide()
                self.act()
            self.updateSoldiers()
            self.checkObjectives()
            if self.mortar is not None and not self.danger_close and self.count%self.mortar_rate_of_fire==0 and self.mortar.currentAmmo > 0:
                landingX, landingY = self.mortar.attack(self.objectives[1])
                shot = MortarShot(landingX, landingY)
                self.mortar_shots.append(shot)
                for red in self.red_combatants:
                    d = math.sqrt(math.pow((red.posx - landingX),2) + math.pow((red.posy - landingY),2))
                    if d <= 30:
                        red.isDead = True
                        self.red_casualties.append(red)
                        Soldier.output.write("Mortar strike killed "+red.name+"\n")
                    if d >30 and d <=90:
                        red.suppression += 30#90
                    # if d >90 and d <=300:
                    #     red.suppression += 50
                self.red_combatants = [red for red in self.red_combatants if not red.isDead]
            self.queue_draw() #gtk function to draw all queued changes
            self.count += 1
            return True
        else:
            self.count += 1
            return False

    def checkObjectives(self):
        for blue in self.blue_combatants:
            d = math.hypot(blue.posx - blue.objectiveX, blue.posy - blue.objectiveY)
            if d < 60:
                blue.updateObjective(self.objectives[1][0], self.objectives[1][1])
        if self.danger_close:
            pass
            #TODO add mortar stuff


    def observe(self):
        for red in self.red_combatants:
            red.observe()
            red.findCover(self.cover_objects)
        for blue in self.blue_combatants:
            blue.observe()
            blue.findCover(self.cover_objects)

    def decide(self):
        for red in self.red_combatants:
            red.decide()
        for blue in self.blue_combatants:
            blue.decide()

    def act(self):
        for red in self.red_combatants:
            isShot, target, shotSuccess, misses = red.act()
            if isShot:
                if shotSuccess:
                    self.shots.append(ShotLine(red.posx, red.posy, target.posx, target.posy, shotSuccess))
                    self.blue_casualties.append(target)
                    self.blue_combatants.remove(target)
                for i in xrange(misses):
                    dx = red.posx - target.posx
                    dy = red.posy - target.posy
                    dist = math.hypot(dx, dy)
                    theta = math.atan2(dy, dx) + random.gauss(0,0.01)
                    new_x = -math.cos(theta) * dist + red.posx
                    new_y = -math.sin(theta) * dist + red.posy
                    self.shots.append(ShotLine(red.posx, red.posy, new_x, new_y, False))
        for blue in self.blue_combatants:
            isShot, target, shotSuccess, misses = blue.act()
            if isShot:
                if shotSuccess:
                    self.shots.append(ShotLine(blue.posx, blue.posy, target.posx, target.posy, shotSuccess))
                    self.red_casualties.append(target)
                    self.red_combatants.remove(target)
                for i in xrange(misses):
                    dx = blue.posx - target.posx
                    dy = blue.posy - target.posy
                    dist = math.hypot(dx, dy)
                    theta = math.atan2(dy, dx) + random.gauss(0,0.01)
                    new_x = -math.cos(theta) * dist + blue.posx
                    new_y = -math.sin(theta) * dist + blue.posy
                    self.shots.append(ShotLine(blue.posx, blue.posy, new_x, new_y, False))

    def updateSoldiers(self):
        for red in self.red_combatants:
            red.update()
        for blue in self.blue_combatants:
            blue.update()

    def init_sim(self):
        #initializes the simulation by reading all data from a csv
        with open(self.input_file, 'rb') as f:
            reader = csv.reader(f)
            input_list = list(reader)
        self.inSim = True

        for i,line in enumerate(input_list):
            if line[0] == 'bluer':
                blue = USrifleman("Blue Rifleman"+str(i), "blue", int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5]))
                blue.updateObjective(self.objectives[0][0], self.objectives[0][1])
                self.blue_combatants.append(blue)
            elif line[0] == 'bluem':
                blue = USmachineGunner("Blue MachineGunner"+str(i), "blue", int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5]))
                blue.updateObjective(self.objectives[0][0], self.objectives[0][1])
                self.blue_combatants.append(blue)
            elif line[0] == 'bluef':
                blue = USfireteamLeader("Blue Fireteam Leader"+str(i), "blue", int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5]))
                blue.updateObjective(self.objectives[0][0], self.objectives[0][1])
                self.blue_combatants.append(blue)
            elif line[0] == 'redr':
                self.red_combatants.append(TalibanRifleman("Red Rifleman"+str(i), "red", int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5])))
            elif line[0] == 'redm':
                self.red_combatants.append(TalibanMachineGunner("Red MachineGunner"+str(i), "red", int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5])))
            elif line[0] == 'mortar':
                self.mortar = Mortar(int(line[1]), int(line[2]))
                self.mortar_rate_of_fire = self.mortar.fireRate#TODO add conversion logic
            elif line[0] == 'cover':
                self.cover_objects.append(Cover(int(line[1]), int(line[2]), int(line[3]), int(line[4])))
            else:
                print "improper csv line: "
                print line

        glib.timeout_add(TIME_BETWEEN_FRAMES, self.on_timer) #Tick

    def expose(self, widget, event):
        #method to draw all objects
        cr = widget.window.cairo_create() #creates a cairo object (used for all drawing)

        if self.inSim:
            #sets the background of the window to be the satellite image of the battlefield
            pixbuf = gtk.gdk.pixbuf_new_from_file('GUI/bg.png')
            widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], pixbuf, 0, 0, 0,0)

            for red in self.red_casualties:
                self.draw_red_casualties(cr, red)
            for blue in self.blue_casualties:
                self.draw_blue_casualties(cr, blue)
            for red in self.red_combatants:
                self.draw_red_soldiers(cr, red)
            for blue in self.blue_combatants:
                self.draw_blue_soldiers(cr, blue)
            for mortar in self.mortars:
                self.draw_mortars(cr, mortar)
            for shot in self.shots:
                cr.set_line_width(1)
                if shot.hit:
                    cr.set_source_rgba(0, 0, 0, shot.alpha) #shot is black if hit
                else:
                    cr.set_source_rgba(1, 1, 1, shot.alpha) #white if miss
                cr.move_to(shot.source_x, shot.source_y)
                cr.line_to(shot.target_x, shot.target_y)
                if shot.hit:
                    cr.arc(shot.target_x, shot.target_y, 7, 0, math.pi*2)
                cr.stroke()
                shot.degrade() #increases the transparency for future ticks
            self.shots = [shot for shot in self.shots if shot.alpha > 0]
            for shot in self.mortar_shots:
                if shot.detonate:
                    cr.set_source_rgba(1,1,1,0.25)
                    #cr.arc(shot.posx, shot.posy, 300, 0, 2*math.pi) #TODO change 5 to proper distance -- implement in mortarshot?
                    #cr.fill()
                    #cr.set_source_rgba(0, 0, 0, 0.25)
                    cr.set_source_rgba(1,1,1,0.35)
                    cr.arc(shot.posx, shot.posy, 90, 0, 2*math.pi)
                    cr.fill()
                    cr.set_source_rgba(1,1,1,0.6)
                    cr.arc(shot.posx, shot.posy, 30, 0, 2*math.pi)
                    cr.fill()
                else:
                    cr.set_line_width(1)
                    cr.set_source_rgb(0,0,0)
                    cr.arc(shot.posx, shot.posy, 3, 0, 2*math.pi)
                    cr.stroke_preserve()
                    cr.set_source_rgb(1,1,1)
                    cr.fill()
                shot.update()
            self.mortar_shots = [shot for shot in self.mortar_shots if shot.detonation_time > 0]
            #for cover in self.cover_objects:
                #cr.set_source_rgb(0,1,0)
                #cr.arc(cover.posx, cover.posy, 3, 0, math.pi*2)
                #cr.stroke()
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


    '''///////////DRAW METHODS///////////'''
    def draw_blue_soldiers(self, cr, blue):
        if blue.__class__.__name__ is 'USrifleman':
            self.draw_blue_rifle(cr, blue)
        elif blue.__class__.__name__ is 'USmachineGunner':
            self.draw_blue_mg(cr, blue)
        elif blue.__class__.__name__ is 'USfireteamLeader':
            self.draw_blue_ftl(cr, blue)
        else:
            assert False, 'Type checking of soldiers is not working'
    def draw_blue_rifle(self, cr, blue):
        cr.set_line_width(1)
        cr.set_source_rgb(0, 0, 0)
        cr.arc(blue.posx, blue.posy, 5, 0, 2*math.pi)
        cr.stroke_preserve()
        cr.set_source_rgb(0, 0, 1)
        cr.fill()
        cr.set_source_rgb(0, 0, 0)
        cr.move_to(blue.posx, blue.posy)
        orientation = (blue.orientation - 2)
        cr.line_to(blue.posx + (5*math.cos(orientation*-math.pi/4)), blue.posy + (5*math.sin(-orientation*-math.pi/4)))
        cr.set_line_width(2)
        cr.stroke()
    def draw_blue_mg(self, cr, blue):
        cr.set_line_width(1)
        cr.set_source_rgb(0, 0, 0)
        cr.arc(blue.posx, blue.posy, 5, 0, 2*math.pi)
        cr.stroke_preserve()
        cr.set_source_rgb(0, 0, 1)
        cr.fill()
        cr.set_source_rgb(0, 0, 0)
        cr.move_to(blue.posx, blue.posy)
        orientation = (blue.orientation - 2)
        cr.set_source_rgb(1, 1, 1)
        cr.line_to(blue.posx + (5*math.cos(orientation*-math.pi/4)), blue.posy + (5*math.sin(-orientation*-math.pi/4)))
        cr.set_line_width(2)
        cr.stroke()
    def draw_blue_ftl(self, cr, blue):
        cr.set_line_width(1)
        cr.set_source_rgb(1, 1, 1)
        cr.arc(blue.posx, blue.posy, 5, 0, 2*math.pi)
        cr.stroke_preserve()
        cr.set_source_rgb(0, 0, 1)
        cr.fill()
        cr.set_source_rgb(0, 0, 0)
        cr.move_to(blue.posx, blue.posy)
        orientation = (blue.orientation - 2)
        cr.line_to(blue.posx + (5*math.cos(orientation*-math.pi/4)), blue.posy + (5*math.sin(-orientation*-math.pi/4)))
        cr.set_line_width(2)
        cr.stroke()
    def draw_red_soldiers(self, cr, red):
        if red.__class__.__name__ is 'TalibanRifleman':
            self.draw_red_rifle(cr, red)
        elif red.__class__.__name__ is 'TalibanMachineGunner':
            self.draw_red_mg(cr, red)
        else:
            assert False, 'Type checking of soldiers is not working'
    def draw_red_rifle(self, cr, red):
        cr.set_line_width(1) #border width
        cr.set_source_rgb(0, 0, 0) #border color black
        cr.arc(red.posx, red.posy, 5, 0, 2*math.pi) #border shape and position (circle)
        cr.stroke_preserve() #draw border
        cr.set_source_rgb(1, 0, 0) #set color to red
        cr.fill() #fill border
        cr.set_source_rgb(0, 0, 0) #set color to black
        cr.move_to(red.posx, red.posy) #move to center of circle
        orientation = (red.orientation - 2)
        cr.line_to(red.posx + (5*math.cos(orientation*-math.pi/4)), red.posy + (5*math.sin(-orientation*-math.pi/4))) #create line from center of circle to border in direction of soldier orientation
        cr.set_line_width(2)
        cr.stroke() #draw line indicating soldier orientation
    def draw_red_mg(self, cr, red):
        cr.set_line_width(1) #border width
        cr.set_source_rgb(0, 0, 0) #border color black
        cr.arc(red.posx, red.posy, 5, 0, 2*math.pi) #border shape and position (circle)
        cr.stroke_preserve() #draw border
        cr.set_source_rgb(1, 0, 0) #set color to red
        cr.fill() #fill border
        cr.set_source_rgb(1, 1, 1) #set color to black
        cr.move_to(red.posx, red.posy) #move to center of circle
        orientation = (red.orientation - 2)
        cr.line_to(red.posx + (5*math.cos(orientation*-math.pi/4)), red.posy + (5*math.sin(-orientation*-math.pi/4))) #create line from center of circle to border in direction of soldier orientation
        cr.set_line_width(2)
        cr.stroke() #draw line indicating soldier orientation
    def draw_blue_casualties(self, cr, blue):
        cr.set_line_width(1)
        cr.set_source_rgb(0, 0, 0)
        cr.arc(blue.posx, blue.posy, 5, 0, 2*math.pi)
        cr.stroke_preserve()
        cr.set_source_rgb(0,0,0.2)
        cr.fill()
    def draw_red_casualties(self, cr, red):
        cr.set_line_width(1) #border width
        cr.set_source_rgb(0, 0, 0) #border color black
        cr.arc(red.posx, red.posy, 5, 0, 2*math.pi) #border shape and position (circle)
        cr.stroke_preserve() #draw border
        cr.set_source_rgb(.2, 0, 0)
        cr.fill()
    def draw_mortars(self, cr, mortar):
        cr.set_line_width(1)
        cr.set_source_rgb(0, 0, 0)
        cr.arc(mortar.posx, mortar.posy, 5, 0, 2*math.pi)
        cr.stroke_preserve()
        cr.set_source_rgb(0, 0, 1)
        cr.fill()
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(2)
        cr.move_to(mortar.posx, mortar.posy)
        cr.line_to(mortar.posx + 5, mortar.posy)
        cr.stroke()
        cr.move_to(mortar.posx, mortar.posy)
        cr.line_to(mortar.posx - 5, mortar.posy)
        cr.stroke()
        cr.move_to(mortar.posx, mortar.posy)
        cr.line_to(mortar.posx, mortar.posy + 5)
        cr.stroke()
        cr.move_to(mortar.posx, mortar.posy)
        cr.line_to(mortar.posx, mortar.posy - 5)
        cr.stroke()

class Simulation(gtk.Window):

    def __init__(self, input_file):
        #inherits from the gtk.Window class
        super(Simulation, self).__init__()

        self.set_title('Simulation')
        self.set_size_request(WIDTH, HEIGHT)
        #doesn't allow the user to resize the window
        self.set_resizable(False)
        #centers the window on the screen
        self.set_position(gtk.WIN_POS_CENTER)

        #TODO comment
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK)

        #create a SimArea object
        self.sim_area = SimArea(input_file)
        #create a key press event listener
        self.connect("key-press-event", self.on_key_down)#TODO TEMP?

        self.connect("button-press-event", self.on_mouse)

        #adds the SimArea to the Simulation window
        self.add(self.sim_area)

        #creates an event listener that kills the process when the window is detroyed
        self.connect("destroy", gtk.main_quit)
        #displays all gtk elements
        self.show_all()

    #####TEMP METHODS?######START
    def on_key_down(self, widget, event):
        if event.type == gtk.gdk.BUTTON_PRESS:
            print "("+str(event.x)+","+str(event.y)+")"
        else:
            key = event.keyval

    def on_mouse(self, widget, event):
        print "("+str(event.x)+","+str(event.y)+")"
    #####TEMP METHODS?######END

class MortarShot:
    #def __init__(self, s_x, s_y, t_x, t_y):
    def __init__(self, t_x, t_y):
        '''
        @summary: a class to hold data for each mortar shot fired
        @param source_x: the x-coord for the source mortar
        @param source_y: the y-coord for the source mortar
        @param target_x: the x-coord for the target point
        @param target_y: the y-coord for the target point
        '''
        self.detonate = True #whether or not the mortar shot has detonated
        self.detonation_time = 15 * TIME_BETWEEN_FRAMES #1.5 seconds for explosion animation
        #self.posx = s_x #x-position of mortar shot
        #self.posy = s_y #y-position of mortar shot
        #self.t_x = t_x #x-position of mortar target
        #self.t_y = t_y #y-position of mortar target
        self.posx = t_x
        self.posy = t_y
        #self.time_in_air = 20000
        # dx = s_x - t_x
        # dy = s_y - t_y
        # dist = math.hypot(dx, dy)
        # ticks_in_air = self.time_in_air / TIME_BETWEEN_FRAMES
        # magnitude = dist / ticks_in_air
        # theta = math.atan2(dy, dx)
        # self.delta_x = math.cos(theta) * magnitude
        # self.delta_y = math.sin(theta) * magnitude

    def update(self):
        if not self.detonate:
            self.posx -= self.delta_x
            self.posy -= self.delta_y
            self.time_in_air -= TIME_BETWEEN_FRAMES
            if self.time_in_air <= 0:
                self.detonate = True
        else:
            self.detonation_time -= TIME_BETWEEN_FRAMES



if __name__ == "__main__":
    Simulation(sys.argv[1])
    gtk.main()
