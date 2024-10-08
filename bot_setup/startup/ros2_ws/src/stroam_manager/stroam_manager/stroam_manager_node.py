#!/usr/binenv python3

import rclpy 
from rclpy.node import Node
from lifecycle_msgs.srv import ChangeState
from lifecycle_msgs.msg import Transition
from stroam_interfaces.action import MotorsInstruct, TurretInstruct
from stroam_interfaces.msg import XboxController
from rclpy.action import ActionClient


class StroamNodeManager(Node):
    """
    Represents a node manager for Stroam: turret, 
    motor controller, and camera nodes.

    Attributes:
        turret_client_: Represents an action client for turret node 
        motors_client_: Represents an action client for motor controller node
        camera_client_: Represents a service client for lifecycle camera node 
        controller_client_: Represensts a subscriber for Xbox360 contr inputs
    """

    def __init__(self):

        super().__init__("stroam_manager")
        
        turret_topic_name = "/turret_actions"
        motors_topic_name = "/motor_controller_actions"
        camera_srv_change_state_name = "/camera/change_state"

        self.motors_client_ = self.ActionClient(self, MotorsInstruct,
                 motors_topic_name)
        self.controller_client_ = self.create_subscription(XboxController,
                "/xbox_controller", handle_controller_messages, 10)
        self.camera_client_ = self.create_client(ChangeState, 
                camera_srv_change_state_name)

        self.get_logger().info("Stroam manager started")


    def handle_controller_messages(self, msg: XboxController):
        """
        Handles Xbox360 controller messages.

        Controller inputs meaning:
                x       <--- fire turret
                b       <--- toggle laser
                mode    <--- if true then in drive mode else in turret mode
        Args:
                msg (XboxController): Contains controller inputs.
        """

        if msg.mode:
                send_motors_goal(msg)
        else:
                send_turret_goal(msg)

    def send_motors_goal(self, msg: XboxController):
        """
        Send joy-stick inputs to motor controller action server.
        Utility func. for handle_controller_messages.

        Args:
                msg (XboxController): Contains controller inputs.
        """

        #Create motors goal
        motors_goal = MotorsInstruct.Goal()
        motors_goal.motors_enabled = True
        motors_goal.left_joy_stick_y = msg.left_joy_y
        motors_goal.right_joy_stick_y = msg.right_joy_y

        self.motors_client_.send_goal_async(motors_goal)

    def send_turret_goal(self, msg: XboxController):
        """
        Send button and right joy-stick values to turret action server node.

        Args:
                msg (XboxController): Contains controller inputs.
        """

        pass


def main(args=None):
    rclpy.init(args=args)
    manager_node = StroamNodeManager()
    rclpy.spin(manager_node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()


