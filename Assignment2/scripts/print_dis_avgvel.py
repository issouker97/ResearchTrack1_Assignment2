#! /usr/bin/env python
"""
.. module:: print_dis_avgvel
	:platform: Unix
	:synopsis: Python module for the print_dis_avgvel

.. moduleauthor:: KERMADJ YOUNES s5447235@studenti.unige.it


Python module for the Subscriber node (print_dis_avgvel).

This node for printing both the distance that separates the robot from the target and its average speed.
In addition, It subscribes to the robot position and speed, this will be through using a custom message.
A parameter will be used to set the frequency of publishing the data

Subscribes to:

- **/posxy_velxy** (message type: `Posxy_velxy`)

---

"""

import rospy
import math
import time
from assignment_2_2022.msg import Posxy_velxy
from colorama import init
init()
from colorama import Fore, Back, Style

class PrintInfo:
    def __init__(self):
	    
          """
          This function makes a new PrintInfo object. The object has three things:
          A number that tells how often to print the information.
          A number that tells when the information was last printed.
          A thing that listens to messages about the position and speed of the robot and does something with them..

          """

          # Get the publish frequency parameter
          self.freq = rospy.get_param("frequency")

          # Last time the info was printed
          self.printed = 0

          # Subscriber to the position and velocity topic
          self.sub_pos = rospy.Subscriber("/posxy_velxy", Posxy_velxy, self.posvel_callback)

    def posvel_callback(self, msg):
	    
        """
        This function defines a method called posvel_callback that takes two parameters: self and msg. 
        The method is used as a callback function for the subscriber object that listens to the topic /posxy_velxy. 
  
        """
        # Compute time period in milliseconds
        period = (1.0/self.freq) * 1000
        
        # Get current time in milliseconds
        curr_time = time.time() * 1000

        # Check if the current time minus the last printed time is greater than the period
        if curr_time - self.printed > period:
            # Get the desired position from ROS parameters
            target_x = rospy.get_param("des_pos_x")
            target_y = rospy.get_param("des_pos_y")

            # Get the actual position of the robot from the message
            robot_x = msg.msg_pos_x
            robot_y = msg.msg_pos_y

            # Compute the distance between the desired and actual positions
            distance = round(math.dist([target_x, target_y], [robot_x, robot_y]),2)
            
            # Get the actual velocity of the robot from the message
            vel_x = msg.msg_vel_x
            vel_y = msg.msg_vel_y            

            # Compute the average speed using the velocity components from the message
            average_speed = round(math.sqrt(vel_x**2 + vel_y**2),2)

            # Print the distance and speed information
            rospy.loginfo(Fore.GREEN + "Distance to target: %s [m]", distance)
            rospy.loginfo(Fore.MAGENTA + "Robot average speed: %s [m/s]", average_speed)

            # Update the last printed time
            self.printed = curr_time

def main():
	
    """
    This code defines a function called main that tries to suppress the timestamps from the log messages, 
    initializes the node with the name "print_dis_avgvel" and creates an object of the PrintInfo class that subscribes to a topic and prints the distance and speed information of the robot at a given frequency, and waits for messages.
    The code also calls the main function if the file is being run directly.
  
    """
   
    # Suppress the timestamps from the log messages
    #rospy.set_param('/rosconsole/formatter/time', 'none')	
    
    # Initialize the node
    rospy.init_node('print_dis_avgvel')
    
    # Create an instance of the PrintInfo class
    print_dis_avgvel = PrintInfo()
    
    # Wait for messages
    rospy.spin()

if __name__ == "__main__":
    main()
