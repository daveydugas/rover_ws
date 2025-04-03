import rclpy
from rclpy.node import Node
from time import sleep
from odrive_can.srv import AxisState

class ServiceCaller(Node):
    def __init__(self):
        super().__init__("service_caller")
        self.client = self.create_client(AxisState, "/odrive_axis0/request_axis_state")  #make a client that is hosting this topic

        self.get_logger().info("Waiting for service...")
        if not self.client.wait_for_service(timeout_sec=5.0):  #wait for the service to become available
            self.get_logger().error("Service not available!")
            return
        
        sleep(3)

        request = AxisState.Request()
        request.axis_requested_state = 8  #create variable to put motor controller in closed loop control

        self.future = self.client.call_async(request) #send the request
        self.future.add_done_callback(self.response_callback)  #go to callback to make sure the service call was successful

    def response_callback(self, future):  #determine success or not
        try:
            response = future.result()
            self.get_logger().info(f"Service call successful: {response}")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")

    
def main():
    rclpy.init()
    node = ServiceCaller()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()