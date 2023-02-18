#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from thrusters.msg import thrusterPercents
import time
from pca9685 import PCA9685

def thrusterCallback(msg):
    msglist = [msg.t1, msg.t2, msg.t3, msg.t4, msg.t5, msg.t6]
    for i in range(6):
        pca.channel_set_duty(i, 0.15 - msglist[i] / 25000)

if __name__ == '__main__':
    rospy.init_node('thruster_interface')

    # Create PCA object
    try: pca = PCA9685(bus=1)
    except: rospy.logwarn("Cannot connect to PCA9685. Ignore this if thrusters are unplugged")
    else:
      pca.set_pwm_frequency(100)
      pca.output_enable()

      # Initialize the thrusters
      pca.channels_set_duty_all(0.15)
      time.sleep(1)

    rospy.Subscriber("thrusters", thrusterPercents, thrusterCallback)

    rospy.spin()
