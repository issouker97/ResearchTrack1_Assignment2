#! /usr/bin/env python
"""
.. module:: bug_as
	:platform: Unix
	:synopsis: Python module for the bug_as

.. moduleauthor:: KERMADJ YOUNES s5447235@studenti.unige.it


This code is a ROS program that implements the bug0 algorithm for planning a path to a goal while avoiding obstacles.
It uses a laser scan sensor and an odometry sensor to get the information about the environment and the robot's pose.
It also uses two services to control the robot's motion: go to point and wall follower.
It also defines an action server that takes a goal as an input and publishes feedback and result messages
    
---

Global Variables:
srv_client_go_to_point_: the service client for the go to point service

srv_client_wall_follower_: the service client for the wall follower service

yaw_: the yaw angle of the robot

yaw_error_allowed_: the allowed error in yaw angle

position_: the position of the robot

pose_: the pose of the robot

desired_position_: the desired position of the robot

regions_: the regions of the laser scan

state_desc_: the list of strings for describing the state of the robot

state_: the state of the robot
       
"""
import rospy
from geometry_msgs.msg import Point, Pose, Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math
import actionlib
import actionlib.msg
import assignment_2_2022.msg
from tf import transformations
from std_srvs.srv import *
import time

srv_client_go_to_point_ = None
srv_client_wall_follower_ = None
yaw_ = 0
yaw_error_allowed_ = 5 * (math.pi / 180)  # 5 degrees
position_ = Point()
pose_ = Pose()
desired_position_ = Point()
desired_position_.z = 0
regions_ = None
state_desc_ = ['Go to point', 'wall following', 'done']
state_ = 0
# 0 - go to point
# 1 - wall following
# 2 - done
# 3 - canceled
# callbacks


def clbk_odom(msg):
    """
    This is the callback function for the odometry subscriber. It updates the global variables for the position, pose and yaw of the robot using the odometry message. 
    It also converts the quaternion orientation to euler angles using the transformations library
    
    """
    global position_, yaw_, pose_

    # position
    position_ = msg.pose.pose.position
    pose_ = msg.pose.pose

    # yaw
    quaternion = (
        msg.pose.pose.orientation.x,
        msg.pose.pose.orientation.y,
        msg.pose.pose.orientation.z,
        msg.pose.pose.orientation.w)
    euler = transformations.euler_from_quaternion(quaternion)
    yaw_ = euler[2]


def clbk_laser(msg):
     """
    This is the callback function for the laser scan subscriber. 
    It updates the global variable for the regions of the laser scan using the laser scan message.
    It divides the laser scan into five regions: right, fright, front, fleft and left. 
    It also takes the minimum distance in each region and caps it at 10 meters

    
    """
    global regions_
    regions_ = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:719]), 10),
    }


def change_state(state):
    """
 This is the function to change the state of the robot and call the appropriate services. It updates the global variable for the state of the robot and logs a message with the state description. 
 It also calls the go to point service and the wall follower service with true or false depending on the state

    
    """
    global state_, state_desc_
    global srv_client_wall_follower_, srv_client_go_to_point_
    state_ = state
    log = "state changed: %s" % state_desc_[state]
    rospy.loginfo(log)
    if state_ == 0:
        resp = srv_client_go_to_point_(True)
        resp = srv_client_wall_follower_(False)
    if state_ == 1:
        resp = srv_client_go_to_point_(False)
        resp = srv_client_wall_follower_(True)
    if state_ == 2:
        resp = srv_client_go_to_point_(False)
        resp = srv_client_wall_follower_(False)


def normalize_angle(angle):
    """
 This is the function to normalize an angle to be within [-pi, pi]. 
 It checks if the absolute value of the angle is greater than pi, and if so, it subtracts or adds 2*pi depending on the sign of the angle. 
 It then returns the normalized angle
    
    """
    if(math.fabs(angle) > math.pi):
        angle = angle - (2 * math.pi * angle) / (math.fabs(angle))
    return angle
    
