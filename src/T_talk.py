import rospy
from std_msgs.msg import String
from thrusterInterface.msg import thrusterPercents
    
if __name__ == '__main__':
    pub = rospy.Publisher('thusters', thrusterPercents, queue_size=10)
    rospy.init_node("t_talk", anonymous=True)
    r = rospy.Rate(10)
    msg = thrusterPercents()

    while not rospy.is_shutdown():
        c_t1 = int(input("Enter in a number 1: "))
        c_t2 = int(input("Enter in a number 2: "))
        c_t3 = int(input("Enter in a number 3: "))
        c_t4 = int(input("Enter in a number 4: "))
        c_t5 = int(input("Enter in a number 5: "))
        c_t6 = int(input("Enter in a number 6: "))
        msg.t1 = c_t1
        msg.t2 = c_t2
        msg.t3 = c_t3
        msg.t4 = c_t4
        msg.t5 = c_t5
        msg.t6 = c_t6
        rospy.loginfo(msg)
        pub.publish(msg)
        r.sleep()
