import rospy
from std_msgs.msg import String
from thrusters.msg import thrusterPercents
import time
import keyboard
from adafruit_servokit import ServoKit
import board
import busio
import adafruit_pca9685

def thrusterCallback(msg, thruster_channels):
    rospy.loginfo(msg)
    
    msglist = [msg.t1, msg.t2, msg.t3, msg.t4, msg.t5, msg.t6]
    
    rospy.loginfo(msglist)
    
    for i in range(6);
        thruster_channels[i].duty_cycle = int(((msg[i] * (2.0/5)+ 1500)*6.5536))
        
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
        time.sleep(0.1)

    rospy.init_node('thrusterSub', anonymous=True)

    rospy.Subscriber("thusters", thrusterPercents, callback = thrusterCallback(msg, thruster_channels))

    

    rospy.spin()
