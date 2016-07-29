int RedPin = 10;      //Arduino driving pin for Red
int GreenPin = 11;    //Arduino driving pin for Green
int BluePin = 9;      //Arduino driving pin for Blue
 
void setColor(int red, int green, int blue)
{
  analogWrite(RedPin, red);
  analogWrite(GreenPin, green);
  analogWrite(BluePin, blue);  
 
}
 
void setup() 
{  
  pinMode(RedPin, OUTPUT);    //Init Arduino driving pins
  pinMode(GreenPin, OUTPUT);
  pinMode(BluePin, OUTPUT);  
  Serial.begin(9600);
}
 
void loop() 
{
  for (int i=0;i<255;i++)  //Changing Red brightness
  {
    setColor(i, 0, 0);
    delay (10);
  }
  delay(2000);
  for (int i=0;i<255;i++)  //Changing Green brightness
  {
    setColor(0, i, 0);
    delay (10);
  }
  delay(2000);
  for (int i=0;i<255;i++)  //Changing Blue brightness
  {
    setColor(0, 0, i);
    delay (10);
  }
  delay(2000);
  for (int i=0;i<255;i++)
  {
    setColor(i, 0, 255-i);
    delay (10);
  }
  for (int i=0;i<255;i++)
  {
    setColor(255-i, i, 0);
    delay (10);
  }
  for (int i=0;i<255;i++)
  {
    setColor(0, 255-i, i);
    delay (10);
  }
}
