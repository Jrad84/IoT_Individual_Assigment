
#define trigger 8
#define echo 9

int led = 13;
float duration;
float distance;
float threshold;
bool lightStatus;

void setup() 
{
    Serial.begin(9600);
    pinMode(trigger, OUTPUT);
    pinMode(echo, INPUT);
    pinMode(led, OUTPUT);
    lightStatus = false;
}

void loop() 
{
  if (Serial.available() > 0)
  {
    String data = Serial.readString();
    threshold = data.toFloat();
  }
  
    // Clears the trigPin
  digitalWrite(trigger, LOW);
  delayMicroseconds(2);
  
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigger, LOW);

  digitalWrite(led, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echo, HIGH);
  
  // Calculating the distance
  distance = (duration / 2) * 0.0343;
 
  if (threshold < distance)
  {
    digitalWrite(led, HIGH);
    lightStatus = true;
  }
  else
  {
    digitalWrite(led, LOW);
    lightStatus = false;
  }
   
   String msg = "distance:" + String(distance) + ", lightStatus:" + String(lightStatus) + ", threshold:" + String(threshold);
   Serial.println(msg);
   
   delay(500);

}
