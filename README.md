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
### Plug in the Steer and Drive Axises to your left most USB port and in any terminal run
```
sudo ip link set can0 up type can bitrate 1000000
```

### Plug in the Suspension Axises to your right most USB port and in any terminal run
```
sudo ip link set can1 up type can bitrate 1000000
```
