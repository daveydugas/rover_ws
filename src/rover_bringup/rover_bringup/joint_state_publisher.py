import rclpy
from rclpy import Node
from sensor_msgs.msg import JointState
from odrive_can.msg import ControlMessage
import math

class JointStatePublisher(Node):

    def __init__(self):
        super().__init__('joint_state_publisher')

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
            "rear_right_steer_26/control_message",
            "rear_left_steer_25/control_message",
            "rear_right_drive_36/control_message",
            "rear_right_drive_46/control_message",
            "rear_left_drive_35/control_message",
            "rear_left_drive_45/control_message",
        ]
        
        #add all joint names to a list
        self.joint_names = [name.replace("/control_message", "") for name in self.topic_names]

        # Initialize joint state arrays
        self.position_estimates = [0.0] * len(self.joint_names)
        self.velocity_estimates = [0.0] * len(self.joint_names)
        self.effort_estimates = [0.0] * len(self.joint_names)

        #create mapping from topic names to their index in the joint arrays
        self.topic_to_index = {topic: i for i, topic in enumerate(self.topic_names)}

        #subscribe to each odrive messages topic
        self.subscribers = []
        
        for i, topic in enumerate(self.topic_names):
            sub = self.create_subscription(
                ControlMessage, 
                topic, 
                lambda msg, i=1: self.odrive_callback(msg, i),
                10
            )
            self.subscribers.append(sub)
            

        #create a publisher to publish joint states
        self.joint_publisher = self.create_publisher(JointState, '/joint_states', 10)

        #timer to call joint state publisher every 50 Hz
        self.timer = self.create_timer((1/50), self.publish_joint_states)

    def odrive_callback(self, msg, index):
        topic = self.get_current_subscription_topic()
        index = self.topic_to_index[topic]
        #take position element from odrive message (in radians)
        self.position_estimates[index] = msg.input_pos

        #take velocity element from odrive message (in radians/sec)
        self.velocity_estimates[index] = msg.input_vel

        #take effort element direction from torque odrive messgae
        self.effort_estimates[index] = msg.torque_estimate

    def get_current_subscription_topic(self):
        # Use introspection to get the topic from which the current callback was triggered
        return self.get_subscription_topic_name()

    def publish_joint_states(self):
        #Initialize Joint State
        self.joint_state_msg = JointState()
        self.joint_state_msg.header.stamp = self.get_clock().now().to_msg()
        self.joint_state_msg.name = self.joint_names
        self.joint_state_msg.position = self.position_estimates
        self.joint_state_msg.velocity = self.velocity_estimates
        self.joint_state_msg.effort = self.effort_estimates

        self.joint_publisher.publish(self.joint_state_msg)


def main(args=None):
    rclpy.init(args=args)

    joint_state_publihser = JointStatePublisher()

    rclpy.spin(joint_state_publihser)

    joint_state_publihser.destroy_node()

    rclpy.shutdown()