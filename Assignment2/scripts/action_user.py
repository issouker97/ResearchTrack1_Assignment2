#!/usr/bin/env python

import rospy
import actionlib
import actionlib.msg
import assignment_2_2022.msg
from std_srvs.srv import *
import sys
import select
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Twist
from assignment_2_2022.msg import Posxy_velxy
from colorama import Fore, Style
from colorama import init

init()

# callback function for the subscriber
def publisher(msg):
    global pub
    # get the position information
    pos = msg.pose.pose.position
    # get the velocity information
    velocity = msg.twist.twist.linear
    # custom message
    posxy_velxy = Posxy_velxy()
    # assign the parameters of the custom message
    posxy_velxy.msg_pos_x = pos.x
    posxy_velxy.msg_pos_y = pos.y
    posxy_velxy.msg_vel_x = velocity.x
    posxy_velxy.msg_vel_y = velocity.y
    # publish the custom message
    pub.publish(posxy_velxy)

def action_client():
    # create the action client
    action_client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2022.msg.PlanningAction)
    # wait for the server to be started
    action_client.wait_for_server()
    
    status_goal = False
	
    while not rospy.is_shutdown():
        # Get the keyboard inputs
        print(Fore.GREEN + "Please enter position of the target or type c to cancel it ")
        x_pos_input = input(Fore.MAGENTA + "X position of target: ")
        y_pos_input = input(Fore.MAGENTA + "Y position of target: ")
        
        # If user entered 'c' cancel the goal
        if x_pos_input == "c" or y_pos_input == "c":
            # Cancel the goal
            action_client.cancel_goal()
            status_goal = False
        else:
            # Convert numbers from string to float
            x_pos_send = float(x_pos_input)
            y_pos_send = float(y_pos_input)
            # Create the goal to send to the server
            goal = assignment_2_2022.msg.PlanningGoal()
            goal.target_pose.pose.position.x = x_pos_send
            goal.target_pose.pose.position.y = y_pos_send
					
            # Send the goal to the action server
            action_client.send_goal(goal)
            status_goal = True


def main():
    # initialize the node
    rospy.init_node('action_user')
    # global publisher
    global pub
    # publisher: send a message which contains two parameters (velocity and position)
    pub = rospy.Publisher("/posxy_velxy", Posxy_velxy, queue_size=1)
    # subscriber: get from "Odom" two parameters (velocity and position)
    sub_from_Odom = rospy.Subscriber("/odom", Odometry, publisher)
    # call the function action_client
    action_client()

if __name__ == '__main__':
    main()
