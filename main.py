"""Python program for interfacing with the RGB strip lights"""

try:
    import sys
    import serial
    import time
    import math

except ImportError, _err:
    print("couldn't load module. {0}".format(_err))
    sys.exit()

class ArduinoSerial:
    """main  module that handles writing to serial and API"""
    def __init__(self):
        self.ser = serial.Serial('COM4', 9600)
        self.color_temp = 4000
        self.lights_on = True #override lights

    def set_color(self, color):
        """convert to serial message and send
        takes [rrr,ggg,bbb] as list input"""
        self.ser.write(chr(int(color[0])))
        self.ser.write(chr(int(color[1])))
        self.ser.write(chr(int(color[2])))

    def terminate(self):
        self.ser.close()

    def main_loop(self):
        """main loop. check for pings, update colour."""
        while True:
            self.set_night_temperature()
            time.sleep(5)


            # enable lights or not
            if self.lights_on:
                self.set_color(convert_K_to_RGB(self.color_temp))
            else:
                self.set_color([0,0,0])

            print "temp: ", self.color_temp

    def set_night_temperature(self):
        """at specific times fade to certain temperature points"""
        _fade = 0
        if int(time.strftime("%H")) >= 0: #morning
            _fade = 4000

        if int(time.strftime("%H")) >= 19: #
            _fade = 3500

        if int(time.strftime("%H")) >= 20:
            _fade = 3000

        if int(time.strftime("%H")) >= 21:
            _fade = 2500

        if int(time.strftime("%H")) >= 22:
            _fade = 2000

        if int(time.strftime("%H%M")) >= 2230:
            _fade = 1000

        print _fade
        self.fade_to_color(_fade)


    def fade_to_color(self, color):
        """fade current colour temperature to given color"""
        if self.color_temp < color:
            self.color_temp += 10
        elif self.color_temp > color:
            self.color_temp +=- 10


def convert_K_to_RGB(colour_temperature):
    """
    Converts from K to RGB, algorithm courtesy of 
    http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
    """
    #range check
    if colour_temperature < 1000: 
        colour_temperature = 1000
    elif colour_temperature > 40000:
        colour_temperature = 40000
    
    tmp_internal = colour_temperature / 100.0
    
    # red 
    if tmp_internal <= 66:
        red = 255
    else:
        tmp_red = 329.698727446 * math.pow(tmp_internal - 60, -0.1332047592)
        if tmp_red < 0:
            red = 0
        elif tmp_red > 255:
            red = 255
        else:
            red = tmp_red
    
    # green
    if tmp_internal <=66:
        tmp_green = 99.4708025861 * math.log(tmp_internal) - 161.1195681661
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green
    else:
        tmp_green = 288.1221695283 * math.pow(tmp_internal - 60, -0.0755148492)
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green
    
    # blue
    if tmp_internal >=66:
        blue = 255
    elif tmp_internal <= 19:
        blue = 0
    else:
        tmp_blue = 138.5177312231 * math.log(tmp_internal - 10) - 305.0447927307
        if tmp_blue < 0:
            blue = 0
        elif tmp_blue > 255:
            blue = 255
        else:
            blue = tmp_blue
    
    return [int(red), int(green), int(blue)]

def main():
    arduino_serial = ArduinoSerial()
    time.sleep(2)
    print("initialised")
    arduino_serial.main_loop()
    arduino_serial.terminate()



if __name__ == '__main__':
    main()
