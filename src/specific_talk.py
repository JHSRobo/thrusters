import time
import keyboard
from adafruit_servokit import ServoKit
import board
import busio
import adafruit_pca9685

if __name__ == '__main__':
  i2c = busio.I2C(board.SCL, board.SDA)
  shield = adafruit_pca9685.PCA9685(i2c)
  kit = ServoKit(channels = 16)
  shield.frequency = 100
    
  thruster_channels = shield.channels[0:6]

  thruster_channels[0].duty_cycle = 0x2666
  print("Done")
  time.sleep(1)
  thruster_channels[1].duty_cycle = 0x2666
  print("Done")
  time.sleep(1)
  thruster_channels[2].duty_cycle = 0x2666
  print("Done")
  time.sleep(1)
  thruster_channels[3].duty_cycle = 0x2666
  print("Done")
  time.sleep(1)
  thruster_channels[4].duty_cycle = 0x2666
  print("Done")
  time.sleep(1)
  thruster_channels[5].duty_cycle = 0x2666
  print("Done")
  time.sleep(1)
  
  while 1:
    range = int(input("Enter a value" ))
    channel = int(input("Channel number: "))
    
    thruster_channels[channel] = (range * 6.5536)
