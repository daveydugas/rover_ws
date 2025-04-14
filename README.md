# REV Rover Workspace
This is a development workspace for writing code for the first generation of REV

## Install
```
git clone https://github.com/daveydugas/rover_ws.git
cd rover_ws
colcon build
source install/local_setup.bash
```
## Prepare for launch
Plug in the Steer and Drive Axises to your left most USB port and in any terminal run
```
sudo ip link set can0 up type can bitrate 1000000
```

Plug in the Suspension Axises to your right most USB port and in any terminal run
```
sudo ip link set can1 up type can bitrate 1000000
```

## Launch
To launch the URDF run
```
ros2 launch rover_bringup rover.launch.py
```
You will see then see the URDF show up on RVIZ and the ODrives will all be put into closed loop control
(If you do not want this, comment out the service call node in the launch file)

To launch a demo, open another terminal and run
```
ros2 run rover_bringup demo_node
```
Then, in another terminal run
```
ros2 run rover_bringup take_me_home
```
This will bring all of the joints to zero first and then run a demo movement of all of the joints
