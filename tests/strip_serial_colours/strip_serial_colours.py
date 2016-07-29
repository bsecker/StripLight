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
        """convert to serial message and send"""
        _message = ','.join([str(i) for i in color])
        self.ser.write(_message)

def main():
    arduino_serial = ArduinoSerial()
    #arduino_serial.set_color([255,255,255])
    time.sleep(2)
    while True:
        print arduino_serial.ser.write('156,123,231\r\n')
        time.sleep(1)
        print arduino_serial.ser.write('0,0,0\r\n')
        time.sleep(1)
if __name__ == '__main__':
    main()