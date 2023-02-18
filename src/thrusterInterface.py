#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from thrusters.msg import thrusterPercents
import time
from adafruit_servokit import ServoKit
import board
import busio
import adafruit_pca9685

def thrusterCallback(msg):
    global thruster_channels
    msglist = [msg.t1, msg.t2, msg.t3, msg.t4, msg.t5, msg.t6]
    
    for i in range(6):
        thruster_channels[i].duty_cycle = int(((msglist[i] * 0.4 + 1500) * 6.5536))

if __name__ == '__main__':
    rospy.init_node('thruster_interface')
    i2c = busio.I2C(board.SCL, board.SDA)
    try: shield = adafruit_pca9685.PCA9685(i2c, reference_clock_speed = 25000000 * 1.04)
    except: rospy.logwarn("Cannot connect to PCA9685. Ignore this if thrusters are unplugged.")
    else: 
        kit = ServoKit(channels = 16)
        shield.frequency = 100
        
        thruster_channels = []

        for i in range(6):
            thruster_channels.append(shield.channels[i])
            thruster_channels[i].duty_cycle = 0x2666
            print("Thruster On")
            time.sleep(0.1)
        
        rospy.Subscriber("thrusters", thrusterPercents, thrusterCallback)

    rospy.spin()
