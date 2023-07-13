#include <Encoder.h>
#include "utils.h"
#include <AccelStepper.h>

#define ENCODER_DO_NOT_USE_INTERRUPTS
Encoder myEnc(2, 3);

AccelStepper vertStepper(1, 7, 4); // pin 7 = step, pin 4 = direction
#define ENABLE_MOTOR 8
#define HALL_SENSOR 5
#define LED_PIN 6
double pi = 3.1415;

long newPosition = 0;
double theta = 0.0;
double oldTheta = 0.0;
double theta_dot = 0.0;
double max_theta_dot = 8.0;
long read_timerate = 10; // read encoder every 10ms
double timestep = read_timerate / 1000.0;
long encoderSteps = 1200;
bool ledState = false;

bool isZero = false;
bool startFlag = false;
long motorAngle = 0;
bool clockwise = true;
float speed = 150.0;
float homingSpeed = 150.0;
bool episodeDone = false;

unsigned long oldTime = 0.0;
unsigned long oldTimeSerial = 0.0;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(ENABLE_MOTOR, OUTPUT);
  pinMode(HALL_SENSOR, INPUT);
  digitalWrite(ENABLE_MOTOR, LOW);
  vertStepper.setMaxSpeed(10000.0);
  vertStepper.setSpeed(speed);
  
  Serial.begin(9600);
}

void loop() {

  // read encoder and magnetic switch
  if (millis() - oldTime >= read_timerate) {
    
    newPosition = myEnc.read();
    isZero = digitalRead(HALL_SENSOR);
    theta = getTheta(newPosition, encoderSteps);
    theta_dot = (theta - oldTheta) / timestep;
    theta_dot = clip(theta_dot, -max_theta_dot, max_theta_dot);

    Serial.print(theta);
    Serial.print(",");
    Serial.print(theta_dot);
    Serial.print(",");
    Serial.println(episodeDone);
    oldTheta = theta;
    oldTime = millis();
  }

  // read the serial for motor commands
  if (millis() - oldTimeSerial >= 5) {
    if (Serial.available() > 0) {
      // read the incoming string:
      String data = Serial.readStringUntil('\n');
      data = data.toFloat();  
      //Serial.println(speed);
      //vertStepper.setSpeed(speed);
    }
  }

  // map the motor angle
  if (isZero) {
    motorAngle = 0.0;
  }
  else {
    motorAngle = map(vertStepper.currentPosition(), -55, 55, -90, 90);
  }  

  // check if episode is done
  if (vertStepper.currentPosition() > 70.0 && clockwise) {
    // invert rotation
    vertStepper.setSpeed(-homingSpeed);
    clockwise = false;
    episodeDone = true;
  }
  else if (vertStepper.currentPosition() < -70.0 && !clockwise) {
    // invert rotation
    vertStepper.setSpeed(homingSpeed);
    clockwise = true;
    episodeDone = true;
  }

  // if (episodeDone) {
  //   if (vertStepper.currentPosition() < 0.005 && vertStepper.currentPosition() > -0.005) {
  //     //vertStepper.setCurrentPosition(0);
  //     startFlag = false;
  //   }
  // }

  if (startFlag) {
    digitalWrite(ENABLE_MOTOR, LOW);
    // when the pendulum passes through home position, reset steps count
    if (isZero) {
      vertStepper.setCurrentPosition(0);
      // if coming from a clockwise direction, use same speed sign
      if (clockwise) {
        vertStepper.setSpeed(speed);
      }
      else {
        vertStepper.setSpeed(-speed);
      }
    }
    vertStepper.runSpeed();
  }
  else {
    digitalWrite(ENABLE_MOTOR, HIGH);
    if (isZero) {
      startFlag = true;
    }
  }
  // count steps
  
  // Serial.println(vertStepper.currentPosition());
    
}