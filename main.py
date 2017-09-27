#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys, os
import gi
import hashlib
import time

gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gst, GObject, Gtk, Gio, GdkPixbuf
# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GdkX11, GstVideo



pin=''
pin_hash='ab890a8cc28ba9ac9b89c988d0783f1d7b20711bc967e92dd9584af9930adfa25eb728cf703d7d13d4bf79799f18d1966f2c503de13c45114ebaab017c022f84'

class MyWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, title="TV", application=app)
        self.args = app.args
        self.set_title("Video-Player")
        self.set_default_size(600, 300)
        #self.connect("destroy", Gtk.main_quit)
        self.set_keep_above(True)
        self.nit_rotator=GObject.timeout_add(1000, self.ura)
        #osnovni mbox
        self.mbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.mbox)
        
        ##overlay
        self.plasti = Gtk.Overlay()
        #button = Gtk.Button(label="Overlayed Button")
        #button.set_valign(Gtk.Align.CENTER)
        #button.set_halign(Gtk.Align.CENTER)
        
        
        #moj stack
        
        
        #eventBox z glavnim predvajalnikom
    
        self.okvir=Gtk.EventBox()
        self.okvir.connect ('button-press-event', self.na_klik)
        self.movie_window = Gtk.DrawingArea()
        self.okvir.add(self.movie_window)
        
        self.plasti.add(self.okvir)
        #self.plasti.add_overlay(button)
        self.plasti.show()
        
        
        
        self.player = Gst.ElementFactory.make("playbin", "player")
        self.player.set_property("buffer-size",250)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)        
        
        self.mbox.pack_start(self.plasti, True, True, 0)
        self.show_all()
        ###izberi program
        self.program()
        
    def on_message(self, bus, message):
        #print message.get_structure().to_string()
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
            
        elif t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            
        elif t == Gst.MessageType.WARNING:
            print message.get_structure().to_string()
        elif t == Gst.MessageType.INFO:
            print message.get_structure().to_string()
            
    def on_sync_message(self, bus, message):
        
        if message.get_structure().get_name() == 'prepare-window-handle':
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_window_handle(self.movie_window.get_property('window').get_xid())        
        
        
        
    def program(self):
        global pin
        print niz[cc][1]
        if "odrasle" in niz[cc][1] and pin != pin_hash:
            print 'xxxxxx'
            self.get_pin()
        else:
            self.play()
        
    
    def play(self):
        self.player.set_state(Gst.State.READY)
        self.player.set_property("uri", niz[cc][2])
        self.player.set_state(Gst.State.PLAYING)
        self.set_title(niz[cc][0])
        
    def pplus(self):
        global cc
        cc=cc+1
        if cc+1 > len(niz):
            cc = 0
        print 'P+: '+str(cc)
        self.program()
    def pminus(self):
        global cc
        cc=cc-1
        if cc < 0:
            cc = cc + len(niz)
        print 'P-: '+str(cc)
        self.program()
    
    def na_klik(self,okvir,event):
        
        x = event.x/okvir.get_allocated_width()
        y = event.y/okvir.get_allocated_height()
        #spodaj desno program naprej
        if x > 0.67 and y > 0.50:
            self.pplus()
        #spodaj levo program nazaj
        if x < 0.33 and y > 0.50:
            self.pminus()
        #spodajcenter p_selektor
        if x > 0.33 and x < 0.67 and y > 0.50:
            #self.p_selektor(self,'Izberi program!', 'Program!')
            self.p_list()
            print 'center spodaj'
        if x > 0.33 and x < 0.67 and y < 0.50:
            global roto, rura
            if roto==0:
                roto=1
                self.roto_indic(True)
                self.player.set_property("mute", True)
            else:
                roto=0
                rura=0
                self.roto_indic(False)
                self.player.set_property("mute", False)
            print 'center zgoraj - toggle roto'
            
    def p_list(self):
        # Returns user input as a string or None
        # If user does not input text it returns None, NOT AN EMPTY STRING.
        def oddaj(box, row):
            global cc
            lb.select_row(row)    
            print ' pressed'
            
            cc=row.get_index()
            pocisti()
            self.program()
            
        def pocisti():
            self.naplast.destroy()
            
        
        
        
        lb=Gtk.ListBox()
        self.naplast=Gtk.ScrolledWindow()
        self.naplast.set_border_width(25)
    
           
        lb.set_selection_mode(1)
        for i, p in enumerate(niz):
            lb.insert(Gtk.Label(p[0]), i)
            
        self.naplast.add_with_viewport(lb)
        lb.select_row(lb.get_row_at_index(cc))

        lb.connect("row_selected", oddaj)

        self.plasti.add_overlay(self.naplast)
        self.naplast.set_valign(Gtk.Align.BASELINE)
        self.naplast.set_halign(Gtk.Align.BASELINE)
        self.show_all()
        
    def roto_indic(self,on_of):
        if on_of == True:
            self.lbl = Gtk.Label()
            self.lbl.set_markup('<span bgcolor="red" background_alpha=\"20%\" style=\"oblique\"> Rotating ! </span>')
            
            self.lbl.set_valign(Gtk.Align.START)
            self.lbl.set_halign(Gtk.Align.CENTER)
            
            self.plasti.add_overlay(self.lbl)
            self.show_all()
            self.okvir.grab_focus()
        else: 
            self.lbl.destroy()
        
    
    
    def get_pin(self):
        # Returns user input as a string or None
        # If user does not input text it returns None, NOT AN EMPTY STRING.
        def oddaj(ent):
            print 'enter pressed'
            obdelaj(ent)
        def ok_clicked(gumb):
            print 'ok clicked'
            obdelaj(self.vnos)
        def cancel_clicked(gumb):
            print 'cancel_clicked'
            pocisti()
        def obdelaj(ent):
            global pin
            hash_object = hashlib.sha512(ent.get_text())
            pin = hash_object.hexdigest()
            print pin
            print pin_hash
            if pin==pin_hash:
                pocisti()
                self.play()
        def pocisti():
            self.naplast.destroy()
            
        
        
        self.vnos = Gtk.Entry()
        button_ok = Gtk.Button("OK")
        
        button_cancel = Gtk.Button("Cancel")
        
        label=Gtk.Label("Zaščitena vsebina! Vnesi PIN!")
        self.naplast = Gtk.VBox()
        self.naplast.set_border_width(6)
        self.naplast.set_valign(Gtk.Align.CENTER)
        self.naplast.set_halign(Gtk.Align.CENTER)
        
        self.naplast.set_spacing(10)
        self.naplast.pack_start(label, False, False, 0)
        self.naplast.pack_start(self.vnos, False, False, 0)
        hbox = Gtk.HBox()
        
        hbox.pack_start(button_cancel, False, False, 8)
        hbox.pack_start(button_ok,False, False, 8)
        hbox.set_halign(Gtk.Align.CENTER)
        self.naplast.pack_start(hbox, False, True, 0)
        ##pwd staff
        self.vnos.set_visibility(False)
        self.vnos.set_invisible_char("*")
        self.vnos.set_alignment(0.5)
        ###funkcije
        button_ok.connect("clicked", ok_clicked)
        button_cancel.connect("clicked", cancel_clicked)
        self.vnos.connect("activate", oddaj)
        ##
        self.plasti.add_overlay(self.naplast)
        self.vnos.grab_focus()
        self.show_all()
        ##

            
    def ura(self):
        global rura
        zamik = 15 #sekundni zamik rotatorja
        #nit se izvaja vsako sekundo, prevri rotator in uro rotatorja 
        if roto == 1: #ce je rotator prizgan
            #preverimo uro
            rura = rura + 1
            self.lbl.set_markup('<span bgcolor="red" background_alpha=\"20%\" style=\"oblique\"> Rotating ! '+str(zamik-rura)+' </span>')
            if rura >= zamik:
                self.pplus()
                rura = 0
        return True
        


