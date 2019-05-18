#define sensor A0
int light = 13;
bool lightStatus = false;
float distance;
float threshold = 30.0;

void setup() {
  Serial.begin(9600);
  pinMode(light, OUTPUT);
  
}

void loop() {

    float volts = analogRead(sensor) * 0.0048828125; // value from sensor * (5 / 1024)
    distance = 13 * pow(volts, -1); 
  

    String msg = "distance:" + String(distance) + ", lightStatus:" + String(lightStatus) + ", threshold:" + String(threshold);
    

    if (Serial.available() > 0)
    {
      String data = Serial.readString();
      distance = data.toFloat();
    }

    delay(1000);
    
    if (distance <= 30)
    {
      //Serial.println(distance);
      digitalWrite(light, HIGH);
      lightStatus = true;
      
    }
    else
    {
      digitalWrite(light, LOW);
    }

    Serial.println(msg);

}
