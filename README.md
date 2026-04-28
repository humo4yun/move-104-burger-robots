# Move 104 Burger Robots 🤖🐢

### Concept: Fleet Coordination & Precise Trajectory Generation in Gazebo

This project focuses on the autonomous control of TurtleBot3 Burger robots (Unit 104 series) to perform complex path planning. The primary objective is to coordinate the robots' movement to visualize specific numeric sequences through high-precision kinematic control.

---

### 🚀 Key Highlights:
* **Multi-Robot Simulation:** Configured and managed the movement of Unit 104 robots within the **Gazebo** physics engine.
* **Digit Visualization ("205"):** Implemented an algorithm to map coordinate waypoints, enabling the robots to "draw" the number **205** with high accuracy.
* **Kinematic Control:** Developed proportional controllers (P-controllers) to manage linear and angular velocities via ROS `cmd_vel` topics.

---

### 🛠 Technical Stack:
* **Framework:** ROS (Noetic/Galactic)
* **Simulator:** Gazebo
* **Robot Model:** TurtleBot3 Burger
* **Language:** Python
* **Key Libraries:** `geometry_msgs`, `nav_msgs`, `rospy`

---

### 📦 How to Use:
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/humo4yun/move-104-burger-robots.git](https://github.com/humo4yun/move-104-burger-robots.git)
   Launch the Gazebo world:
roslaunch move-104-burger-robots world.launch 
   Run the movement script:
python3 move_robot_205.py
