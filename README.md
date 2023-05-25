Research Track 1 :  Assignment Undertaken Number #2
================================

## Aim of The Assignment

On this repository, I have the privilege to share with you my modest response to the Research Track's second assignment, wherein we are tasked to build a package for a robot simulation in Gazebo and Rviz. Therefore, I did create a new ROS package, for which we will develop 3 nodes to perform specific tasks as follows: 

1. An action client node that permits the user to set or cancel a target (x, y) and also publishes the robot's position and velocity as a custom message  (x, y, vel x, vel y), by using the values published on the subject /odom.

2. A service node that when we activate, it will print the number of target reached and cancelled.
 
3. A node for printing both the distance that separates the robot from the target and its average speed. In addition, It subscribes to the robot’s position and speed, this will be through using a custom message. A parameter will be used to set the frequency of publishing the data. 

4. In order to run all the simulation together, **a launch file** was created for this purpose. Set the value for the **frequency** of the information published by node 3
---------------------------------
## Details About The  First Node: Action (action_user.py)

The first node of our package creates a publisher "pub" that publishes a custom message "**Posxy_velxy**" on the topic "/posxy_velxy". The custom message contains four fields "**msg_pos_x**", "**msg_pos_y**", "**msg_vel_x**", "**msg_vel_y**" that represent the position and velocity of the robot.

In addition, the node creates a subscriber "sub_from_Odom" that subscribes to the topic "/odom", that publishes the Odometry message. Whenever a message is received on the topic "/odom", the callback function "publisher" is called.  This function has a role to : 
-	Generates an instance of the custom message and get both the position and velocity data from the odometry message.
-	Following this,  it assigns the position and velocity data to the corresponding fields of the custom message and publishes the message on the topic "/posxy_velxy"

Last but not least, creating a action client by the "action_client()" function and waiting for the action server "/reaching goal" starting the process. There will be then a while loop run with two choices : 
-	The first choice is to enter the target position, which means if the user inputs the target position, this function changes the inputs from strings to floats, then creates a goal with the target position and sends it to the action server(Planning.action). Moreover, status_goal is set to true. A target is transmitted to the action server using a straightforward action client implementation, and the target's outcome, which may be an error, a success, or a cancelation, is then awaited.
-	On the other hand, cancelling the target with pressing on “c”. in this case, the action client cancels the target and sets the status_goal to false.
--------------------------------------------------------------------------------------------------------------------------------------------------
## Details About The Second Node: Service (goal_service.py)

This node builds a ROS service that has a role to :
- Reply to the questions, of how many attained and cancelled goals,  on the "goal service" topic. 
- Refreshe the counters about the number  of goals attained and cancelled in accordance by subscribing to the topic "/reaching goal/result" and receiving messages to enquire about goal status.
- Each time the service is called, the current values of goal reached/cancelled are returned in a goal rcResponse message.

The result callback method is called whenever a message on the "/reaching goal/result" topic is received. This method looks at the message's goal's status (while the robot is moving, status is 1, when the target is cancelled, status is 2, and when the robot reaches the target, status is 3), and it increases the relevant counter, either goal cancelled or goal reached. Run "rostopic echo /reaching goal/status" to see the current situation.

----------------------------------------------------------------------------------

## Details About The Third Node: Printing both  Distance and Average Velociity (print_dis_avgvel.py)

This node has the role to print out data on a robot's average velocity and distance from the target. The publish frequency parameter, which controls how frequently the information is printed, is obtained by the node from ROS parameters. In addition, it initializes a variable to keep track the recent data printed and creates a subscriber to the '/posxy_velxy' topic, which includes messages of robot's updated (x,y) positions and (x,y) velocities.

There is function called math.dist() function, which is used to calculate the distance between the desired position of the robot and its real-time position that the node gets respectively from the message received. The same thing happens with the average velocity, the node receive the velocity component of both desired and real-time  speed and calculate the average. At the end, printing results, distance and average velocity, will be through using the rosp.loginfo() function and make a refresh to the recent reported time variable.

