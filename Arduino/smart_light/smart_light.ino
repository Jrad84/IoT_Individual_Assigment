#define sensor A0
int light = 13;

void setup() {
  Serial.begin(9600);
  pinMode(light, OUTPUT);
  
}

void loop() {

    float volts = analogRead(sensor) * 0.0048828125; // value from sensor * (5 / 1024)
    int distance = 13 * pow(volts, -1); 
    delay(1000);

    if (distance <= 30)
    {
      Serial.println(distance);
      digitalWrite(light, HIGH);
    }
    else
    {
      Serial.println("Power saving mode on.");
      digitalWrite(light, LOW);
    }

}
