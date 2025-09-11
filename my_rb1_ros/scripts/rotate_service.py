#! /usr/bin/env python

import rospy
from my_rb1_ros.srv import Rotate, RotateResponse 
from geometry_msgs.msg import Twist

def my_callback(request):
    rospy.loginfo("Service Requested")
    rospy.loginfo("Service Completed")
    return RotateResponse() # the service Response class, in this case EmptyResponse

rospy.init_node('rotate_service_server') 
my_service = rospy.Service('/rotate_robot', Rotate , my_callback) # create the Service called move_bb8_in_circle with the defined callback

rospy.loginfo("Service Ready")
rospy.spin() # mantain the service open.