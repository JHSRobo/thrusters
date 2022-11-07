import rospy
from std_msgs.msg import String
from thrusterInterface.msg import thrusterPercents
import time
import keyboard
from adafruit_servokit import ServoKit
import board
import busio
import adafruit_pca9685

def callback(msg):
    rospy.loginfo(msg)
    dc1 = msg.t1
    dc2 = msg.t2
    rospy.loginfo(dc1)
    rospy.loginfo(dc2)
    
    thruster_channel0.duty_cycle = dc1
    thruster_channel1.duty_cycle = dc2

    rospy.loginfo(thruster_channel0)
    rospy.loginfo(thruster_channel1)

if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA)
    shield = adafruit_pca9685.PCA9685(i2c)
    kit = ServoKit(channels = 16)
    shield.frequency = 100
    thruster_channel0 = shield.channels[0]
    thruster_channel1 = shield.channels[1]

    thruster_channel0.duty_cycle = 0x2666
    print("Done")
    time.sleep(2)
    thruster_channel1.duty_cycle = 0x2666
    print("Done")
    time.sleep(2)

    rospy.init_node('thrusterSub', anonymous=True)

    rospy.Subscriber("thusters", thrusterPercents, callback=callback)

    

    rospy.spin()
