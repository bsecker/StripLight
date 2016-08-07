// pins for the LEDs:
const int redPin = 10;      //Arduino driving pin for Red
const int greenPin = 11;    //Arduino driving pin for Green
const int bluePin = 9;      //Arduino driving pin for Blue
int colorRGB[3];

unsigned long previous_time = 0;
const long timeout_interval = 10; //Timeout to automatically turn off lights 
bool enable_pins = 1;

void setColor(int red, int green, int blue)
{
  // fade the red, green, and blue legs of the LED:
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);  
 
}

void setOff(){
  // turn all pins off
  analogWrite(redPin, 0);
  analogWrite(greenPin, 0);
  analogWrite(bluePin, 0);  
}

void setup() {
  // initialize serial:
  Serial.begin(9600);
  // make the pins outputs:
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

}

void loop() {

  unsigned long current_time = millis();

  // Read Serial Messages 
  while (Serial.available() > 2 ) {
        colorRGB[0] = Serial.read();
        colorRGB[1] = Serial.read();
        colorRGB[2] = Serial.read();
    }

  if (current_time - previous_time >= timeout_interval){
    enable_pins = 0; //turn off
  }
  else {
    enable_pins = 1;
  }
  
  setColor(colorRGB[0], colorRGB[1], colorRGB[2]);

  /*

  BIG ASS COMMENT FOR NEXT TIME:
  completely redo timeouts
  


  */
  previous_time = current_time;


}
