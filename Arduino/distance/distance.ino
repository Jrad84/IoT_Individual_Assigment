int trigger = 8;
int echo = 9;
int led = 13;
long duration, distance, cm, threshold;
bool lightStatus = 0;

void setup() 
{
    pinMode(trigger, OUTPUT);
    pinMode(echo, INPUT);
    pinMode(led, OUTPUT);
    Serial.begin(9600);
    threshold = 60.0;

}

void loop() 
{
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
  distance= duration*0.034/2;
  
  
  if (distance <= threshold)
  {
    digitalWrite(led, HIGH);
    lightStatus = 1;
    Serial.println(distance);
    Serial.println(lightStatus);
    Serial.println(threshold);
  }
  delay(200);

}