class MyApplication(Gtk.Application):

    def __init__(self):
        # init the parent class
        # the Gio.ApplicationFlags.HANDLES_COMMAND_LINE flags tells that
        # we want to handle the command line and do_command_line will be called
        Gtk.Application.__init__(self,flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE)
        self.args = None # store for parsed command line options
        
        Gst.init(None)
        
    def do_activate(self):
        win = MyWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)
        
    def on_quit(self, action, param):
        self.quit()
        
    def do_command_line(self, args):
        '''
        Gtk.Application command line handler
        called if Gio.ApplicationFlags.HANDLES_COMMAND_LINE is set.
        must call the self.do_activate() to get the application up and running.
        '''
        print 'Raba: ukaz.py fullm3ufilepath ch=? udpyx=http... purge=words_separatedby_comma'
        global cc, niz, roto, rura
        roto = 0
        rura = 0
        cc=0
        udpxy=''
        purge=[] #niz prepovedanih kjucev
        for ar in args.get_arguments():
            print ar
            if 'ch=' in ar:
                cc=int(ar.split('=')[1])
            if 'udpxy=' in ar:
                udpxy=ar.split('=')[1]
            if 'purge=' in ar:
                kw=ar.split('=')[1]
                purge=kw.split(',')
        if len(args.get_arguments()) >= 2:
            niz = self.seznam(args.get_arguments()[1], udpxy, purge) #prvi argument je seznam v m3u fullpath
        else:
            print 'Zahteva m3u falj kot prvi argument!'
            self.quit()

        self.activate()
        return 0
        
    def seznam(self,path,udpxy,purge):
                global niz
                print purge
                n = []
                f = open(path, 'r')
                lines = f.readlines()
                f.close()
                for c, val in enumerate(lines):
                    #if info is in this line, udp is in next
                    if '#EXTINF:' in val:
                        if any(word in val for word in purge):
                            print val
                            print 'Pogoj purge izpolnjen'
                        else:
                            ime=val.split(',')[1].rstrip()
                            data=val.split(',')[0]
                            naslov=lines[c+1].rstrip()
                            if udpxy != '':
                                naslov=naslov.replace('udp://@',udpxy)
                            print ime+': '+naslov
                            n.append([ime, data, naslov])
                #print n
                return n
    


if __name__ == "__main__":
    app = MyApplication()
    app.run(sys.argv)
