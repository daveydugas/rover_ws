import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32MultiArray

class DummyPublisher(Node):

    def __init__(self):
        super().__init__('dummy_publisher')

        self.publisher = self.create_publisher(Float32MultiArray, 'sarahs_topic', 10)

        self.timer = self.create_timer(1.0, self.dummy_callback)

    def dummy_callback(self):
        msg=Float32MultiArray()

        matrix = [[0.0,1.0,2.0],
                    [3.0,4.0,5.0],
                    [6.0,7.0,8.0],
                    [9.0,10.0,11.0],
                    [12.0,13.0,14.0],
                    [15.0,16.0,17.0]]

        msg.data = [item for row in matrix for item in row]

        self.publisher.publish(msg)
        self.get_logger().info(f'Published array: {msg.data}')

def main(args=None):
    rclpy.init(args=args)

    dummy_publisher = DummyPublisher()

    rclpy.spin(dummy_publisher)

    dummy_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()