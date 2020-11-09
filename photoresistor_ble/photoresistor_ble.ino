#include <SoftwareSerial.h>

SoftwareSerial HC06(10, 11); //HC06-TX Pin 10, HC06-RX to Arduino Pin 11
int CDSPin = 0; // 光敏電阻接在A0接腳
int CDSVal = 0; // 設定初始光敏電阻值為0 強度越大，電阻值越小；光強度越小，電阻值越大。
int ledPin = 7;      // LED connected to digital pin 9
int* cache;
typedef enum{
  Set,
  Start,
  Record,
} Mode;
Mode mode = Set;
unsigned long start_time = 0;
unsigned long current_time = 0;
unsigned long sample_cycle = 0;
unsigned long time_limit = 2.5;
bool record_mode = false;

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
  HC06.begin(9600); //Baudrate 9600 , Choose your own baudrate 
  Serial.begin(9600);
}

void loop() {   
  if (mode == Record)
  {
    int _size = 2500 / sample_cycle;
    cache = new int [_size];
    start_time = millis();
    cache[0] = analogRead(CDSPin);
    current_time = start_time;
    int num = 0;
    for (int i = 1; i < _size; i++)
    {
      num += sample_cycle;
      while ((current_time - start_time) < num)
      {
        current_time = millis();
      } 
      cache[i] = analogRead(CDSPin);
    }
    for (int i = 0; i < _size; i++)
    {
        bool check = true;
        while(check)
        {
          while(HC06.available() > 0 && HC06.read() == '1')
          {
              HC06.println(cache[i]);
              check = false;
          }
        }
    }
    delete cache;
    mode = Set;
  }
  else if (mode == Set)
  {
    if(HC06.available() > 0) //When HC06 receive something
    {
      String receive = HC06.readString(); //Read from Serial Communication
      if(isNumeric(receive))
      {
        sample_cycle = receive.toInt();
        mode = Start;
        HC06.println(sample_cycle);
      }
    }
  }
  else
  {
    if(HC06.available() > 0) //When HC06 receive something
    {
      char receive = HC06.read(); //Read from Serial Communication
      if(receive == 'S')
      {
        mode = Record;
        HC06.println('S');
      }
      else if(receive == 'Q')
        mode = Set;
    }
  }
}
