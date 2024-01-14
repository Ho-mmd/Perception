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
- simple SSH: almost 0s

```bash
# enable lidar connection
sudo chmod a+rw /dev/ttyUSB0  

# enable inter-machine connection
sudo ufw disable

# enable controller using ssh connection
ssh <?>@<?> -Y
```


https://ros2-industrial-workshop.readthedocs.io/en/latest/_source/navigation/ROS2-Cartographer.html  
https://github.com/ros2/cartographer/tree/foxy