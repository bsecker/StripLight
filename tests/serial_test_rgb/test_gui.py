import gtk
import sys
import serial
import time

class PyApp(gtk.Window):

   def __init__(self):
       super(PyApp, self).__init__()

       self.serialPort = "COM4"

       self.set_title("RGB Test")
       self.set_size_request(260, 150)
       self.set_position(gtk.WIN_POS_CENTER)
       self.setup_serial()

       headerVbox = gtk.VBox(True,0)
       headerLabel1 = gtk.Label("RGB Control App for Arduino")
       headerLabel2 = gtk.Label("Written by John Meichle")
       headerVbox.pack_start(headerLabel1)
       headerVbox.pack_end(headerLabel2)


       rHbox = gtk.HBox(True,0)
       rLabel = gtk.Label("Red: ")
       rHbox.pack_start(rLabel)   
            
       rScale = gtk.HScale()
       rScale.set_name("red")
       rScale.set_range(0, 255)
       rScale.set_increments(1, 10)
       rScale.set_digits(0)
       rScale.set_size_request(160, 35)
       rScale.connect("value-changed", self.on_changed)
       rHbox.pack_end(rScale)
       
       gHbox = gtk.HBox(True,0)
       gLabel = gtk.Label("Green: ")
       gHbox.pack_start(gLabel)   
       
       gScale = gtk.HScale()
       gScale.set_name("green")
       gScale.set_range(0, 255)
       gScale.set_increments(1, 10)
       gScale.set_digits(0)
       gScale.set_size_request(160, 35)
       gScale.connect("value-changed", self.on_changed)
       gHbox.pack_end(gScale)
       
       bHbox = gtk.HBox(True,0)       
       bLabel = gtk.Label("Blue: ")
       bHbox.pack_start(bLabel)   
       
       bScale = gtk.HScale()
       bScale.set_name("blue")
       bScale.set_range(0, 255)
       bScale.set_increments(1, 10)
       bScale.set_digits(0)
       bScale.set_size_request(160, 35)
       bScale.connect("value-changed", self.on_changed)
       bHbox.pack_end(bScale)
       
       
       vbox = gtk.VBox(True,0)

       vbox.pack_start(headerVbox)
       vbox.pack_start(rHbox)
       vbox.pack_end(gHbox)
       vbox.pack_end(bHbox)
       
       

       self.add(vbox)

       self.connect("destroy", lambda w: gtk.main_quit())
       self.show_all()
       


   def on_changed(self, widget):
       
       val = widget.get_value()
       name = widget.get_name()
      
       if name == "red":
           self.ser.write("r" + chr(int(val)))
       elif name == "green":
           self.ser.write("g" + chr(int(val)))
       elif name == "blue":
           self.ser.write("b" + chr(int(val)))
       else: 
           print "ERROR: Invalid widget name, in on_changed function"
   
                
                
   def setup_serial(self):
     self.ser = serial.Serial()
     self.ser.setPort(self.serialPort)
     self.ser.baudrate = 57600
     self.ser.open()
     if (self.ser.isOpen()):
       print "Serial Open"
     else:
       print "Serial Closed"

PyApp()
gtk.main()