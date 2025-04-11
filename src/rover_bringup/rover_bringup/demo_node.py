import rclpy
from rclpy.node import Node

from std_msgs.msg import String, Bool
from odrive_can.msg import ControlMessage
from time import sleep
import math

class DemoPublisher(Node):

    def __init__(self):
        super().__init__('demo_publisher')
        
        self.homed = False

        self.create_subscription(Bool, 'homing_done', self.homing_done_callback, 10)

        self.get_logger().info("Demo node started. Waiting for homing to complete...")

        self.front_right_upper_suspension_publisher = self.create_publisher(ControlMessage, '/front_right_upper_suspension_12/control_message', 10) 
        self.front_left_upper_suspension_publisher = self.create_publisher(ControlMessage, '/front_left_upper_suspension_11/control_message', 10) 

        self.middle_right_upper_suspension_publisher = self.create_publisher(ControlMessage, '/middle_right_upper_suspension_14/control_message', 10) 
        self.middle_left_upper_suspension_publisher = self.create_publisher(ControlMessage, '/middle_left_upper_suspension_13/control_message', 10) 

        self.rear_right_upper_suspension_publisher = self.create_publisher(ControlMessage, '/rear_right_upper_suspension_16/control_message', 10) 
        self.rear_left_upper_suspension_publisher = self.create_publisher(ControlMessage, '/rear_left_upper_suspension_15/control_message', 10) 

        self.front_right_steer_publisher = self.create_publisher(ControlMessage, '/front_right_steer_22/control_message', 10) 
        self.front_left_steer_publisher = self.create_publisher(ControlMessage, '/front_left_steer_21/control_message', 10)

        self.middle_right_steer_publisher = self.create_publisher(ControlMessage, '/middle_right_steer_24/control_message', 10) 
        self.middle_left_steer_publisher = self.create_publisher(ControlMessage, '/middle_left_steer_23/control_message', 10)

        self.rear_right_steer_publisher = self.create_publisher(ControlMessage, '/rear_right_steer_26/control_message', 10) 
        self.rear_left_steer_publisher = self.create_publisher(ControlMessage, '/rear_left_steer_25/control_message', 10) 

        self.front_right_drive_publisher_32 = self.create_publisher(ControlMessage, '/front_right_drive_32/control_message', 10) 
        self.front_right_drive_publisher_42 = self.create_publisher(ControlMessage, '/front_right_drive_42/control_message', 10) 

        #self.front_left_drive_publisher_31 = self.create_publisher(ControlMessage, '/front_left_drive_31/control_message', 10) 
        #self.front_left_drive_publisher_41 = self.create_publisher(ControlMessage, '/front_left_drive_41/control_message', 10) 

        #self.middle_right_drive_publisher_34 = self.create_publisher(ControlMessage, '/middle_right_drive_34/control_message', 10) 
        #self.middle_right_drive_publisher_44 = self.create_publisher(ControlMessage, '/middle_right_drive_44/control_message', 10) 

        #self.middle_left_drive_publisher_33 = self.create_publisher(ControlMessage, '/middle_left_drive_33/control_message', 10) 
        #self.middle_left_drive_publisher_43 = self.create_publisher(ControlMessage, '/middle_left_drive_43/control_message', 10) 

        #self.rear_right_drive_publisher_36 = self.create_publisher(ControlMessage, '/rear_right_drive_36/control_message', 10) 
        #self.rear_right_drive_publisher_46 = self.create_publisher(ControlMessage, '/rear_right_drive_46/control_message', 10) 

        #self.rear_left_drive_publisher_35 = self.create_publisher(ControlMessage, '/rear_left_drive_35/control_message', 10) 
        #self.rear_left_drive_publisher_45 = self.create_publisher(ControlMessage, '/rear_left_drive_45/control_message', 10)

        self.timer = self.create_timer(1/10, self.front_right_upper_suspension_callback)
        self.timer = self.create_timer(1/10, self.middle_left_upper_suspension_callback)
        self.timer = self.create_timer(1/10, self.rear_left_upper_suspension_callback)
        self.timer = self.create_timer(1/10, self.front_left_upper_suspension_callback)
        self.timer = self.create_timer(1/10, self.rear_right_upper_suspension_callback)
        self.timer = self.create_timer(1/10, self.middle_right_upper_suspension_callback)

        self.timer = self.create_timer(1/10, self.steer_callback)
        self.timer = self.create_timer(1.0, self.drive_callback)

        self.front_time = 0
        self.steer_time = 0
        self.middle_time = 0
        self.rear_time = 0

    def homing_done_callback(self, msg):
        if msg.data and not self.homed:
            self.get_logger().info("Homing complete signal received. Starting demo...")
            self.homed = True

    def front_right_upper_suspension_callback(self):
        if not self.homed:
            return
        self.front_time += 0.025
        msg=ControlMessage()
        msg.control_mode = 3
        msg.input_mode = 1
        msg.input_pos = 0.05 * math.sin(self.front_time + 0)
        msg.input_vel = 0.0
        msg.input_torque = 0.0
        self.front_right_upper_suspension_publisher.publish(msg)

    def middle_left_upper_suspension_callback(self):
        if not self.homed:
            return
        self.front_time += 0.025
        msg=ControlMessage()
        msg.control_mode = 3
        msg.input_mode = 1
        msg.input_pos = 0.05 * math.sin(self.front_time + math.pi/2)
        msg.input_vel = 0.0
        msg.input_torque = 0.0
        self.middle_left_upper_suspension_publisher.publish(msg)

    def rear_left_upper_suspension_callback(self):
        if not self.homed:
            return
        self.front_time += 0.025
        msg=ControlMessage()
        msg.control_mode = 3
        msg.input_mode = 1
        msg.input_pos = 0.05 * math.sin(self.front_time + math.pi)
        msg.input_vel = 0.0
        msg.input_torque = 0.0
        self.rear_left_upper_suspension_publisher.publish(msg)

    def front_left_upper_suspension_callback(self):
        if not self.homed:
            return
        self.front_time += 0.025
        msg=ControlMessage()
        msg.control_mode = 3
        msg.input_mode = 1
        msg.input_pos = -0.05 * math.sin(self.front_time + 0)
        msg.input_vel = 0.0
        msg.input_torque = 0.0
        self.front_left_upper_suspension_publisher.publish(msg)

    def rear_right_upper_suspension_callback(self):
        if not self.homed:
            return
        self.front_time += 0.025
        msg=ControlMessage()
        msg.control_mode = 3
        msg.input_mode = 1
        msg.input_pos = -0.05 * math.sin(self.front_time + math.pi/2)
        msg.input_vel = 0.0
        msg.input_torque = 0.0
        #self.rear_right_upper_suspension_publisher.publish(msg)

    def middle_right_upper_suspension_callback(self):
        if not self.homed:
            return
        self.front_time += 0.025
        msg=ControlMessage()
        msg.control_mode = 3
        msg.input_mode = 1
        msg.input_pos = -0.05 * math.sin(self.front_time + math.pi)
        msg.input_vel = 0.0
        msg.input_torque = 0.0
        self.middle_right_upper_suspension_publisher.publish(msg)

    def steer_callback(self):
        if not self.homed:
            return
        self.get_logger().info("Sending steer commands")
        self.steer_time += 0.05
        msg=ControlMessage()
        msg.control_mode = 3
        msg.input_mode = 1
        msg.input_pos = 0.1 * math.sin(self.steer_time)
        msg.input_vel = 0.0
        msg.input_torque = 0.0
        self.front_right_steer_publisher.publish(msg)
        self.front_left_steer_publisher.publish(msg)
        self.middle_right_steer_publisher.publish(msg)
        self.middle_left_steer_publisher.publish(msg)
        #self.rear_right_steer_publisher.publish(msg)
        self.rear_left_steer_publisher.publish(msg)
    
    def drive_callback(self):
        if not self.homed:
            return
        msg=ControlMessage()
        msg.control_mode = 1
        msg.input_mode = 1
        msg.input_pos = 0.0
        msg.input_vel = 0.0
        msg.input_torque = 0.0
        self.front_right_drive_publisher_32.publish(msg)
        self.front_right_drive_publisher_42.publish(msg)
    #   self.front_left_drive_publisher_31.publish(msg)
    #   self.front_left_drive_publisher_41.publish(msg)
    #   self.middle_right_drive_publisher_34.publish(msg)
    #   self.middle_right_drive_publisher_44.publish(msg)
    #   self.middle_left_drive_publisher_33.publish(msg)
    #   self.middle_left_drive_publisher_43.publish(msg)
    #   self.rear_right_drive_publisher_36.publish(msg)
    #   self.rear_right_drive_publisher_46.publish(msg)
    #   self.rear_left_drive_publisher_35.publish(msg)
    #   self.rear_left_drive_publisher_45.publish(msg)
    
def main(args=None):
    rclpy.init(args=args)

    demo_publisher = DemoPublisher()

    rclpy.spin(demo_publisher)

    demo_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()