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
  // if there is cereal, eat it
  while (Serial.available() > 2 ) {
        colorRGB[0] = Serial.read();
        colorRGB[1] = Serial.read();
        colorRGB[2] = Serial.read();

    }

    
    
    // fade the red, green, and blue legs of the LED:
    analogWrite(redPin, colorRGB[0]);
    analogWrite(greenPin, colorRGB[1]);
    analogWrite(bluePin, colorRGB[2]);
    
  }

