void setup() 
{
  Serial.begin(9600);
  pinMode(A0,INPUT);
}

void loop() 
{
  if(Serial.available() > 0)
  {
    if(((char) Serial.read()) == 'a')
    {
      Serial.println(analogRead(A0));
      Serial.println(micros());
    }
  }

  //delay(100);
}
