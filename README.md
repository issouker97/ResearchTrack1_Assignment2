RESEARCH TRACK 1  ASSIGNMENT 2
================================

## Goal Of The Assignment

This assignment involves creating a package for a robot simulation in Gazebo and Rviz. 
The aim of this assignment is to create a new ROS package which we will develope 3 nodes: 

1. A node that implements an action client, allowing the user to **set a target (x, y) or to cancel it**. The node
also **publishes the robot position and velocity** as a custom message (x,y, vel_x, vel_y), by relying on the values
published on the topic /odom.
2. A service node that, when called, prints the number of goals reached and cancelled.
3. A node that subscribes to the robot’s position and velocity (using the custom message) and prints the
**distance of the robot from the target and the robot’s average speed**. Use a parameter to set how fast the
node publishes the information.
4. Also create a **launch file** to start the whole simulation. Set the value for the **frequency** with which node (c) publishes
the information.

<p align="center" width="100%">
    <img width="48%" height="350" src="https://user-images.githubusercontent.com/58879182/213936088-b599162b-4c8a-4728-b4f6-830d56a3db6e.png">
    <img width="48%" height="350" src="https://user-images.githubusercontent.com/58879182/213935894-04b775d8-8a03-4a45-86b4-349905741c48.png">
    
</p>

---------------------------------
## First Node: Action (action_user.py)

The first node of our package creates a publisher "pub" that publishes a custom message "**Posxy_velxy**" on the topic "/posxy_velxy". The custom message contains four fields "**msg_pos_x**", "**msg_pos_y**", "**msg_vel_x**", "**msg_vel_y**" that represent the position and velocity of the robot.

```python
 def publisher(msg):
    global pub
    # get the position information111
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
```
The node also creates a subscriber "sub_from_Odom" that subscribes to the topic "/odom", which publishes the Odometry message. The callback function "publisher" is called every time a message is received on the topic "/odom". This function extracts the position and velocity data from the Odometry message and creates an instance of the custom message. The function then assigns the position and velocity data to the corresponding fields of the custom message and publishes the message on the topic "/posxy_velxy".

<p align="center" width="100%">
    <img width="800" height="250" src="https://user-images.githubusercontent.com/58879182/213940945-5b4c75b8-79c5-45ce-9602-caa3081905f1.png">
</p>



Finally the "action_client()" funtion creates an action client and waits for the action server "/reaching_goal" to start. It enters a while loop that prompts the user to enter the target position or type "c" to cancel the goal. If the user enters "c", the action client cancels the goal and sets the status_goal to false. If the user inputs a target position, the function converts the inputs from strings to floats, creates a goal with the target position and sends it to the action server(Planning.action). It also sets status_goal to true.
It's a simple implementation of action client, it sends a goal to the action server and waits for the result of the goal, it could be an error, a success, or a cancelation. The user can interact with the client, setting a goal or canceling it.

<p align="center" width="100%">
    <img width="60%" src="https://user-images.githubusercontent.com/58879182/213941409-7911d914-4ef2-48ae-b2bb-a1432ce44d4f.png">
</p>

### Flowchart of the action_user.py

<p align="center" width="100%">
    <img width="80%" src="https://user-images.githubusercontent.com/58879182/214115689-40ca2b9f-a117-4484-ab77-335498e31adc.png">
</p>

--------------------------------------------------------------------------------------------------------------------------------------------------
## Second Node: Service (goal_service.py)

The second node creates a ROS service that listens for requests on the "goal_service" topic, and responds with the number of goals reached and cancelled. It also subscribes to the "/reaching_goal/result" topic to receive messages about the status of goals and updates the counters for goals reached and cancelled accordingly. When the service is called, it returns a goal_rcResponse message containing the current values of goal_reached and goal_cancelled.

<p align="center" width="100%">
    <img width="800" height="250" src="https://user-images.githubusercontent.com/58879182/213945125-df4fc75e-a79e-40b6-813d-e3963bbc4f50.png">
</p>

It initializes a ROS node called "goal_service" and creates an instance of the Service class. This creates the service, which listens for requests on the "goal_service" topic, and a subscriber to the "/reaching_goal/result" topic. When a request is received on the "goal_service" topic, the data method is called, which returns a goal_rcResponse message containing the current values of goal_reached and goal_cancelled.

