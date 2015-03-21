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
import glib


WIDTH = 740
HEIGHT = 680
DOT_SIZE = 20
ALL_DOTS = WIDTH * HEIGHT / (DOT_SIZE * DOT_SIZE)
RAND_POS = 26

x = [0] * ALL_DOTS
y = [0] * ALL_DOTS


class SimArea(gtk.DrawingArea):

    def __init__(self):
        super(SimArea, self).__init__()

        #self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0, 0))
        self.set_size_request(773, 571)

        self.connect("expose-event", self.expose)
 
        self.init_game()

    def on_timer(self):

        if self.inGame:
            self.check_apple()
            self.check_collision()
            self.move()
            self.queue_draw()
            return True
        else:
            return False
    
    def init_game(self):

        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.inGame = True
        self.dots = 3

        for i in range(self.dots):
            x[i] = 50 - i * 10
            y[i] = 50
        
        try:
            self.dot = cairo.ImageSurface.create_from_png("GUI/blue.png")
            self.head = cairo.ImageSurface.create_from_png("GUI/red.png")
            self.apple = cairo.ImageSurface.create_from_png("GUI/blue_indirect.png")
        except Exception, e:
            print e.message
            sys.exit(1)

        self.locate_apple()
        glib.timeout_add(100, self.on_timer)

        
        

    def expose(self, widget, event):
        pixbuf = gtk.gdk.pixbuf_new_from_file('temp.png')
        widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], pixbuf, 0, 0, 0,0)

        cr = widget.window.cairo_create()

        if self.inGame:
            cr.set_source_rgb(0, 0, 0)
            cr.paint()

            cr.set_source_surface(self.apple, self.apple_x, self.apple_y)
            cr.paint()

            for z in range(self.dots):
                if (z == 0): 
                    cr.set_source_surface(self.head, x[z], y[z])
                    cr.paint()
                else:
                    cr.set_source_surface(self.dot, x[z], y[z])                 
                    cr.paint()
        else:
            self.game_over(cr)
             
    

    def game_over(self, cr):

        w = self.allocation.width / 2
        h = self.allocation.height / 2

        (x, y, width, height, dx, dy) = cr.text_extents("Game Over")

        cr.set_source_rgb(65535, 65535, 65535)
        cr.move_to(w - width/2, h)
        cr.show_text("Game Over")
        self.inGame = False
    


    def check_apple(self):

        if x[0] == self.apple_x and y[0] == self.apple_y: 
            self.dots = self.dots + 1
            self.locate_apple()
        
    
    def move(self):

        z = self.dots

        while z > 0:
            x[z] = x[(z - 1)]
            y[z] = y[(z - 1)]
            z = z - 1

        if self.left:
            x[0] -= DOT_SIZE

        if self.right: 
            x[0] += DOT_SIZE

        if self.up:
            y[0] -= DOT_SIZE

        if self.down:
            y[0] += DOT_SIZE
        
    

    def check_collision(self):

        z = self.dots
       
        while z > 0:
            if z > 4 and x[0] == x[z] and y[0] == y[z]:
                self.inGame = False
            z = z - 1

        if y[0] > HEIGHT - DOT_SIZE: 
            self.inGame = False
        
        if y[0] < 0:
            self.inGame = False
        
        if x[0] > WIDTH - DOT_SIZE:
            self.inGame = False

        if x[0] < 0:
            self.inGame = False
        

    def locate_apple(self):
    
        r = random.randint(0, RAND_POS)
        self.apple_x = r * DOT_SIZE
        r = random.randint(0, RAND_POS)
        self.apple_y = r * DOT_SIZE
   

    def on_key_down(self, event): 
    
        key = event.keyval

        if key == gtk.keysyms.Left and not self.right: 
            self.left = True
            self.up = False
            self.down = False
        

        if key == gtk.keysyms.Right and not self.left:
            self.right = True
            self.up = False
            self.down = False
        

        if key == gtk.keysyms.Up and not self.down:
            self.up = True
            self.right = False
            self.left = False
        

        if key == gtk.keysyms.Down and not self.up: 
            self.down = True
            self.right = False
            self.left = False


class Simulation(gtk.Window):

    def __init__(self):
        super(Simulation, self).__init__()
        
        self.set_title('Simulation')
        self.set_size_request(WIDTH, HEIGHT)
        self.set_resizable(False)
        self.set_position(gtk.WIN_POS_CENTER)

        self.sim_area = SimArea()
        self.connect("key-press-event", self.on_key_down)
        self.add(self.sim_area)
        
        self.connect("destroy", gtk.main_quit)
        self.show_all()


    def on_key_down(self, widget, event): 
     
        key = event.keyval
        self.sim_area.on_key_down(event)


Simulation()
gtk.main()
