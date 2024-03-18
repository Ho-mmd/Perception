FROM nvidia/cuda:12.2.2-base-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y \
 && apt install -y curl gnupg gnupg1 gnupg2 locales python3-pip \
 && pip3 install cmake --upgrade \ 
 && locale-gen en_US en_US.UTF-8 \
 && update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 \
 && export LANG=en_US.UTF-8 \
 && apt install -y vim gedit git software-properties-common \
 && add-apt-repository universe \
 && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
 && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null \
 && apt update && apt upgrade -y \
 && apt install -y ros-foxy-desktop python3-argcomplete ros-dev-tools \
 && curl -sSL http://get.gazebosim.org | sh \
 && apt install -y ros-foxy-gazebo-ros-pkgs \
 && apt install ros-foxy-vision-msgs \
 && echo "source /opt/ros/foxy/setup.bash" >> /root/.bashrc 

CMD ["/bin/bash"]
