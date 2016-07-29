int RedPin = 10;      //Arduino driving pin for Red
int GreenPin = 11;    //Arduino driving pin for Green
int BluePin = 9;      //Arduino driving pin for Blue


#include <IRremote.h>
 
int RECV_PIN = 4; //IR Receiving pin on the driver shield
 
IRrecv irrecv(RECV_PIN);
 
decode_results results;

void setColor(int red, int green, int blue)
{
  analogWrite(RedPin, red);
  analogWrite(GreenPin, green);
  analogWrite(BluePin, blue);  
 
}
 
void setup()
{
  Serial.begin(9600);
  irrecv.enableIRIn(); // Start the receiver
}
 
void loop() {
  if (irrecv.decode(&results)) {
    Serial.println(results.value);
    irrecv.resume(); // Receive the next value

    switch (results.value) {
    	case 16769055: //on\
    	setColor(255,255,255);
    	break;

    	case 16736415: //off
    	setColor(0,0,0);
    	break;

    	case 16748655: //r
    	setColor(255,0,0);
    	break;

    	case 16716015: //g
    	setColor(0,255,0);
    	break;

    	case 16732335: //b
    	setColor(0,0,255);
    	break;

    	case 16764975: //w
    	setColor(255,255,255);
    	break;

    }
   
  }
}
