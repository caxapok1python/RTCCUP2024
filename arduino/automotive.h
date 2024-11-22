#include "Arduino.h"
#include "MPU6050.h"
#include "GyverPID.h" // pid regulator

// banka automotive
#define PODEZD_K_BANKE 40  // max 255

// autopilot directions
#define FORWARD 1
#define BACKWARD 0

// reset pin
#define RST 12

// pid regulator coefs
const float kp = 1.0;
const float ki = 1.0;
const float kd = 1.0;
const float DT = 30;

MPU6050 mpu;
GyverPID regulator(kp, ki, kd, DT);

// Automotive banka
void autoCatch(){
  man2Pos(defaultPos);
  readCap();
  while (!capState){
    manualPower(LEFT, PODEZD_K_BANKE);
    manualPower(RIGHT, PODEZD_K_BANKE);
    readCap();
  }
  manualPower(LEFT, 0);
  manualPower(RIGHT, 0);
  manCatch(true);
  delay(500);
  man2Pos(workPos);
  delay(1000);
}

void time_banka(){
  // подготовка
  manCatch(false);  // разжимаем клешню
  manualPower(LEFT, 0); // остановка левой стороны
  manualPower(RIGHT, 0); // остновка правой стороны
  delay(1000); // ждем не понятно чего
  manualPower(LEFT, PODEZD_K_BANKE); // поехали левым мотором
  manualPower(RIGHT, PODEZD_K_BANKE); // плехали правым мотором
  delay(1500); // ждем отъезда
  manualPower(LEFT, 0); // остановка левой стороны
  manualPower(RIGHT, 0); // остновка правой стороны
  manCatch(true); // зажимаем клешню
  delay(200); // ожидание между 
  man2Pos(workPos); // поднимаем манипулятор
  delay(200);
  manualPower(LEFT, -1 * PODEZD_K_BANKE); // отъчезжаем левым мотором
  manualPower(RIGHT, -1 * PODEZD_K_BANKE); // отъезжаем правым мотором
  delay(1000); // ждем пока отъедет
  manualPower(LEFT, 0); // остановка левой стороны
  manualPower(RIGHT, 0); // остновка правой стороны
}

// check button and run automatic funcs
void checkAutomotive(){
  if (modeTumbler > tumblerRange[1]){ // mode thumbler down
    time_banka();
    delay(100);
  }

  if (midTumbler > tumblerRange[1]){  // middle thembler down
    delay(50);
    // control Arduino from Raspberry PI
    runRPI(); 
  }
}

// ПИД по гироскопу
// читаем гироскопы




//auto drive 
void autopilot(const short int direction, const short int speed){
  if (direction == FORWARD){ // drive forward
    return;
  }
  // drive backward
  ;
}

