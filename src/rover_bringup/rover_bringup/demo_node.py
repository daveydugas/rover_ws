import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from odrive_can.msg import ControlMessage
from time import sleep

class DemoPublisher(Node):

    def __init__(self):
        super().__init__('demo_publisher')
        
        self.front_right_upper_suspension_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name
        self.front_left_upper_suspension_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name

        self.middle_right_upper_suspension_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name
        self.middle_left_upper_suspension_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name

        self.rear_right_upper_suspension_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name
        self.rear_left_upper_suspenion_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name

        self.front_right_steer_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name
        self.front_leftt_steer_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name
        self.middle_right_steer_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name
        self.middle_left_steer_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name
        self.rear_right_steer_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name
        self.rear_left_steer_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name

        self.front_right_drive_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name
        self.front_leftt_drive_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name
        self.middle_right_drive_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name
        self.middle_left_drive_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name
        self.rear_right_drive_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name
        self.rear_left_drive_publisher = self.create_publisher(ControlMessage, 'topic', 10) #change topic name

        self.create_timer(0.0, self.start_front_timer)
        self.create_timer(1.0, self.start_middle_timer)
        self.create_timer(2.0, self.start_rear_timer)

        self.timer = self.create_timer(1.0, self.steer_callback)
        self.timer = self.create_timer(1.0, self.drive_callback)

        self.toggle_1 = True
        self.toggle_2 = True
        self.toggle_3 = True
        self.toggle_4 = True

    def start_front_timer(self):
        self.front_suspension_timer = self.create_timer(1.0, self.front_suspension_callback)

    def start_middle_timer(self):
        self.middle_suspension_timer = self.create_timer(1.0, self.middle_suspension_callback)

    def start_rear_timer(self):
        self.rear_suspension_timer = self.create_timer(1.0, self.rear_suspension_callback)

    def front_suspension_callback(self):
        msg=ControlMessage()
        msg.control_mode = 2
        msg.input_mode = 1
        msg.input_pos = 0.2 if self.toggle_1 else -0.2  #publish 0.2 if self.toggle is true and -0.2 if self.toggle is false
        msg.input_vel = 0.0
        msg.input_torque = 0.0
        self.front_right_upper_suspension_publisher.publish(msg)
        self.front_left_upper_suspension_publisher.publish(msg)

        self.toggle_1 = not self.toggle_1 #flip state

    def middle_suspension_callback(self):
        msg=ControlMessage()
        msg.control_mode = 2
        msg.input_mode = 1
        msg.input_pos = -0.2 if self.toggle_2 else 0.2  #publish -0.2 if self.toggle is true and 0.2 if self.toggle is false
        msg.input_vel = 0.0
        msg.input_torque = 0.0
        self.middle_right_upper_suspension_publisher.publish(msg)
        self.middle_right_upper_suspension_publisher.publish(msg)

        self.toggle_2 = not self.toggle_2 #flip state
    
    def rear_suspension_callback(self):
        msg=ControlMessage()
        msg.control_mode = 2
        msg.input_mode = 1
        msg.input_pos = 0.2 if self.toggle_3 else -0.2
        msg.input_vel = 0.0
        msg.input_torque = 0.0
        self.rear_right_upper_suspension_publisher.publish(msg)
        self.rear_left_upper_suspenion_publisher.publish(msg)

        self.toggle_3 = not self.toggle_3

    def steer_callback(self):
        msg=ControlMessage()
        msg.control_mode = 2
        msg.input_mode = 1
        msg.input_pos = 0.2 if self.toggle_4 else -0.2
        msg.input_vel = 0.0
        msg.input_torque = 0.0
        self.front_right_steer_publisher.publish(msg)
        self.front_leftt_steer_publisher.publish(msg)
        self.middle_right_steer_publisher.publish(msg)
        self.middle_left_steer_publisher.publish(msg)
        self.rear_right_steer_publisher.publish(msg)
        self.rear_left_steer_publisher.publish(msg)

        self.toggle_4 = not self.toggle_4
    
    def drive_callback(self):
        msg=ControlMessage()
        msg.control_mode = 2
        msg.input_mode = 1
        msg.input_pos = 0.0
        msg.input_vel = 0.1
        msg.input_torque = 0.0
        self.front_right_drive_publisher.publish(msg)
        self.front_leftt_drive_publisher.publish(msg)
        self.middle_right_drive_publisher.publish(msg)
        self.middle_left_drive_publisher.publish(msg)
        self.rear_right_drive_publisher.publish(msg)
        self.rear_left_drive_publisher.publish(msg)
    
def main(args=None):
    rclpy.init(args=args)

    demo_publisher = DemoPublisher()

    rclpy.spin(demo_publisher)

    demo_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()