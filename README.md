# Perception

<img src=/images/Architecture_Perception.png alt="Architecture_Perception" width="100%" height="100%"/>

This repository is for the **Perception** part of the [Autonomous-Driving-System](https://github.com/SEA-ME-COSS/Autonomous-Driving-System) project.

-----------------------------------

### Train Dataset

- Gazebo
	- Traffic Light
		- Red (546 images)
		- Yellow (451 images)
		- Green (599 images)
	- RoundAbout (890 images)
	- Crosswalk (926 images)

- Real World
	- Traffic Light
		- Red (360 images)
		- Yellow (30 images)
		- Green (211 images)
	- RoundAbout (350 images)
	- Crosswalk (296 images)
 	- Lane 

------------------------------------

### Labelling

- Tools 
    - https://github.com/HumanSignal/labelImg
    - https://github.com/labelmeai/labelme (For lane detection)

------------------------------------

### Model

- Yolov8
    - https://docs.ultralytics.com/ko
	- https://github.com/ultralytics/ultralytics

------------------------------------

### Usage

- /data/main.py
	- Make raw dataset from rosbag

- /object_detect/objectDetect.py
	- Detect object in Gazebo simulation   	

- /object_detect/real.py
	- Detect object in real world
