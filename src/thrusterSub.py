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
    
    dc = []
    
    for i in range(6):
        dc.append(int(((((dict(i + 1) * 3) + 1500) / 10000) * 65536)))
    
    
    rospy.loginfo(dc)
    
    for i in range(6):
        thruster_channels[i].duty_cycle = dc[i]

    rospy.loginfo(thruster_channels)

if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA)
    shield = adafruit_pca9685.PCA9685(i2c)
    kit = ServoKit(channels = 16)
    shield.frequency = 100
    
    dict = {1:msg.t1, 2:msg.t2, 3:msg.t3, 4:msg.t4, 5:msg.t5, 6:msg.t6}
    
    thruster_channels = shield.channels[0:6]
    
    for i in range(6):
        thruster_channels[i].duty_cycle = 0x2666
        print("Done")
        # Give time so that the thrusters initialize correctly
        time.sleep(2)

    rospy.init_node('thrusterSub', anonymous=True)

    rospy.Subscriber("thusters", thrusterPercents, callback=callback)

    

    rospy.spin()
