String str;
#include<Servo.h>
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  servo1.attach(3);//1,2同側, 1,3左右2,4左右
  servo2.attach(5);
  servo3.attach(7);
  servo4.attach(9);
  servo1.write(100);
  servo2.write(120);
  servo3.write(80);
  servo4.write(80);
  delay(500);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()){
    str = Serial.readStringUntil('\n');
    if (str=="TurnOff"){
      servo1.write(40);
      servo3.write(130);
      delay(500);  
      servo1.write(100);
      servo3.write(80);
      delay(500);
      servo1.detach();
      servo3.detach();
    }else if (str=="TurnOn"){
      servo2.write(70);
      servo4.write(130);
      delay(500);  
      servo2.write(120);    
      servo4.write(80);
      delay(500);
      servo2.detach();
      servo4.detach();
    }
  }
}
