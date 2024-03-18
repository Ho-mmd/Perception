cmake_minimum_required(VERSION 3.20)    
project(detect)    

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")    
  add_compile_options(-Wall -Wextra -Wpedantic)    
endif()    
    
set(Torch_DIR "/home/library/libtorch/share/cmake/Torch")    
find_package(Torch REQUIRED)    
    
find_package(ament_cmake REQUIRED)    
find_package(rclcpp REQUIRED)    
find_package(std_msgs REQUIRED)    
    
find_package(cv_bridge REQUIRED)    

find_package(OpenCV REQUIRED)    
    
add_executable(detect main.cpp)    
include_directories(detect ${OpenCV_INCLUDE_DIRS})    
target_link_libraries(detect ${TORCH_LIBRARIES} ${OpenCV_LIBS})
    
ament_target_dependencies(detect rclcpp std_msgs) 

set_property(TARGET detect PROPERTY CXX_STANDARD 17)    

