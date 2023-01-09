# thrusters
Recieves thruster values from /thrusters, and spins the thrusters with them. Convert that into a duty cycle and uses I2C. Range for thrusters is 1100 - 1900. Center is 1500 with a dead zone of 1475 - 1525

This package depends on adafruit_servokit, which is not supported by rosdep. We have added a line to ROVMIND/rov_bringup to install this package.

## Author and Maintainer: Nathan Peterson
