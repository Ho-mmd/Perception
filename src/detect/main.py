import rclpy
from rclpy.node import Node
from vision_msgs.msg import Classification2D, ObjectHypothesis
import cv2
from ultralytics import YOLO

class signDetection: 
    def __init__(self, model_path):
        self.model = YOLO(model_path);

    def detectSign(self, image_path):
        sign_id = self.model.names[int(self.model(image_path)[0].boxes.cls)];
        return sign_id;

class signPublisher(Node):
    def __init__(self, detect):
        super().__init__("sign_publisher");
        self.detect = detect;
        self.publisher_ = self.create_publisher(Classification2D, "/perception/sign", 10);
        timer_period = 0.5;
        self.timer = self.create_timer(timer_period, self.sign_info);
        self.get_logger().info("Publish Start");

    def sign_info(self):
        image_path = "/home/detect/testImage/1.jpg";
        sign_id = self.detect.detectSign(image_path);

        msg = Classification2D();
        msg.header.stamp = self.get_clock().now().to_msg();
        msg.header.frame_id = "signs";

        classify = ObjectHypothesis();
        classify.id = sign_id;
        classify.score = 0.7;

        msg.results.append(classify);

        self.publisher_.publish(msg);
        self.get_logger().info(f'Publishing: ID="{sign_id}"');
 
def main(args=None):
    rclpy.init(args=args)

    model_path = "/home/detect/models/bestn.pt";
    detect = signDetection(model_path);

    sign_publisher = signPublisher(detect);

    try:
        rclpy.spin(sign_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        sign_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

