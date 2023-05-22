#! /usr/bin/env python

import rospy  # Import the ROS python library
from assignment_2_2022.srv import goal_rc, goal_rcResponse  # Import the service and service response messages
import actionlib  # Import the actionlib library
import actionlib.msg  # Import the actionlib message library
import assignment_2_2022.msg  # Import the package message library

class Service:
    def __init__(self):
        # Initialize the counters for goals reached and cancelled
        self.goal_cancelled = 0
        self.goal_reached = 0

        # Create the service
        self.srv = rospy.Service('goal_service', goal_rc, self.data)

        # Subscribe to the result topic
        self.sub_result = rospy.Subscriber('/reaching_goal/result', assignment_2_2022.msg.PlanningActionResult,
                                           self.result_callback)

    def result_callback(self, msg):
        # Get the status of the result from the msg
        status = msg.status.status

        # Goal cancelled (status = 2)
        if status == 2:
            self.goal_cancelled += 1

        # Goal reached (status = 3)
        elif status == 3:
            self.goal_reached += 1

    def data(self, req):
        # Return the response containing the current values of goal_cancelled and goal_reached
        return goal_rcResponse(self.goal_reached, self.goal_cancelled)


def main():
    # Initialize the node
    rospy.init_node('goal_service')

    # Create an instance of the Service class
    goal_service = Service()

    # Wait for messages
    rospy.spin()


if __name__ == "__main__":
    main()
