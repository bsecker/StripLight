"""Python program for interfacing with the RGB strip lights
Timer currently uses threading
"""

try:
    import sys
    import serial
    import time
    import math
    from flask import Flask, render_template, request
    from threading import Timer, Thread

except ImportError, _err:
    print("couldn't load module. {0}".format(_err))
    sys.exit()

# notification color constants
RED = (255, 0, 0)

# Flask webserver
app = Flask(__name__)

class ArduinoSerial:
    """main class that handles writing to serial and API"""
    def __init__(self):
        self.ser = serial.Serial('COM4', 9600)
        self.color_temp = 4000
        self.light_status = "on" #override lights

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
        time.sleep(1)
        self.set_lights("on")
        time.sleep(1)
        self.set_lights("notify", color = RED, blink_speed = 0.3, repeats = 2)
        time.sleep(1)
        self.set_lights("off")

    def set_lights(self, status = "on", **args):
        """
        Set lights to a color, or blink.
        status = [on, off, notify]
        color = RGB color to blink 
        blink_speed = speed to blink at
        repeats = number of times to blink

        """
        # enable lights or not
        if status == "on":
            self.color_temp = self.set_night_temperature()
            self.set_color(convert_K_to_RGB(self.color_temp))
        elif status == "off":
            self.set_color([0,0,0])
        elif status == "notify":
            self.blink(args)

        print "temp: ", self.color_temp

    def blink(self, args):
        """blink lights on and off"""
        for _i in range(args["repeats"]):
            self.set_color(args["color"])
            time.sleep(args["blink_speed"])
            self.set_color([0, 0, 0])
            time.sleep(args["blink_speed"])

    def set_night_temperature(self):
        """at specific times fade to certain temperature points. replace with curve"""
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

        print "fading to: ", _fade
        return self.fade_to_color(_fade, self.color_temp)

    def fade_to_color(self, color, color_temp):
        """fade current colour temperature to given color"""
        if color_temp < color:
            color_temp += 10
        elif color_temp > color:
            color_temp +=- 10

        return color_temp


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

class Scheduler(object):
    """https://gist.github.com/chadselph/4ff85c8c4f68aa105f4b
    Use multiple threads to make a timer for writing to serial every 5 seconds
    """

    def __init__(self, sleep_time, function):
        self.sleep_time = sleep_time
        self.function = function
        self._t = None

    def start(self):
        if self._t is None:
            self._t = Timer(self.sleep_time, self._run)
            self._t.start()
        else:
            raise Exception("this timer is already running")

    def _run(self):
        self.function(arduino_serial.light_status)
        self._t = Timer(self.sleep_time, self._run)
        self._t.start()

    def stop(self):
        if self._t is not None:
            self._t.cancel()
            self._t = None


@app.route("/")
def main():
    try: 
        # setup unless already done that - TO DO: FIX THIS BIT UP. CURRENTLY {VERY} BAD
        global arduino_serial, scheduler
        arduino_serial = ArduinoSerial()
        time.sleep(2)
        print("Initialised Serial")
        arduino_serial.set_lights("on")

        # set lights every 5 seconds
        scheduler = Scheduler(5, arduino_serial.set_lights)
        scheduler.start()
    except: # FIX THIS BIT TO PROPERLY HANDLE ERRORS.
        pass

    templateData = {
      'title' : 'HELLO!',
      'name' : 'Benjamin',
      'light_status' : arduino_serial.light_status,
      'fade_to' : arduino_serial.color_temp,
      }
    return render_template('index.html', **templateData)

@app.route("/toggle")
def toggle_leds():
    if arduino_serial.light_status == "off":
        arduino_serial.light_status = "on"
    else:
        arduino_serial.light_status = "off"
    
    templateData = {
      'title' : 'HELLO!',
      'name' : 'Benjamin',
      'light_status' : arduino_serial.light_status,
      'fade_to' : arduino_serial.color_temp,
      }

    return render_template('index.html', **templateData)

@app.route("/notify")
def notify_leds():
    arduino_serial.set_lights("notify", color = RED, blink_speed = 0.3, repeats = 2)

    templateData = {
      'title' : 'HELLO!',
      'name' : 'Benjamin',
      'light_status' : arduino_serial.light_status,
      'fade_to' : arduino_serial.color_temp,
      }

    return render_template('index.html', **templateData)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=85, debug=True)
    scheduler.stop()
    arduino_serial.terminate()
    