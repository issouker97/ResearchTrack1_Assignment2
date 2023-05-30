#! /usr/bin/env python
"""
.. module:: goal_service
	:platform: Unix
	:synopsis: Python module for the goal_service

.. moduleauthor:: KERMADJ YOUNES s5447235@studenti.unige.it


This service node that when we activate, it will print the number of target reached and cancelled.

Subscribes to:

- **/reaching_goal/result**: Use to receive status updates on goals.

Service:

- **goal_service**: Service use to take the number of reached goals and canceled goals.

Functions:

    - `init(self)`: This function makes a class that can send and receive goals. It counts how many goals were done or stopped. It makes a service and a subscriber for this.
     
    - `result_callback(self, msg)`: This function is a callback method that handles the messages from the result topic. 
       
    - `data(self, req)`: This function defines a method called data that takes two parameters: self and req. 
          
Usage:
   
    - The `result_callback` It checks the status of the result and updates the counters for goals cancelled or reached accordingly
   
    - The `data` is used to return an object of type goal_rcResponse that contains the values of two attributes of self: goal_reached and goal_cancelled.

Variables:
    count_canceled : int
        Count the amount of canceled goals.
        
    count_reached : int
        Count  the amount of reached goals.
"""
import rospy  # Import the ROS python library
from assignment_2_2022.srv import goal_rc, goal_rcResponse  # Import the service and service response messages
import actionlib  # Import the actionlib library
import actionlib.msg  # Import the actionlib message library
import assignment_2_2022.msg  # Import the package message library

class Service:
    def __init__(self):
        
<<<<<<< HEAD
        """
        *This function can send and receive goals*
=======
         """
         *This function can send and receive goals*
>>>>>>> 58c13d211aa93d119d7e7ddde6085761d4af2be7
    
             Args:
                 self: Message that contains the status of the goal.
 
<<<<<<< HEAD
        """
=======
          """
>>>>>>> 58c13d211aa93d119d7e7ddde6085761d4af2be7
        
        # Initialize the counters for goals reached and cancelled
        self.goal_cancelled = 0
        self.goal_reached = 0

        # Create the service
        self.srv = rospy.Service('goal_service', goal_rc, self.data)

        # Subscribe to the result topic
        self.sub_result = rospy.Subscriber('/reaching_goal/result', assignment_2_2022.msg.PlanningActionResult, self.result_callback)

    def result_callback(self, msg):
        
        """
        *This function is use for checking the status of the results*
     
             Args:
                 self
                 msg: is the taken message 
               
<<<<<<< HEAD
        """
=======
          """
>>>>>>> 58c13d211aa93d119d7e7ddde6085761d4af2be7
        # Get the status of the result from the msg
        status = msg.status.status

        # Goal cancelled (status = 2)
        if status == 2:
            self.goal_cancelled += 1

        # Goal reached (status = 3)
        elif status == 3:
            self.goal_reached += 1

    def data(self, req):
<<<<<<< HEAD
        
=======
>>>>>>> 58c13d211aa93d119d7e7ddde6085761d4af2be7
        """
        *Used to return an object of type goal_rcResponse*
     
            Args:
                self
                req 
            
<<<<<<< HEAD
	        Returns:
                Service goal_rcResponse.
               
        """
=======
	    Returns:
                Service goal_rcResponse.
               
           """
>>>>>>> 58c13d211aa93d119d7e7ddde6085761d4af2be7
        # Return the response containing the current values of goal_cancelled and goal_reached
        return goal_rcResponse(self.goal_reached, self.goal_cancelled)


def main():
 
    """
    This is the Main entry point of our node.

        - Start to intialize the ROS node with the name "goal_service".
    
        - Create an instance of the Service class.  
    
        - Keeps the node activated by calling `rospy.spin()`.
<<<<<<< HEAD
    
    """
=======
     """
>>>>>>> 58c13d211aa93d119d7e7ddde6085761d4af2be7
    # Initialize the node
    rospy.init_node('goal_service')

    # Create an instance of the Service class
    goal_service = Service()

    # Wait for messages
    rospy.spin()


if __name__ == "__main__":
    main()
