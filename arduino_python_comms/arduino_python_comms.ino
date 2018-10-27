/*
Shiva Nathan (15-112 G)
recMove and storeMove functions based on example code for receiving single input char 
https://forum.arduino.cc/index.php?topic=288234.
all other functions written by Shiva Nathan
to control servomotors based on received serial character
21 April 2017
Upload this sketch FIRST and THEN run python code
*/

#include <Servo.h>

//Establish a servo for each finger
Servo pinky;
Servo ring;
Servo middle;
Servo index;
Servo thumb;

//Servo degree of movement to curl or extend finger all the way 
// REVERSE FOR THUMB SERVO
int curled = 120;
int extended = 0;

//Establish Arduino pin connections for each servo
int servoPin = 8; //HiTec HS-82MG servos use 6 volts
int servoPin2 = 9;
int servoPin3 = 10;
int servoPin4 = 11;
int servoPin5 = 12;

char receivedChar;
boolean newData = false;

void setup() {
 //Establish serial communication at 9600 baud
 Serial.begin(9600);
 Serial.println("<Arduino is ready>");
 //Enable servomotors to their respective pins
 pinky.attach(servoPin);
 ring.attach(servoPin2);
 middle.attach(servoPin3);
 thumb.attach(servoPin4);
 index.attach(servoPin5);
}

void loop() {
  //Receive character from serial, store it as receivedChar, and make corresponding receivedChar
 recMove();
 storeMove();
 makeMove();
}

//Receive character from serial
void recMove() {
 if (Serial.available() > 0) {
 receivedChar = Serial.read();
 newData = true;
 }
}

//Print received character from serial and store it in receivedChar
void storeMove() {
 if (newData == true) {
 Serial.print("receivedChar is: ");
 Serial.println(receivedChar);
 newData = false;
 }
}

void makeMove() {
 if (receivedChar == 'g') { playGun(); }
 else if (receivedChar == 'p') { playPaper(); }
 else if (receivedChar == 's') { playScissors(); }
 else { playRock(); }
}

void playRock() {
   index.write(curled);
    middle.write(curled);
    ring.write(curled);
    pinky.write(curled);
    thumb.write(extended); //the thumb servo is oriented in the opposite direction as the rest 
}


void playPaper() {
  index.write(extended);
    middle.write(extended);
    ring.write(extended);
    pinky.write(extended);
    thumb.write(curled); //the thumb servo is oriented in the opposite direction as the rest 
}

void playScissors() {
  index.write(extended);
    middle.write(extended);
    ring.write(curled);
    pinky.write(curled);
    thumb.write(extended); //the thumb servo is oriented in the opposite direction as the rest 
}

void playGun() {
  index.write(extended);
    middle.write(curled);
    ring.write(curled);
    pinky.write(curled);
    thumb.write(curled); //the thumb servo is oriented in the opposite direction as the rest 
}
