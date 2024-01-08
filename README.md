# ADS(Autonomous Driving Systems) Project
## ADS-Perception ( 'Perception' → Planning → Control )
This project will cover the following content.
- LIDAR
- Camera
- GPS (I'm not sure)
- IMU (I'm not sure)  

With ROS2, RViz2, Gazebo, SLAM, Matlab, PyTorch, Yolo ...

## LIDAR code language performance
Laptop_Ubuntu20.04
- py = CPU 1.87%
- cpp = CPU 1.11%

RaspberryPi_Ubuntu20.04
- py = CPU 5.44%
- cpp = CPU 2.51%

maximum rotation speed = 8.3~8.4rps (HW specific)

Manual teleoperation latency  
- pub-sub: 0.03s
- simple SSH: s

```bash
# enable lidar connection
sudo chmod a+rw /dev/ttyUSB0  

# enable inter-machine connection
sudo ufw disable
```
