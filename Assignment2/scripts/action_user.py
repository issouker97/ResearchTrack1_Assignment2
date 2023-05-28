#!/usr/bin/env python
"""
.. module:: action_user
	:platform: Unix
	:synopsis: Python module for the action_user

.. moduleauthor:: KERMADJ YOUNES s5447235@studenti.unige.it


An action client node that permits the user to set or cancel a target (x, y) and also publishes the robot's position and velocity
as a custom message (x, y, vel x, vel y), by using the values published on the subject /odom..

Functions:
    - `publisher()`: Use to get both position and velocity informations

    - `action_client()`: Get the keyboard inputs and also create the goal to send to the server.
  
Usage:
    - The user is able to set a parameter to send a target position or can also cancel an existing target with pressing 'c'.
    
    - User interface prompts to get the input of the user for executing the function above.
    
---

Global Variables:
    pub
     it is used to publish custom messages of type Posxy_velxy to the topic /posxy_velxy
       
"""


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
    """
    this function takes an odometry message as input and publishes a custom message that contains only the x and y componenets of the position
    and velocity of the rebot
    
    """
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
    """
    This function creates an action client that communicates with an action server called /reaching_goal that provides a service of planning a path for the robot to reach a target pose.
    The function asks the user to input the x and y coordinates of the target pose or type c to cancel the goal. 
    If the user enters c, the function cancels the current goal. Otherwise, the function sends the goal to the action server and waits for feedback. 

    """
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
    """
    This function creates a node called action_user that publishes and subscribes to custom messages that contain the position and velocity of the robot. 
    It also creates an action client that sends goals to an action server.
    """
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
