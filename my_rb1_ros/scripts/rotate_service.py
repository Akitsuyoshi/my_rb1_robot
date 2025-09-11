#! /usr/bin/env python

import rospy
from std_srvs.srv import Empty, EmptyResponse 
from geometry_msgs.msg import Twist

def my_callback(request):
    rospy.loginfo("Service Requested")
    rospy.loginfo("Service Completed")
    return EmptyResponse() # the service Response class, in this case EmptyResponse

rospy.init_node('rotate_service_server') 
my_service = rospy.Service('/rotate_robot', Empty , my_callback) # create the Service called move_bb8_in_circle with the defined callback

rospy.loginfo("Service Ready")
rospy.spin() # mantain the service open.