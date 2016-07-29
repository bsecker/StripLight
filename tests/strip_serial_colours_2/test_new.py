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
    loop = True
    if (arduino_serial.ser.isOpen()):
    # Start a main loop
        while loop:
            redVal = input('Red value:')
            greenVal = input('Green value:')
            blueVal = input('Blue value:')

            arduino_serial.ser.write(chr(int(redVal))+chr(int(greenVal))+chr(int(blueVal)))

            # Check if user wants to end
            loopCheck = raw_input('Loop (y/N):')
            if (loopCheck == 'N'):
             loop = False
        # After loop exits, close serial connection
        arduino_serial.ser.close()


    arduino_serial.ser.close()
if __name__ == '__main__':
    main()