def done():
     """
     This is the function to stop the robot when it reaches its goal or cancels its action.
     It creates a twist message and sets the linear and angular velocities to zero. 
     It then publishes the twist message to the cmd_vel topic
  """
    twist_msg = Twist()
    twist_msg.linear.x = 0
    twist_msg.angular.z = 0
    pub.publish(twist_msg)
    
    
def planning(goal):
     """
    This is the function to implement the planning algorithm using bug0 and ROS actions. 
    It takes a goal as an argument and changes the state of the robot accordingly. 
    It also publishes feedback and result messages to the action server. 
    It checks if the robot has reached the goal, encountered an obstacle, or received a preemption request. 
    It uses the go to point and wall follower services to control the robot's motion.
  """
    global regions_, position_, desired_position_, state_, yaw_, yaw_error_allowed_
    global srv_client_go_to_point_, srv_client_wall_follower_, act_s, pose_
    change_state(0)
    rate = rospy.Rate(20)
    success = True
    
    desired_position_.x = goal.target_pose.pose.position.x
    desired_position_.y = goal.target_pose.pose.position.y
    rospy.set_param('des_pos_x', desired_position_.x)
    rospy.set_param('des_pos_y', desired_position_.y)
    
    
    feedback = assignment_2_2022.msg.PlanningFeedback()
    result = assignment_2_2022.msg.PlanningResult()
    
    while not rospy.is_shutdown():
        err_pos = math.sqrt(pow(desired_position_.y - position_.y, 2) +
                        pow(desired_position_.x - position_.x, 2))
        if act_s.is_preempt_requested():
            rospy.loginfo("Goal was preeempted")
            feedback.stat = "Target cancelled!"
            feedback.actual_pose = pose_
            act_s.publish_feedback(feedback)
            act_s.set_preempted()
            success = False
            change_state(2)
            done()
            break
        elif err_pos < 0.5:
            change_state(2)
            feedback.stat = "Target reached!"
            feedback.actual_pose = pose_
            act_s.publish_feedback(feedback)
            done()
            break       
        elif regions_ == None:
            continue
        
        elif state_ == 0:
            feedback.stat = "State 0: go to point"
            feedback.actual_pose = pose_
            act_s.publish_feedback(feedback)
            if regions_['front'] < 0.2:
                change_state(1)
        elif state_ == 1:
            feedback.stat = "State 1: avoid obstacle"
            feedback.actual_pose = pose_
            act_s.publish_feedback(feedback)
            desired_yaw = math.atan2(
                desired_position_.y - position_.y, desired_position_.x - position_.x)
            err_yaw = normalize_angle(desired_yaw - yaw_)
            if regions_['front'] > 1 and math.fabs(err_yaw) < 0.05:
                change_state(0)
        elif state_== 2:
            break
            
            
        else:
            rospy.logerr('Unknown state!')

        rate.sleep()
    
    if success:
        rospy.loginfo('Goal: Succeeded!')
        act_s.set_succeeded(result)
    
    

def main():
    """
    This is the main function that runs the program. 
    It initializes the ROS node, sets the desired position parameters, creates the subscribers, publisher, service clients and action server.
    It also calls the planning function and sleeps at a rate of 20 Hz
  """
    
    time.sleep(2)
    global regions_, position_, desired_position_, state_, yaw_, yaw_error_allowed_
    global srv_client_go_to_point_, srv_client_wall_follower_, act_s, pub

    rospy.init_node('bug0')
    
    desired_position_.x = 0.0
    desired_position_.y = 1.0
    rospy.set_param('des_pos_x', desired_position_.x)
    rospy.set_param('des_pos_y', desired_position_.y)
    sub_laser = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odom)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    srv_client_go_to_point_ = rospy.ServiceProxy(
        '/go_to_point_switch', SetBool)
    srv_client_wall_follower_ = rospy.ServiceProxy(
        '/wall_follower_switch', SetBool)
    act_s = actionlib.SimpleActionServer('/reaching_goal', assignment_2_2022.msg.PlanningAction, planning, auto_start=False)
    act_s.start()
   
    # initialize going to the point
    

    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        rate.sleep()
    
if __name__ == "__main__":
    main()
