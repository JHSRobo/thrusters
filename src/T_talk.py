import rospy
from std_msgs.msg import String
from thrusters.msg import thrusterPercents
    
if __name__ == '__main__':
    pub = rospy.Publisher('thusters', thrusterPercents, queue_size=10)
    rospy.init_node("t_talk", anonymous=True)
    r = rospy.Rate(10)
    msg = thrusterPercents()
    msg.t1 = int(1500/10000*65536)
    msg.t2 = int(1500/10000*65536)

    while not rospy.is_shutdown():
        c_t1 = int(input("Enter in a number 1: "))
        c_t2 = int(input("Enter in a number 2: "))
        msg.t1 = int(c_t1/10000*65536)
        msg.t2 = int(c_t2/10000*65536)
        rospy.loginfo(msg)
        pub.publish(msg)
        r.sleep()