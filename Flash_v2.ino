// 30 min light exposure contin

String command;

void setup()
{
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Input 1 to Turn LED on and 2 to off");
}

// Cycle Duration

int seconds  = 60; // 5 min continuous extatitation  
int Time_ON  = seconds * 1000 ;
int Time_OFF = seconds * 1000 ;
int sk = 1;

// Subroutines
void photodamage_cycle()
{
    digitalWrite(13, HIGH);
    Serial.println("Light is on");
    delay (Time_ON);
    digitalWrite(13, LOW);
    delay(Time_OFF);
}

void loop() 
{
if(Serial.available())
  {   
    command = Serial.readStringUntil('\n');
    if(command.equals("photodamage_cycle") || command.equals("PDC"))
    {
      photodamage_cycle();
      Serial.println("Done");
    }
  }    
 else 
 {
  Serial.println("Waiting"); // Tells Python is ready;
  delay (2000);
 }
}
