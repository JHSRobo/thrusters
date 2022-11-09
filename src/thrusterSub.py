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
    
    dc = []
    
    for i in range(6):
        dc.append(int(((((msglist[i] * 3) + 1500) / 10000) * 65536)))
    
    
    rospy.loginfo(dc)
    
    for i in range(6):
        thruster_channels[i].duty_cycle = dc[i]

    rospy.loginfo(thruster_channels)

if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA)
    shield = adafruit_pca9685.PCA9685(i2c)
    kit = ServoKit(channels = 16)
    shield.frequency = 100
    
    msglist = {0:msg.t1, 1:msg.t2, 2:msg.t3, 3:msg.t4, 4:msg.t5, 5:msg.t6}
    
    thruster_channels = shield.channels[0:6]
    
    for i in range(6):
        thruster_channels[i].duty_cycle = 0x2666
        print("Done")
        # Give time so that the thrusters initialize correctly
        time.sleep(2)

    rospy.init_node('thrusterSub', anonymous=True)

    rospy.Subscriber("thusters", thrusterPercents, callback=callback)

    rospy.spin()
