import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import os

num = 0;

class cameraSubscribe(Node):
    def __init__(self):
        super().__init__('camera_sub_node');
        self.subscription = self.create_subscription(
                Image,
                "/piracer/camera_sensor/image_raw",
                self.listener_callback,
                10);
        self.subscription;
        self.get_logger().info("Subscribe Start");
        self.bridge = CvBridge();

    def listener_callback(self, msg):
        global num;
        self.get_logger().info("Received");
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8");
        cv2.imwrite(os.path.join("./images/trafficLight", f'trafficLight_{num}.jpg'), cv_image);
        num += 1;

def main(args=None):
    rclpy.init(args=args);

    camera_sub = cameraSubscribe();

    try:
        rclpy.spin(camera_sub);
    except KeyboardInterrupt:
        pass
    finally:
        camera_sub.destroy_node();
        rclpy.shutdown();

if __name__ == '__main__':
    main();

