#include <Servo.h>

// This is using an arduino Nano
#define triggerPin 3
#define echoPin 4

//Servo needs to be on PWM pins:
#define horizontalServo 6
#define verticalServo 5

//Global variables for servos
Servo vServo, hServo;

void setup() {
  // Starting serial
  Serial.begin(115200);
  Serial.println("*** STARTING ***");

  //Setting up pins
  pinMode(triggerPin, OUTPUT);
  pinMode(echoPin, INPUT);

  //Setting up servos
  vServo.attach(verticalServo);
  hServo.attach(horizontalServo);
  vServo.write(90);
  hServo.write(90);
}


//This function is borrowed from internet:
//A timiout has been added at the pulseIn function
int compute_distance()
{
  // establish variables for duration of the ping,
  // and the distance result in centimeters
  long duration, mm;

  // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);

  // Read the signal from the sensor: a HIGH pulse whose
  // duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.

  duration = pulseIn(echoPin, HIGH, 40000);


  //Converting and returning milimeters
  mm = duration * 10 / 29 /2;
  return mm ;
}

void complete_scan()
{
  //Starting zone
  int hmin = 60;
  int vmin = 60;

  // Steps setup:
  int hstep = 2;
  int vstep = 2;


  for (int v = 0; v < 30; v++)
  {
    vServo.write(vmin + v * vstep);
    bool newline = true;
    for (int x = 0; x <  30; x++)
    {
      hServo.write(hmin + x * hstep);
      if (newline)
        delay(350);
      delay(50);
      newline = false;
      int result  = compute_distance();
      int tries = 0;

      //This catch sensors's errors and retry:
      while ((result >= 4000 || result == 0) && tries < 5)
      {
        delay(100);
        result = compute_distance();
        tries++;
      }
      if (result > 4000)
        result = 4000;
      Serial.println(result);
    }
  }
}


//Main loop
void loop() {
  //This will start to sync with the arduino
  Serial.print("Parsing:\n");

  //Wait for serial:
  while (!Serial.available()) {}

  //Read serial command:
  String command = Serial.readString();

  //This is for manual testing
  if (command == "MOVE")
  {
    Serial.println("M");

    while (!Serial.available()) {}
    String hmovestring = Serial.readString();
    int hmove = hmovestring.toInt();
    Serial.println(hmovestring);
    hServo.write(hmove);

    while (!Serial.available()) {}
    int vmove = Serial.parseInt();
    Serial.println(vmove);
    vServo.write(vmove);
  }

  //Return the distance at the current position
  if (command == "SCAN")
  {
    //Serial.println("S");
    Serial.println(compute_distance());
  }

  //Launch the all 30*30 scan
  if (command == "IMG")
    complete_scan();
}
