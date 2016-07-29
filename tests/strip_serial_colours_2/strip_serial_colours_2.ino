/*
  Reading a serial ASCII-encoded string.

 This sketch demonstrates the Serial parseInt() function.
 It looks for an ASCII string of comma-separated values.
 It parses them into ints, and uses those to fade an RGB LED.

 Circuit: Common-anode RGB LED wired like so:
 * Red cathode: digital pin 3
 * Green cathode: digital pin 5
 * blue cathode: digital pin 6
 * anode: +5V

 created 13 Apr 2012
 by Tom Igoe

 This example code is in the public domain.
 */

// pins for the LEDs:
const int redPin = 10;      //Arduino driving pin for Red
const int greenPin = 11;    //Arduino driving pin for Green
const int bluePin = 9;      //Arduino driving pin for Blue
int colorRGB[3];

void setup() {
  // initialize serial:
  Serial.begin(9600);
  // make the pins outputs:
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void loop() {
  // if there's any serial available, read it:
  while (Serial.available() >=2 ) {
    colorRGB[0] = Serial.read();
    colorRGB[1] = Serial.read();
    colorRGB[2] = Serial.read();

      // fade the red, green, and blue legs of the LED:
      analogWrite(redPin, colorRGB[0]);
      analogWrite(greenPin, colorRGB[1]);
      analogWrite(bluePin, colorRGB[2]);
    }
  }