-------------------------------------
## How To Create Launch File (assignment2.launch)

Running the Launch file makes multiple nodes start at the same time with adjusting parameters. The launch file is written in XML and uses the tag as the root element. The launch file runs by including another launch file, "sim_w1.launch", which is already located in our package to run Gazebo and Rviz simulators and environment related nodes. Afterwards, it sets two parameters "des_pos_x" with values 0.0  and "des_pos_y" with values 1.0. These parameters used by other nodes to determine the desired position of the robot.

In order to set how many times both the distance and average velocity data should be printed, we just need to set the parameter **frequency** used by the node "print_dis_avgvel.py" on 1.0.

After that, it starts nodes using the <node> tag, these nodes are:

  +  "wall_follower.py"
  +  "go_to_point.py"
  +  "bug_action_service.py"
  +  "action_user.py"
  +  "goal_service.py"
  +  "print_dis_avgvel.py"

Each of these nodes is specified by stating the package name "assignment 2 2022" in which it resides, the file type, and the node name. The final two nodes are launched with the extra parameters output="screen" and launch-prefix="xterm -hold -e," which force the output of these nodes to be printed to the screen in a new terminal window.
	

	
```xml
 def __init__(self):
 <?xml version="1.0"?>
<launch>
    <include file="$(find assignment_2_2022)/launch/sim_w1.launch" />
    <param name="des_pos_x" value= "0.0" />
    <param name="des_pos_y" value= "1.0" />
    
    <!--Frequency parameter to set the frequency of the print_dis_avgvel node -->
    <param name="frequency" type="double" value="1.0" />
    
    <node pkg="assignment_2_2022" type="wall_follow_service.py" name="wall_follower" />
    <node pkg="assignment_2_2022" type="go_to_point_service.py" name="go_to_point"  />
    <node pkg="assignment_2_2022" type="bug_as.py" name="bug_action_service" output="screen" />
    <node pkg="assignment_2_2022" type="action_user.py" name="action_user" output="screen" launch-prefix="xterm -hold -e" />
    <node pkg="assignment_2_2022" type="goal_service.py" name="goal_service"  />
    <node pkg="assignment_2_2022" type="print_dis_avgvel.py" name="print_dis_avgvel" output="screen" launch-prefix="xterm -hold -e" />
</launch>
```
This launch file allows to start all the necessary nodes for the application and set the required parameters with a single command, instead of running each node and setting each parameter separately. It also allows to run the nodes in a specific order and with specific settings.
	
------------------------------------
## Installation :

As a first step, It’s preferable to install the xterm library, this will help us to print outputs of the nodes in a new terminal window:

```command
	sudo apt-get install xterm -y
```
Next, navigate to your ROS workspace 'src' folder and clone this repository using the following command:
	
```command
	git clone <link of the repository>
```
Once the repository has been cloned, navigate to the work space drectory and run the following command to build the package:

```command
	catkin_make
```


After the package has been built successfully, finally, we can launch the simulation
	
---------------------------------

## Simulation Time :
The launch file for the assignment can be found in the "launch" folder within the "assignment_2_2022" directory. To start the simulation, use the following command: 

```command
	roslaunch assignment_2_2022 assignment2.launch
```
Upon successful launch, four screens should appear: one for inputting target coordinates (action_user.py), one for displaying the distance and average velocity of the robot (print_dis_avgvel.py), and two for the Gazebo and Rviz visualization environments.
	
To run the service node (goal_service.py) that, when called, prints the number of goals reached and cancelled use the following command:

```command
	rosservice call /gaol_service
```
---------------------------------
		
## Conclusion :

The package shows how to handle with action clients, services, custom messages with ROS and their role to control the behaviour of the robot and its performances

1- Adding something as a signal to attract the eye such as colors to distinguish between the position of the robot in real-time and the target position in RViz.

2- Making an obvious sign, for instance a red flag at the target location would be a good idea in Gazebo environment.

3- Building an algorithm to illustrate the path done by the robot to reach the target and optimize its trajectory.
