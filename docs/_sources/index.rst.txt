.. Rt1_assignment2_documentation documentation master file, created by
   sphinx-quickstart on Sun May 28 12:20:18 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Welcome to Rt1_assignment2_documentation's documentation!
=========================================================
On this repository, I have the privilege to share with you my modest response to the Research Track's second assignment, wherein we are tasked to build a package for a robot simulation in Gazebo and Rviz. Therefore, I did create a new ROS package, for which we will develop 3 nodes to perform specific tasks as follows:

    1-An action client node that permits the user to set or cancel a target (x, y) and also publishes the robot's position and velocity as a custom message (x, y, vel x, vel y), by using the values published on the subject /odom.

    2-A service node that when we activate, it will print the number of target reached and cancelled.

    3-A node for printing both the distance that separates the robot from the target and its average speed. In addition, It subscribes to the robot’s position and speed, this will be through using a custom message. A parameter will be used to set the frequency of publishing the data.

    4-In order to run all the simulation together, a launch file was created for this purpose. Set the value for the frequency of the information published by node 3


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Rt1_2nd_Assignment_Documentation
**********************************
This the documentation for assignment 2 rt1

action_user.py
=================
.. automodule:: scripts.action_user
	:members:

bug_as.py
=================
.. automodule:: scripts.bug_as
	:members:

goal_service.py
=================
.. automodule:: scripts.goal_service
	:members:

print_dis_avgvel.py
=====================
.. automodule:: scripts.print_dis_avgvel
	:members:
	
wall_follow_service.py
==========================
.. automodule:: scripts.wall_follow_service
	:members:


