import rclpy
from rclpy.node import Node

from example_interfaces.msg import Int8

import pygame


class TeleopPublisher(Node):
    def __init__(self):
        super().__init__('controller_node')
        self.publisher_1 = self.create_publisher(Int8, 'steering_data', 10)
        self.publisher_2 = self.create_publisher(Int8, 'throttle_data', 10)
        self.timer_ = self.create_timer(0.1, self.callback)  # [s]

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

        self.pre_steering_data = None
        self.pre_throttle_data = None


    def callback(self):
        if self.a and self.d:
            self.steering_msg.data = 0
        elif self.a:
            self.steering_msg.data = -1
        elif self.d:
            self.steering_msg.data = 1
        else:
            self.steering_msg.data = 0

        if self.w and self.s:
            self.throttle_msg.data = 0
        elif self.w:
            self.throttle_msg.data = 1
        elif self.s:
            self.throttle_msg.data = -1
        else:
            self.throttle_msg.data = 0

        if self.pre_steering_data is None or self.pre_steering_data != self.steering_msg.data:
            self.pre_steering_data = self.steering_msg.data
            self.publisher_1.publish(self.steering_msg)
            # self.get_logger().info('')

        if self.pre_throttle_data is None or self.pre_throttle_data != self.throttle_msg.data:
            self.pre_throttle_data = self.throttle_msg.data
            self.publisher_2.publish(self.throttle_msg)
            # self.get_logger().info('')


def main(args=None):
    pygame.init()

    pygame.display.set_mode((300, 200))
    pygame.display.set_caption("Controller (w, a, s, d)")

    rclpy.init(args=args)

    teleop_publisher = TeleopPublisher()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        teleop_publisher.w = keys[pygame.K_w]
        teleop_publisher.a = keys[pygame.K_a]
        teleop_publisher.s = keys[pygame.K_s]
        teleop_publisher.d = keys[pygame.K_d]

        rclpy.spin_once(teleop_publisher)

    teleop_publisher.destroy_node()
    rclpy.shutdown()

    pygame.quit()


if __name__ == '__main__':
    main()
