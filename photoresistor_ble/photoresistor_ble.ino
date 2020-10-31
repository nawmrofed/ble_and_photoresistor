#include <SoftwareSerial.h>

SoftwareSerial HC06(10, 11); //HC06-TX Pin 10, HC06-RX to Arduino Pin 11
int CDSPin = 0; // 光敏電阻接在A0接腳
int CDSVal = 0; // 設定初始光敏電阻值為0
////強度越大，電阻值越小；光強度越小，電阻值越大。
int ledPin = 7;      // LED connected to digital pin 9
int val = 0;         // variable to store the read value

void setup() {
  HC06.begin(9600); //Baudrate 9600 , Choose your own baudrate 
  Serial.begin(9600);
//  pinMode(ledPin, OUTPUT);  // sets the pin as output
}

void loop() {

//    val = 128;
//  analogWrite(ledPin, val); // analogRead values go from 0 to 1023, analogWrite values from 0 to 255
//  Serial.println(val);
  if(HC06.available() > 0) //When HC06 receive something
  {
    char receive = HC06.read(); //Read from Serial Communication
    if(receive == '1') //If received data is 1, turn on the LED and send back the sensor data
    {
      CDSVal = analogRead(CDSPin);
      HC06.println(CDSVal);
    }
  }  
  delay(50);  
}
