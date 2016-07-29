"""Python program for interfacing with the RGB strip lights"""

try:
	import sys
	import serial
except ImportError, _err:
	print("couldn't load module. {0}".format(_err))
	sys.exit()

class ArduinoSerial:
	def __init__(self):
		"""main serial communication module that handles writing to serial"""

		self.ser = serial.Serial('COM8')

	def set_color(self, color):
		"""convert to serial message and send"""
		for _i in color:
			
