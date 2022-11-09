#include <Arduino_LSM6DS3.h>

float ax, ay, az, gx, gy, gz;
float old_ax=0;
float der_ax=0; 
int timeout = 50; 

int counter = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

}

void loop() {

  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
    IMU.readAcceleration(ax, ay, az);
 
    IMU.readGyroscope(gx, gy, gz);
    // Serial.print("ax: "); 
    // Serial.print(ax); 
    // Serial.print(", ");
    // // Serial.print(", ay: "); 
    // Serial.print(ay); 
    // Serial.print(", ");
    // // Serial.print(", az: "); 
    // Serial.print(az); 
    // Serial.print(", ");
    // // Serial.print(", gx: "); 
    // Serial.print(gx); 
    // Serial.print(", ");
    // // Serial.print(", gy: "); 
    // Serial.print(gy); 
    // Serial.print(", ");
    // // Serial.print(", gz: "); 
    // Serial.println(gz); 

    der_ax = (ax-old_ax) / (float)100 ; 
    // der_gz = (gz-old_gz) / (float)100;

    Serial.println(der_ax); 
    // Serial.print(", ");
    // Serial.println(der_gz); 

    if(der_ax >= .025 && gz < 0){
      // Serial.print (counter);
      Serial.println(" fast hit");
      delay(timeout);
      // counter += 1;
    }
    else if(der_ax >= .007 && gz < 0 ){
      // Serial.print (counter);
      Serial.println(" slow hit");
      delay(timeout);
      // counter += 1;
    }
  }

  delay(100);

  old_ax = ax; 
  // old_gz = gz; 
}
