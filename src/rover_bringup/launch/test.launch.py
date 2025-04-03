from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration, FindExecutable
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument, LogInfo
import os

def generate_launch_description():
    # Declare launch arguments for flexibility
    declare_urdf_path = DeclareLaunchArgument(
        'urdf_file',
        default_value=os.path.join(get_package_share_directory('rover_description'), 'urdf', 'REV_URDF_FULL.xacro'),
        description='Path to the URDF/XACRO file'
    )

    # Get the URDF file path from the launch argument
    urdf_file = LaunchConfiguration('urdf_file')

    # Robot description (use xacro to process URDF)
    robot_description = ParameterValue(Command([FindExecutable(name='xacro'), ' ', urdf_file]),value_type=str)

    # Robot state publisher node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        remappings=[],
    )

    joint_state_pub_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
    )

    # RViz node (optional: specify config if you have one)
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz',
        arguments=['-d', os.path.join(get_package_share_directory('rover_description'), 'rviz', 'default.rviz')]  # Example config path
    )

    return LaunchDescription([
        declare_urdf_path,  # Declare the launch argument
        LogInfo(msg=["Launching with URDF: ", urdf_file]),  # Log the URDF being loaded
        robot_state_publisher_node,
        rviz2_node,
        joint_state_pub_node
    ])
