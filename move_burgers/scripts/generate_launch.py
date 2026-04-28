#!/usr/bin/env python3
import os
path = os.path.expanduser('~/catkin_ws/src/hw2_U205/launch/spawn_swarm.launch')
model = "$(find hw2_U205)/urdf/turtlebot3_burger_no_lidar.urdf.xacro"
content = '<launch>\n  <include file="$(find gazebo_ros)/launch/empty_world.launch">\n    <arg name="paused" value="false"/><arg name="use_sim_time" value="true"/><arg name="gui" value="true"/>\n  </include>'
for i in range(1, 105):
    x = -25.0 + (i * 0.48)
    content += f'\n  <group ns="tb3_{i}"><param name="robot_description" command="$(find xacro)/xacro {model}" /><node pkg="gazebo_ros" type="spawn_model" name="s{i}" args="-urdf -model tb3_{i} -x {x:.2f} -y -10.0 -z 0.05 -param robot_description" /></group>'
content += '\n</launch>'
with open(path, 'w') as f: f.write(content)
