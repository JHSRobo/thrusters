#!/usr/bin/env python3
import time
from adafruit_servokit import ServoKit
import board
import busio
import adafruit_pca9685

if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA)
    shield = adafruit_pca9685.PCA9685(i2c)
    kit = ServoKit(channels = 16)
    shield.frequency = 100
    
    thruster_channels = []

    for i in range(6):
        thruster_channels.append(shield.channels[i])
        thruster_channels[i].duty_cycle = 0x2666
        print("Thruster On")
        time.sleep(0.1)

    while 1:
        range = int(input("Enter a value: "))
        channel = int(input("Enter in a channel between 0 & 5: "))

        thruster_channels[channel].duty_cycle = int(range * 6.5536)
        print(int(range * 6.5536))
        print(channel)

        time.sleep(5)
        thruster_channels[channel].duty_cycle = 0x2666
