// this code is referenced [uCam Development | Mbed](https://os.mbed.com/users/ms523/notebook/ucam-development/)
// #include <uCamII.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(3, 2); // (3:RX, 2:TX) 
const unsigned char SYNC[] = {0xAA, 0x0D, 0x00, 0x00, 0x00, 0x00};
const unsigned char ACK[] = {0xAA, 0x0E, 0x0D, 0x00, 0x00, 0x00};

byte _SYNC_COMMAND[6] = {0xAA, 0x0D, 0x00, 0x00, 0x00, 0x00};

// #define cameraDebugSerial

void setup() {

  Serial.begin(57600);
  while (!Serial) {
      Serial.println("wait");
  }

  Serial.println("serial connectted");
  Serial.println("");

  unsigned char buf[6] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00};

  mySerial.begin(57600);
  Serial.println("---uCam Initailse---");


  // this will give 60 attempts to syn with the uCam module
  for (int i=0; i<=60; i++) {
    // send out the sync sync command
    Serial.print("sending out SYNC command ");
    Serial.print(i+1);
    Serial.println(" times");
    for (int i=0; i<6; i++) {
      // mySerial.write(SYNC[i]);
      ;
    }
    // if you use byte array, below is also usable insted of above for repeat `mySerial.write(SYNC[i])`
    // mySerial.write(_SYNC_COMMAND, sizeof(_SYNC_COMMAND));


    // get response from uCam
    if (mySerial.available() > 0) {
      Serial.println("");
      for (int i=0; i<6; i++) {
        buf[i] = mySerial.read();
      }
    }

    if (buf[0] == 0xAA && buf[1] == 0x0E && buf[2] == 0x0D && buf[4] == 0x00 && buf[5] == 0x00) {
      Serial.print("ACK received: ");
      for (int i=0; i<6; i++) {
        Serial.print(buf[i], HEX);
      }
      Serial.println("");



      // get response from uCam
      if (mySerial.available() > 0) {
        for (int i=0; i<6; i++) {
          buf[i] = mySerial.read();
        }

        if (buf[0] == 0xAA && buf[1] == 0x0D && buf[2] == 0x00 && buf[3] == 0x00 && buf[4] == 0x00 && buf[5] == 0x00) {
          Serial.print("SYNC received: ");
          for (int i=0; i<6; i++) {
            Serial.print(buf[i], HEX);
          }
          Serial.println("");

          Serial.println("Sending out ACK command");
          for (int i=0; i<6; i++) {
            mySerial.write(ACK[i]);
          }
          Serial.print("SYNC complete after ");
          Serial.print(i+1);
          Serial.println(" attempts");
          break;
        } else {
          Serial.println("No SYNC received... trying again...");
        }      
      } else {
        Serial.println("No ACK received... trying again...");
      }

    }

    if (i==60) {
      Serial.println("Testing failed - Too many attempts");
    }

    delay(5 + i);
  }


}

void loop() {

}