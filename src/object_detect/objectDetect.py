import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from sensor_msgs.msg import Image
from vision_msgs.msg import Classification2D, ObjectHypothesis
import cv2
from cv_bridge import CvBridge
from ultralytics import YOLO

depthQue = [];
rgbQue = [];

class cameraSubscribe(Node):
    def __init__(self, signDetect):
        super().__init__('camera_sub_node');
        self.signDetect = signDetect;
        self.depth = MutuallyExclusiveCallbackGroup();
        self.rgb = MutuallyExclusiveCallbackGroup();
        self.depthQue = [];
        self.rgbQue = [];

        self.subscription1 = self.create_subscription(
            Image,
            '/camera/depth/image_raw',
            self.depthback,
            10,
            callback_group=self.depth
        );

        self.subscription2 = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.rgbback,
            10,
            callback_group=self.rgb
        );

        self.bridge = CvBridge();
        
    def depthback(self, msg):
        self.get_logger().info(f'Depth Image Received');

        depth_image = self.bridge.imgmsg_to_cv2(msg, "32FC1");
        depthQue.append(depth_image);

    def rgbback(self, msg):
        self.get_logger().info(f'Rgb Image Received');

        rgb_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8');
        rgbQue.append(rgb_image);

        if(len(rgbQue) > 0):
            self.signDetect.signInfo(rgbQue);

class signDetect:
    def __init__(self, model_path, signPublish):
        self.signPublish = signPublish;
        self.model = YOLO(model_path);
        self.resultQue = [];

    def signInfo(self, rgbQue):
        rgb_image = rgbQue.pop(0);
        results = self.model(rgb_image);

        for result in results:
            if len(result) > 0:
                self.resultQue.append(result);
            else:
                pass;

        if(len(depthQue) > 0): 
            self.depthInfo(depthQue);


    def depthInfo(self, depthQue):
        depth_image = depthQue.pop(0);

        sign_id = "";
        dist = -1;

        while(len(self.resultQue) > 0):
            tmp = self.resultQue.pop(0);
            
            for tp in tmp:
                box = tp.boxes.xyxy;

                x = int((box[0][0] + box[0][2]) / 2);
                y = int((box[0][1] + box[0][3]) / 2);
                
                if(dist == -1 or depth_image[y, x].item() < dist):
                    dist = depth_image[y, x].item();
                    sign_id = self.model.names[int(tp.boxes.cls)];
        
        if(dist != -1):
            print(sign_id, dist);
            self.signPublish.pub_sign(sign_id, dist);
        else:   
            sign_id = "None";
            self.signPublish.pub_sign(sign_id, dist);

class signPublish(Node):
    def __init__(self):
        super().__init__("sign_pub_node");
        self.publisher_ = self.create_publisher(Classification2D, "/perception/sign", 10);
    
    def pub_sign(self, sign_id, score):
        msg = Classification2D();
        msg.header.stamp = self.get_clock().now().to_msg();
        msg.header.frame_id = "signs";

        classify = ObjectHypothesis();
        classify.id = sign_id;
        classify.score = score;

        msg.results.append(classify);

        self.publisher_.publish(msg);

def main(args=None):
    rclpy.init(args=args);

    model_path = "/home/object_detect/models/bestn.pt";

    sign_pub = signPublish();
    sign_detect = signDetect(model_path, sign_pub);
    node = cameraSubscribe(sign_detect);

    executor = MultiThreadedExecutor();
    executor.add_node(node);

    try:
        executor.spin();
    finally:
        node.destroy_node();
        rclpy.shutdown();

if __name__ == '__main__':
    main();