When a message is received on the "/reaching_goal/result" topic, the result_callback method is called. This method examines the status (when robot moving: status = 1, when robot target cancelled: status = 2 and when robot reached the target: status = 3) of the goal, which is contained within the message, and increments the appropriate counter, either goal_cancelled or goal_reached. To check the status "rostopic echo /reaching_goal/status" can be run.

<p align="center" width="100%">
    <img width="32%" src="https://user-images.githubusercontent.com/58879182/213946558-6baa0529-c805-478d-bbfa-5d8cf2a23401.png">
    <img width="32%" src="https://user-images.githubusercontent.com/58879182/213946559-fb0281e6-65eb-4569-b5b9-347fece81313.png">
    <img width="32%" src="https://user-images.githubusercontent.com/58879182/213946570-c6f54c7b-8104-4759-9046-0e861b1b48c9.png">
</p>

----------------------------------------------------------------------------------

## Third Node: Print Distance and Average Velociity (print_dis_avgvel.py)

The third node prints out information about a robot's distace from target and average velocity. The node gets the publish frequency parameter from ROS parameters, which is used to determine how often the information is printed. It also initializes a variable to keep track of the last time the information was printed and creates a subscriber to the '/posxy_velxy' topic, which i  to containining messages of robot's curren x,y positions and x,y velocities.

```python
 def __init__(self):
        # Get the publish frequency parameter
        self.freq = rospy.get_param("frequency")

        # Last time the info was printed
        self.printed = 0

        # Subscriber to the position and velocity topic
        self.sub_pos = rospy.Subscriber("/posxy_velxy", Posxy_velxy, self.posvel_callback)
```
The node first gets the desired position of the robot, and the actual position of the robot from the message received. It then calculates the distance between the desired and actual positions using the math.dist() function. It also gets the actual velocity of the robot from the message and calculates the average speed using the velocity components from the message. Finally, it prints the distance and average speed information using the rospy.loginfo() function, and updates the last printed time variable.

<p align="center" width="100%">
    <img width="60%" src="https://user-images.githubusercontent.com/58879182/213949410-960707c9-6672-490f-96c1-2d3c2618f1cd.png">
</p>


-------------------------------------
## Creating Launch file (assignment2.launch)

The ROS launch file is used to start multiple nodes and set parameters at once. The launch file is written in XML and uses the <launch> tag as the root element.The launch file starts by including another launch file, "sim_w1.launch", which is already located in our package to run Gazebo and Rviz simulators and environment related nodes. Then, it sets two parameters "des_pos_x" and "des_pos_y" with values 0.0 and 1.0 respectively. These parameters used by other nodes to determine the desired position of the robot.

Then we set a parameter "frequency" with a value of 1.0. This parameter used by the node "print_dis_avgvel.py" to determine how often the distance and average velocity information should be printed.

After that, it starts nodes using the <node> tag, these nodes are:

  +  "wall_follower.py"
  +  "go_to_point.py"
  +  "bug_action_service.py"
  +  "action_user.py"
  +  "goal_service.py"
  +  "print_dis_avgvel.py"

Each of these nodes is defined by specifying the package name "assignment_2_2022" where they reside, the type of the file, and the name of the node. The last two nodes are run with the additional parameter output="screen" and launch-prefix="xterm -hold -e" respectively, which causes the output of these nodes to be printed to the screen in a new terminal window.
	

	
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
## Installation

First of all before running the program it is required to install the xterm libray. Open a terminal window and run the following command to install the xterm package, this library helps us to print outputs of the nodes in a new terminal window :

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

## How To Run The Simulation
The launch file for the assignment can be found in the "launch" folder within the "assignment_2_2022" directory. To start the simulation, use the following command: 

```command
	roslaunch assignment_2_2022 assignment2.launch
```
Upon successful launch, four screens should appear: one for inputting target coordinates (action_user.py), one for displaying the distance and average velocity of the robot (print_dis_avgvel.py), and two for the Gazebo and Rviz visualization environments.
	
