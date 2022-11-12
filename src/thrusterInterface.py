import rospy
from std_msgs.msg import String
from thrusters.msg import thrusterPercents
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
    dc3 = msg.t3
    dc4 = msg.t4
    dc5 = msg.t5
    dc6 = msg.t6
    rospy.loginfo(dc1)
    rospy.loginfo(dc2)
    rospy.loginfo(dc3)
    rospy.loginfo(dc4)
    rospy.loginfo(dc5)
    rospy.loginfo(dc6)
    
    thruster_channel0.duty_cycle = int(((dc1 * (2.0/5)+ 1500)*6.5536))
    thruster_channel1.duty_cycle = int(((dc2 * (2.0/5)+ 1500)*6.5536))
    thruster_channel2.duty_cycle = int(((dc3 * (2.0/5)+ 1500)*6.5536))
    thruster_channel3.duty_cycle = int(((dc4 * (2.0/5)+ 1500)*6.5536))
    thruster_channel4.duty_cycle = int(((dc5 * (2.0/5)+ 1500)*6.5536))
    thruster_channel5.duty_cycle = int(((dc6 * (2.0/5)+ 1500)*6.5536))

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
    time.sleep(0.1)
    thruster_channel1.duty_cycle = 0x2666
    print("Done")
    time.sleep(0.1)
    thruster_channel2.duty_cycle = 0x2666
    print("Done")
    time.sleep(0.1)
    thruster_channel3.duty_cycle = 0x2666
    print("Done")
    time.sleep(0.1)
    thruster_channel4.duty_cycle = 0x2666
    print("Done")
    time.sleep(0.1)
    thruster_channel5.duty_cycle = 0x2666
    print("Done")
    time.sleep(0.1)

    rospy.init_node('thrusterSub', anonymous=True)

    rospy.Subscriber("thusters", thrusterPercents, callback=callback)

    

    rospy.spin()
