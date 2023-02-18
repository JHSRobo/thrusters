#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from thrusters.msg import thrusterPercents
import time
from pca9685 import PCA9685

def thrusterCallback(msg):
    global thruster_channels
    msglist = [msg.t1, msg.t2, msg.t3, msg.t4, msg.t5, msg.t6]
    
    for i in range(6):
        duty_cycle = int(msglist[i] * 0.163 + 614)
        pca.channel_set_duty(i, duty_cycle)

if __name__ == '__main__':
    rospy.init_node('thruster_interface')

    # Create PCA object
    pca = PCA9685(bus=1)
    pca.set_pwm_frequency(100)
    pca.output_enable()

    # Initialize the thrusters
    pca.channels_set_duty_all(614)
    time.sleep(0.1)
        
    rospy.Subscriber("thrusters", thrusterPercents, thrusterCallback)

    rospy.spin()
