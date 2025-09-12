#! /usr/bin/env python

import rospy
import math
from tf.transformations import euler_from_quaternion
from my_rb1_ros.srv import Rotate, RotateResponse 
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


yaw = 0.0

# Converts quanternion(x, y, z, w) to euler angles(roll, pitch, yaw) to get yaw
# Reference: https://www.theconstruct.ai/ros-qa-135-how-to-rotate-a-robot-to-a-desired-heading-using-feedback-from-odometry/
def odom_callback(msg):
    global yaw
    orient = msg.pose.pose.orientation
    orients = [orient.x, orient.y, orient.z, orient.w]
    (_, _, yaw) = euler_from_quaternion(orients)

def normalize_rad(rad):
    # arctan(y, x) gives us normalized angle between -pi and pi, with y and x cordinates
    return math.atan2(math.sin(rad), math.cos(rad))

def rotate_callback(request):
    global yaw
    rospy.loginfo("Service Requested")
    my_pub =  rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rate = rospy.Rate(20)

    target_rad = math.radians(request.degrees)
    last_yaw = yaw
    rotated = 0.0

    move = Twist()
    speed = 0.3
    # propotional gain
    k = 0.6 
    while not rospy.is_shutdown():
        delt = normalize_rad(yaw - last_yaw)
        rotated += delt
        last_yaw = yaw
        remain = abs(target_rad) - abs(rotated)
        if remain <= math.radians(0.5):
            break
        # propotional control, using k * ramain
        speed = max(speed/30, min(speed, k * remain))
        move.angular.z = speed if request.degrees > 0 else -speed
        my_pub.publish(move)
        rate.sleep()

    # publish mutiple to stop drift
    move.angular.z = 0.0
    for _ in range(20):
        my_pub.publish(move)
        rate.sleep()
    response = RotateResponse()
    response.result = f"The robot rotated {request.degrees} degrees"
    rospy.loginfo("Service Completed")
    return response


rospy.init_node('rotate_service_server')
rospy.Subscriber('/odom', Odometry, odom_callback)
rospy.Service('/rotate_robot', Rotate, rotate_callback)
rospy.loginfo("Service Ready")
rospy.spin() # mantain the service open.