<p align="center" width="100%">
    <img width="24%" height="200" src="https://user-images.githubusercontent.com/58879182/213941409-7911d914-4ef2-48ae-b2bb-a1432ce44d4f.png">
    <img width="24%" height="200" src="https://user-images.githubusercontent.com/58879182/213949410-960707c9-6672-490f-96c1-2d3c2618f1cd.png">
    <img width="24%" height="200" src="https://user-images.githubusercontent.com/58879182/213936088-b599162b-4c8a-4728-b4f6-830d56a3db6e.png">
    <img width="24%" height="200" src="https://user-images.githubusercontent.com/58879182/213935894-04b775d8-8a03-4a45-86b4-349905741c48.png">	
</p>

To run the service node (goal_service.py) that, when called, prints the number of goals reached and cancelled use the following command:

```command
	rosservice call /gaol_service
```
or just us the rqt tool to call the service. rqt is a tool in ROS (Robot Operating System) that provides a simple and intuitive GUI (graphical user interface) for debugging and analyzing various aspects of the system. It allows users to view various data streams, such as topics, services, and parameters, as well as perform tasks such as plotting, logging, and debugging. rqt also provides a plugin system which allows developers to create custom plugins for specific tasks. It helps to debug, visualize and inspect the ROS system, also to monitor and control the ROS nodes and topics.

```command
	rqt
```
<p align="center" width="100%">
    <img width="800" height="300" src="https://user-images.githubusercontent.com/58879182/214059310-a25e8d3d-29fd-4a1f-927f-9e372578cba3.png">
</p>

To access the Service Caller function in rqt, follow these steps:

    1- Go to the "Plugins" menu
    2- Select "Services"
    3- Click on "Service Caller"
    4- In the Service Caller window, locate the "goal_service"
    5- Click the "Call" button
    6- The response window will display the number of targets reached and cancelled.
	
<p align="center" width="100%">
    <img width="800" height="300" src="https://user-images.githubusercontent.com/58879182/214059302-e17e3cf2-5126-48c3-a3e2-119a81665366.png">
</p>
	
---------------------------------

## Troubleshooting

When running `roslaunch assignment_2_2022 assignment2.launch` file, you may be presented with some errors related to the graphical board of your pc. Try the following steps:

Open the urdf directory and change 43 and 71 lines of the robot2_lazer.gazebo file with the followings:
* line 43: 
	```xml 
	<sensor type="ray" name="head_hokuyo_sensor"> 
	``` 
* change with  
	```xml 
	<sensor type="gpu_ray" name="head_hokuyo_sensor"> 
	```
* line 71: 
	```xml 
	<plugin name="hokuyo_node" filename="libgazebo_ros_laser.so"> 
	``` 
* change with  
	```xml 
	<plugin name="gazebo_ros_head_hokuyo_controller" filename="libgazebo_ros_gpu_laser.so"> 
	```

-----------------------------------
		
## Conclusion

In this assignment, a package was developed with three nodes: (a) an action client node that allows the user to set a target (x, y) or cancel it, and also publishes the robot's position and velocity as a custom message; (b) a service node that prints the number of goals reached and cancelled; and (c) a node that subscribes to the robot's position and velocity and prints the distance of the robot from the target and the robot's average speed. A launch file was also created to start the whole simulation and set the frequency at which node (c) publishes information. Overall, the package demonstrates the use of action clients, services, and custom messages in ROS and how they can be used to control a robot and monitor its performance. Some possible improvements for this assignment could include:

1- Using markers in RViz to display the target position and the robot's current position in a more intuitive way, such as by using different colors or shapes to indicate different states (e.g. goal reached, goal canceled).

2- Incorporating the robot's orientation in the visualization, such as by using an arrow or a 3D model of the robot to indicate the direction it is facing.

3- Using Gazebo's built-in visualization tools to display the target position in the simulated environment, such as by placing a marker or a flag at the target location.

4- Incorporating a path-planning algorithm to display the robot's planned path to the target, such as by using RViz's "Path" display type.

5- Implementing input validation to ensure that the user can only enter integers, and not other types of input such as floating point numbers or characters. Providing feedback to the user if an invalid input is entered, such as by displaying an error message or highlighting the input field in red.

6- Adding a feature to check if the input value is within a certain range or not, and if not, prompt the user to enter a value within the range.
