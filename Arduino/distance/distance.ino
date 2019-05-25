
#define trigger 8
#define echo 9

int led = 13;
float duration, distance, threshold;
bool lightStatus = 0;

void setup() 
{
    Serial.begin(9600);
    pinMode(trigger, OUTPUT);
    pinMode(echo, INPUT);
    pinMode(led, OUTPUT);
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

  distance = (duration / 2) * 0.0343;
 
  if (distance <= threshold)
  {
    digitalWrite(led, HIGH);
    lightStatus = 1;
  }
   
   Serial.println(distance);
   Serial.println(lightStatus);
   Serial.println(threshold);
   
   delay(500);

}
