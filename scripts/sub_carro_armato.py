#!/usr/bin/env python3
from RPi.GPIO import cleanup
from gpiozero.pins.pigpio import PiGPIOFactory
from carro_armato import Motore
from carro_armato import Ruote
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist


def callback(data, args):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.linear)
    args[0].avanti_dietro(data.linear.y)
    args[0].velocity_right(data.linear.y)
    args[1].avanti_dietro(data.linear.y)
    args[1].velocity_left(data.linear.y)
    args[2].avanti_dietro(-data.linear.y)
    args[2].velocity_right(-data.linear.y)
    args[3].avanti_dietro(data.linear.y)
    args[3].velocity_left(data.linear.y)
   
    
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    
    motoreFront_Right=Motore(26, 19, 13)
    motoreFront_Left=Motore(21, 20, 16)
    motoreBack_Right=Motore(17, 27, 22)
    motoreBack_Left=Motore(2, 3, 4)
    
   
    #rospy.Subscriber("/cmd_vel", Twist, callback, (motoreFront_Right,motoreFront_Left,motoreBack_Right,motoreBack_Left))
    rospy.Subscriber("motors_pub", Twist, callback, (motoreFront_Right,motoreFront_Left,motoreBack_Right,motoreBack_Left))
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
    print("Spengo")
    motoreFront_Right.spegnimento_motori()
    motoreFront_Left.spegnimento_motori()
    motoreBack_Right.spegnimento_motori()
    motoreBack_Left.spegnimento_motori()
    cleanup()


if __name__ == '__main__':
    print("ragionato")
    factory=PiGPIOFactory()
    listener()
    motoreFront_Right=None
    motoreFront_Left=None
    motoreBack_Right=None
    motoreBack_Left=None
    
    
    
    
    