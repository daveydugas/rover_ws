import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32MultiArray, Float32

class SendMotorCommands(Node):

    def __init__(self):
        super().__init__('send_motor_commands')
        self.subscriber_ = self.create_subscription(Float32MultiArray, '/sarahs_topic', self.listener_callback,
        10)
        
        self.front_left_suspension_11_publisher_ = self.create_publisher(Float32, 'drive_topic', 10)
        self.timer = self.create_timer(1.0, self.publish_data)

        self.subscriber_

    def listener_callback(self, msg):
        data = msg.data

        for i in range(54):
            value = msg.data[i]
            


    def publish_data(self):
        pass


def main(args=None):
    rclpy.init(args=args)

    send_motor_commands = SendMotorCommands()

    rclpy.spin(send_motor_commands)

    send_motor_commands.destroy_node()

    rclpy.shutdown()