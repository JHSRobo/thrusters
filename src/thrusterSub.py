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
    
    dc1 = int(((((msg.t1 * 3) + 1500) / 10_000) * 65536))
    dc2 = int(((((msg.t2 * 3) + 1500) / 10_000) * 65536))
    dc3 = int(((((msg.t3 * 3) + 1500) / 10_000) * 65536))
    dc4 = int(((((msg.t4 * 3) + 1500) / 10_000) * 65536))
    dc5 = int(((((msg.t5 * 3) + 1500) / 10_000) * 65536))
    dc6 = int(((((msg.t6 * 3) + 1500) / 10_000) * 65536))
    
    
    rospy.loginfo(dc1)
    rospy.loginfo(dc2)
    rospy.loginfo(dc3)
    rospy.loginfo(dc4)
    rospy.loginfo(dc5)
    rospy.loginfo(dc6)
    
    thruster_channel0.duty_cycle = dc1
    thruster_channel1.duty_cycle = dc2
    thruster_channel2.duty_cycle = dc3
    thruster_channel3.duty_cycle = dc4
    thruster_channel4.duty_cycle = dc5
    thruster_channel5.duty_cycle = dc6

    rospy.loginfo(thruster_channel0)
    rospy.loginfo(thruster_channel1)
    rospy.loginfo(thruster_channel2)
    rospy.loginfo(thruster_channel3)
    rospy.loginfo(thruster_channel4)
    rospy.loginfo(thruster_channel5)

if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA)
    shield = adafruit_pca9685.PCA9685(i2c)
    kit = ServoKit(channels = 16)
    shield.frequency = 100
    
    thruster_channel0 = shield.channels[0]
    thruster_channel1 = shield.channels[1]
    thruster_channel2 = shield.channels[2]
    thruster_channel3 = shield.channels[3]
    thruster_channel4 = shield.channels[4]
    thruster_channel5 = shield.channels[5]

    thruster_channel0.duty_cycle = 0x2666
    print("Done")
    time.sleep(2)
    thruster_channel1.duty_cycle = 0x2666
    print("Done")
    time.sleep(2)
    thruster_channel2.duty_cycle = 0x2666
    print("Done")
    time.sleep(2)
    thruster_channel3.duty_cycle = 0x2666
    print("Done")
    time.sleep(2)
    thruster_channel4.duty_cycle = 0x2666
    print("Done")
    time.sleep(2)
    thruster_channel5.duty_cycle = 0x2666
    print("Done")
    time.sleep(2)

    rospy.init_node('thrusterSub', anonymous=True)

    rospy.Subscriber("thusters", thrusterPercents, callback=callback)

    

    rospy.spin()
