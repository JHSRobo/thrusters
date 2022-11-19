#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from thrusters.msg import thrusterPercents
import time
import logging
from adafruit_servokit import ServoKit
import board
import busio
import adafruit_pca9685

rospy.loginfo("logloglog")

def thrusterCallback(msg):
    global thruster_channels

    logging.info(f"The msg is {msg}")
    msglist = [msg.t1, msg.t2, msg.t3, msg.t4, msg.t5, msg.t6]
    
    # rospy.loginfo(msglist)
    logging.info(f"The msglist is {msglist}")
    
    for i in range(6):
        thruster_channels[i].duty_cycle = int(((msglist[i] * 0.4 + 1500) * 6.5536))
        logging.info(f"The thruster channel is {i} and is giving it a value of {int(((msglist[i] * 0.4 + 1500) * 6.5536))}")

if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA)
    shield = adafruit_pca9685.PCA9685(i2c)
    kit = ServoKit(channels = 16)
    shield.frequency = 100
    
    logging.basicConfig(filename="log/thrusterslog.log", level=logging.INFO)
    
    thruster_channels = []

    for i in range(6):
        thruster_channels.append(shield.channels[i])
        thruster_channels[i].duty_cycle = 0x2666
        print("Thruster On")
        time.sleep(0.1)

    rospy.init_node('thruster_interface')

    rospy.Subscriber("thrusters", thrusterPercents, thrusterCallback)
    rospy.logerr("Subscriber created")
    rospy.spin()
