import rclpy    
from rclpy.node import Node    
from sensor_msgs.msg import Image    
from vision_msgs.msg import Classification2D, ObjectHypothesis    
import cv2    
from cv_bridge import CvBridge
import numpy as np    
from ultralytics import YOLO    
    
class cameraSubscriber(Node):    
    def __init__(self, sign_detect):    
        super().__init__('camera_sub_node');    
        self.sign_detect = sign_detect;
        self.subscription = self.create_subscription(    
                Image,    
                'camera_data',    
                self.listener_callback,    
                10);    
        self.subscription;    
        self.bridge = CvBridge();    
    
    def listener_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8');
        
        sign_id, score = self.sign_detect.detectSign(cv_image);
        self.sign_detect.pub_sign(sign_id, score);


class signPublisher(Node):
    def __init__(self):
        super().__init__("sign_publisher");
        self.publisher_ = self.create_publisher(Classification2D, "/perception/sign", 10);
        self.get_logger().info("Publish Start");

    def sign_info(self, sign_id, score):
        msg = Classification2D();
        msg.header.stamp = self.get_clock().now().to_msg();
        msg.header.frame_id = "signs";

        classify = ObjectHypothesis();
        classify.id = sign_id;
        classify.score = score;

        msg.results.append(classify);

        self.publisher_.publish(msg);
        self.get_logger().info(f'Publishing: ID="{sign_id}"');
 
class signDetection: 
    def __init__(self, model_path, publisher):
        self.model = YOLO(model_path);
        self.publisher = publisher;

    def detectSign(self, cv_image):
        sign_id = self.model.names[int(self.model(cv_image)[0].boxes.cls)];
        score = 0.7;

        return sign_id, score;

    def pub_sign(self, sign_id, score):
        self.publisher.sign_info(sign_id, score);

def main(args=None):
    rclpy.init(args=args)

    model_path = "/home/detect/models/bestn.pt";
    
    sign_publisher = signPublisher();
    sign_detect = signDetection(model_path, sign_publisher);
    camera_subscriber = cameraSubscriber(sign_detect);

    try:
        rclpy.spin(camera_subscriber);
    except KeyboardInterrupt:
        pass
    finally:
        camera_subscriber.destroy_node();
        sign_publisher.destroy_node();
        rclpy.shutdown();

if __name__ == '__main__':
    main();

