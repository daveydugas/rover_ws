import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32MultiArray, Float32
from odrive_can.msg import ControlMessage

class SendMotorCommands(Node):

    def __init__(self):
        super().__init__('send_motor_commands')

        self.topic_names = [   #add all topic names to a list
            "front_right_upper_susepension_12/control_message",
            "front_left_upper_suspension_11/control_message",
            "front_right_steer_22/control_message",
            "front_left_steer_21/control_message",
            "front_right_drive_32/control_message",
            "front_right_drive_42/control_message",
            "front_left_drive_31/control_message",
            "front_left_drive_41/control_message",
            "middle_right_upper_suspension_14/control_message",
            "middle_left_upper_suspension_13/control_message",
            "middle_right_steer_24/control_message",
            "middle_left_steer_23/control_message",
            "middle_right_drive_34/control_message",
            "middle_right_drive_44/control_message",
            "middle_left_drive_33/control_message",
            "middle_left_drive_43/control_message",
            "rear_right_upper_suspension_16/control_message",
            "rear_left_upper_suspension_15/control_message",
            "rear_right_steer_26/ccontrol_message",
            "rear_left_steer_25/control_message",
            "rear_right_drive_36/control_message",
            "rear_right_drive_46/control_message",
            "rear_left_drive_35/control_message",
            "rear_left_drive_45/control_message",
        ]

        #create a publisher for each topic in the list
        self.publishers = [self.create_publisher(ControlMessage, name, 10) for name in self.topic_names]
        
        #create a subscriber to sarahs topic containing the commands
        self.create_subscription(Float32MultiArray, 'sarahs_topic', self.callback, 10)

    def callback(self, msg): #callback for creating the messages and publishing them
        data = msg.data
        if len(data) != 18: #check to make sure the array is published correctly
            self.get_logger().warn(f"Expected 18 values but got {len(data)}")
            return
        
        for i in range(6):
            index = i * 3 # create this to be able to start index 0 every 3 spaces (you have received 6 subarrays with 3 values in each)
            suspension = data[index]  #first value is suspension torque
            steer = data[index + 1]  #second value is steer position
            drive = data[index + 2] #third value is drive velocity

            #create control messages for each value in the array
            msg_suspension = ControlMessage(control_mode=1, input_mode=1, input_pos=0.0, input_vel=0.0, input_torque=suspension) #control_mode 1 for torque
            msg_steer = ControlMessage(control_mode=3, input_mode=1, input_pos=steer, input_vel=0.0, input_torque=0.0,) #control mode 3 for position
            msg_drive = ControlMessage(control_mode=2, input_mode=1, input_pos=0.0, input_vel=drive, input_torque=0.0) #control mode 2 for velcity

            #publish each value to the i-th topic in the topic_names array
            self.publishers[i * 4 + 0].publish(msg_suspension)
            self.publishers[i * 4 + 1].publish(msg_steer)
            self.publishers[i * 4 + 2].publish(msg_drive)
            self.publishers[i * 4 + 3].publish(msg_drive)

def main(args=None):
    rclpy.init(args=args)

    send_motor_commands = SendMotorCommands()

    rclpy.spin(send_motor_commands)

    send_motor_commands.destroy_node()

    rclpy.shutdown()