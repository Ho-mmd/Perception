import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

from piracer.vehicles import PiRacerStandard


class TeleopSubscriber(Node):
    def __init__(self):
        super().__init__('receiver_node')
        self.subscription_ = self.create_subscription(Twist, '/piracer/cmd_vel', self.callback, 10)
        self.subscription_  # prevent unused variable warning

        self.piracer = PiRacerStandard()


    def callback(self, control_msg):
        self.piracer.set_steering_percent(control_msg.angular.z * 0.8)
        self.piracer.set_throttle_percent(control_msg.linear.x * 0.5)
        # self.get_logger().info('')


def main(args=None):
    rclpy.init(args=args)

    teleop_subscriber = TeleopSubscriber()

    rclpy.spin(teleop_subscriber)

    teleop_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
