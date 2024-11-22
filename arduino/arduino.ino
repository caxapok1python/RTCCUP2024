// Include
#include "Arduino.h" // basic library
#include "reset.h" // rescure reset
#include "joystick.h" // joystick library
#include "motors.h" // motors driver library
#include "manipulator.h" // manipulator library
#include "rpi.h" // rpi library (no code)
// #include "gyro.h" // gyto library (no code)
#include "automotive.h" // automatisation library


int cam = 0;

// SETUP
void setup(){
    setupRescure(); // setup sercure reset pin

    // debug
    // setup serial
    Serial.begin(115200);
    delay(10);

    // setup components
    // firmata serail 57600 baud
    setupJoystick(); // joystick

    setupMotors(); // motors: setup drivers
    Serial.println("[+] Motors has been configurated!!");

    setupMan(); // manipulator
    Serial.println("[+] Manipulator has been configurated!!");
    // setupGyro(); // gyro & acceleration

}

// LOOP

void loop(){
    // debug
    // testMan();
    // debugJoystick();
    // return;
    // calibrateSticks();

    // TODO: camera flip button
    // main
    // read joystic
    readSticks(); // sticks
    controlMotors(); // motors
    readJoyButton(); // button
    readTumblers(); // tumblers
    if (buttonLeft){ //stop motors if button pressed
        leftStick = rightStick = stickRange[2];
        controlMotors(); // motors
        if (midTumbler < tumblerRange[0]){ // middle tumbler up
            resetFunc();
        }
        // if (midTumbler > tumblerRange[1]) { // switch camera if mid tumbler pressed to low
        //     cam++;
        //     Serial.print("cam: " );
        //     Serial.println(cam % 3);
        //     analogWrite(CAM_SWITHER, camPose[cam % 3]);
        //     // cam_switcher.write(cam_pos[cam % 3]);
        //     // digitalWrite(CAM_SWITCHER_PORT, switchCameraStat);
        // }
        // return;
    }
    
    

    // control robot components
    
    controlMan(); // manipulator
    

    // automotive
    checkAutomotive(); // check start for automotive
}

