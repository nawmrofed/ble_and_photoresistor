#include <SoftwareSerial.h>


int CDSPin = 0; // 光敏電阻接在A0接腳
int CDSVal = 0; // 設定初始光敏電阻值為0 強度越大，電阻值越小；光強度越小，電阻值越大。
int ledPin = 7;      // LED connected to digital pin 9
typedef enum{
  Start,
  Record,
} Mode;
Mode mode = Start;
bool check = false;

boolean isNumeric(String str) {
    byte stringLength = str.length();
    if (stringLength == 0) {
        return false;
    }
    boolean seenDecimal = false;
    for(byte i = 0; i < stringLength; ++i) {
        if (isDigit(str.charAt(i))) {
            continue;
        }
        return false;
    }
    return true;
}

void setup() {
  Serial.begin(115200); //Baudrate 9600 , Choose your own baudrate 
//  Serial.begin(9600);
}

void loop() {   
  if (mode == Record)
  {
    int num = 0;
    if(Serial.available() > 0)
    {
      char c = Serial.read();
      if (c == '1')
      {
        check = true;
      }
      else if (c == '2')
      { 
        mode = Start;
        check = false;
      }
    }
    if (check)
    {
      Serial.println(analogRead(CDSPin));
      Serial.flush();
    }    
  }
  else
  {
    if(Serial.available() > 0) //When Serial receive something
    {
      char receive = Serial.read(); //Read from Serial Communication
      if(receive == 'S')
      {
        mode = Record;
        Serial.println('S');
      }
    }
  }
}
