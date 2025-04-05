import rclpy
from rclpy.node import Node
from time import sleep
from odrive_can.srv import AxisState

class ServiceCaller(Node):
    def __init__(self):
        super().__init__("service_caller")

        joint_names = [
            "front_right_upper_suspension_12",
            "front_left_upper_suspension_11",
            "front_right_steer_22",
            "front_left_steer_21",
            "front_right_drive_32",
            "front_right_drive_42",
            "front_left_drive_31",
            "front_left_drive_41",
            "middle_right_upper_suspension_14",
            "middle_left_upper_suspension_13",
            "middle_right_steer_24",
            "middle_left_steer_23",
            "middle_right_drive_34",
            "middle_right_drive_44",
            "middle_left_drive_33",
            "middle_left_drive_43",
            "rear_right_upper_suspension_16",
            "rear_left_upper_suspension_15",
            "rear_right_steer_26",
            "rear_left_steer_25",
            "rear_right_drive_36",
            "rear_right_drive_46",
            "rear_left_drive_35",
            "rear_left_drive_45",
        ]

        self.service_clients = {}
        self.service_futures = {}

        for name in joint_names:
            topic = f"/{name}/request_axis_state"
            client = self.create_client(AxisState, topic)
            self.service_clients[name] = client

        self.get_logger().info("Waiting for all services...")

        for name, client in self.service_clients.items():
            if not client.wait_for_service(timeout_sec=5.0):
                self.get_logger().error(f"Service for {name} not available!")
                continue

            request = AxisState.Request()
            request.axis_requested_state = 8

            future = client.call_async(request)
            self.service_futures[name] = future
            future.add_done_callback(lambda fut, n=name: self.response_callback(n, fut))

    def response_callback(self, name, future):
        try:
            response = future.result()
            self.get_logger().info(f"[{name}] Service call successful: {response}")
        except Exception as e:
            self.get_logger().error(f"[{name}] Service call failed: {e}")
    
def main():
    rclpy.init()
    node = ServiceCaller()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()