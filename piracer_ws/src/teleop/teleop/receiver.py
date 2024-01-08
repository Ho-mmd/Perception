import rclpy
from rclpy.node import Node

from example_interfaces.msg import Int8

from piracer.vehicles import PiRacerStandard


class TeleopSubscriber(Node):
    def __init__(self):
        super().__init__('receiver_node')
        self.subscription_1 = self.create_subscription(Int8, 'steering_data', self.steering_callback, 10)
        self.subscription_2 = self.create_subscription(Int8, 'throttle_data', self.throttle_callback, 10)
        self.subscription_1  # prevent unused variable warning
        self.subscription_2  # prevent unused variable warning

        self.piracer = PiRacerStandard()


    def steering_callback(self, steering_msg):
        self.piracer.set_steering_percent(steering_msg.data * -1.0)
        self.get_logger().info('')


    def throttle_callback(self, throttle_msg):
        self.piracer.set_throttle_percent(throttle_msg.data * 0.3)
        self.get_logger().info('')


def main(args=None):
    rclpy.init(args=args)

    teleop_subscriber = TeleopSubscriber()

    rclpy.spin(teleop_subscriber)

    teleop_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()