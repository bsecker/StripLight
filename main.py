"""Python program for interfacing with the RGB strip lights"""

try:
    import sys
    import serial
    import time
except ImportError, _err:
    print("couldn't load module. {0}".format(_err))
    sys.exit()

class ArduinoSerial:
    """main serial communication module that handles writing to serial"""
    def __init__(self):
        self.ser = serial.Serial('COM4', 9600)

    def set_color(self, color):
        """convert to serial message and send
        takes [rrr,ggg,bbb] as list input"""
        self.ser.write(chr(int(color[0]))+chr(int(color[1]))+chr(int(color[2])))

    def terminate(self):
        self.ser.close()

def main():
    arduino_serial = ArduinoSerial()
    time.sleep(2)
    arduino_serial.set_color([255,255,255])

    
if __name__ == '__main__':
    main()