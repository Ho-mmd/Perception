import rclpy
from rclpy.node import Node

from example_interfaces.msg import Int8

import pygame


class TeleopPublisher(Node):
    def __init__(self):
        super().__init__('teleop_pub_node')
        self.publisher_1 = self.create_publisher(Int8, 'steering_data', 10)
        self.publisher_2 = self.create_publisher(Int8, 'throttle_data', 10)
        self.timer_ = self.create_timer(0.2, self.callback)  # [s]

        pygame.init()

        self.steering_msg = Int8()
        self.throttle_msg = Int8()

        self.steering_msg.data = 0
        self.throttle_msg.data = 0

        self.publisher_1.publish(self.steering_msg)
        self.publisher_2.publish(self.throttle_msg)

        self.w = False
        self.a = False
        self.s = False
        self.d = False


    def callback(self):
        self.w = keyboard.is_pressed('w')
        self.a = keyboard.is_pressed('a')
        self.s = keyboard.is_pressed('s')
        self.d = keyboard.is_pressed('d')

        if self.a and self.d:
            self.steering_msg.data = 0
        elif self.a:
            self.steering_msg.data = -1
        elif self.d:
            self.steering_msg.data = 1
        else:
            self.steering_msg.data = 0
        
        self.publisher1_.publish(self.steering_msg)
        self.get_logger().info('')

    
    def __del__(self):
        pygame.quit()


def main(args=None):
    rclpy.init(args=args)

    teleop_publisher = TeleopPublisher()

    rclpy.spin(teleop_publisher)

    teleop_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
