import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool, String
from odrive_can.msg import ControllerStatus, ControlMessage
from time import sleep

class TakeRoverHome(Node):

    def __init__(self):
        super().__init__('take_rover_home')
        self.homing_complete = False

        #create publisher to publish a boolean to 'homing_done' topic once the procedure is finished
        self.homing_done_pub = self.create_publisher(Bool, 'homing_done', 10)

        #create a timer that checks if homing is done every 0.1 seconds
        self.wait_timer = self.create_timer(0.1, self.check_homing_done, callback_group=None)

        #add all topic names to a list
        self.joint_names = [ 
            "front_right_upper_suspension_12",
            "front_left_upper_suspension_11",
            "front_right_steer_22",
            "front_left_steer_21",
            "middle_right_upper_suspension_14",
            "middle_left_upper_suspension_13",
            "middle_right_steer_24",
            "middle_left_steer_23",
            "rear_right_upper_suspension_16",
            "rear_left_upper_suspension_15",
            "rear_right_steer_26",
            "rear_left_steer_25",
        ]

        #build topic names with for loops
        self.status_topics = [name + "/controller_status" for name in self.joint_names]
        self.command_topics = [name + "/control_message" for name in self.joint_names]

        #use a dictionary to store publishers
        self.publishers_ = {
            name: self.create_publisher(ControlMessage, topic, 10)
            for name, topic in zip(self.joint_names, self.command_topics)
        }

        #use a dictionary to store latest pos_estimate from each joint
        self.current_positions = {}

        #set up subscribers, go to the make_status_callback to gather pos_estimates
        for name, topic in zip(self.joint_names, self.status_topics):
            self.create_subscription(ControllerStatus, topic, self.make_status_callback(name), 10)
        
        #start homing procedure every 5 seconds
        self.homing_timer = self.create_timer(5.0, self.start_homing)

    # def joint_state_callback(self, msg):
    #     name = msg.name
    #     position = msg.position

    #     self.current_positions[name] = position
    #     self.get_logger().info(f"Updated position for joint: {name}")

    #callback to store current positions associated with each joint
    def make_status_callback(self, name):
        def callback(msg):
            self.current_positions[name] = msg.pos_estimate
        return callback

    #conduct homing procedure
    def start_homing(self):
        current_len = len(self.current_positions)
        total_joints = len(self.joint_names)
        self.get_logger().info(f"Received {current_len} / {total_joints} joint positions")
        self.get_logger().info(f"Current joints received: {list(self.current_positions.keys())}")
        sleep(5.0)
        for name in self.joint_names:
            if name not in self.publishers_:
                self.get_logger().warn(f"No publisher found for {name}")

        if len(self.current_positions) < len(self.joint_names):
            self.get_logger().warn("Not all positions received yet, waiting...")
            return  # just wait for next timer tick or let external trigger retry

        self.get_logger().info("Starting to home all joints...")

        steps = 100 #create 100 steps to iterate on
        for i in range(steps + 1):  #iterate from i=0 to i=100 (101 steps)
            for name in self.joint_names:  #iterate through all the joint names in the joint list
                start = self.current_positions[name] #set the starting position of each joint
                current = start * (1 - i / steps)  #mulitply the position by the fraction of how much movement is left

                msg = ControlMessage()
                msg.control_mode = 3
                msg.input_mode = 1
                msg.input_pos = float(current)
                msg.input_vel = 0.0
                msg.input_torque = 0.0

                self.publishers_[name].publish(msg)

            sleep(0.03)

        self.get_logger().info("Homing complete")
        sleep(15.0)
        self.homing_complete = True
        self.homing_timer.cancel()

    #meanwhile this is running every 0.1 seconds and checking if homing_complete changes to True
    def check_homing_done(self):
        if self.homing_complete:
            self.wait_timer.cancel() # when it does change it cancels the timer
            self.publish_homing_done() # calls the publish_homing_done function

    #publish that the homing is done
    def publish_homing_done(self):
        self.get_logger().info("Publishing homing done signal...")
        self.homing_done_pub.publish(Bool(data=True)) #sends boolean true saying that homing is done
            
def main(args=None):
    rclpy.init(args=args)

    take_rover_home = TakeRoverHome()

    rclpy.spin(take_rover_home)

    take_rover_home.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()