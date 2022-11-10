import rospy
from std_msgs.msg import String
from thrusterInterface.msg import thrusterPercents
import time
import keyboard
from adafruit_servokit import ServoKit
import board
import busio
import adafruit_pca9685

def callback(msglist):
    rospy.loginfo(msglist)
    
    msglist = [msg.t1, msg.t2, msg.t3, msg.t4, msg.t5, msg.t6]
    
    dc = []
    
    for i in range(6):
        # Do some number crunching to shift the thruster percents to duty cycles
        thrustDc = int(((msglist[i] - 3.6) * 3 + 1500) * 6.5536)
        dc.append(thrustDc)
    
    rospy.loginfo(dc)
    
    for i in range(6):
        thruster_channels[i].duty_cycle = dc[i]

    rospy.loginfo(thruster_channels)

if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA)
    shield = adafruit_pca9685.PCA9685(i2c)
    kit = ServoKit(channels = 16)
    shield.frequency = 100
    
    thruster_channels = shield.channels[0:6]
    
    for i in range(6):
        thruster_channels[i].duty_cycle = 0x2666
        print("Done")
        # Give time so that the thrusters initialize correctly
        time.sleep(0.01)

    rospy.init_node('thrusterSub', anonymous=True)

    rospy.Subscriber("thusters", thrusterPercents, callback=callback)

    rospy.spin()
