from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration, FindExecutable
from ament_index_python.packages import get_package_share_path
from launch.actions import IncludeLaunchDescription
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument, LogInfo
from ament_index_python.packages import get_package_share_directory
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

    foxglove_launch = IncludeLaunchDescription(
        XMLLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('foxglove_bridge'),
                'launch',
                'foxglove_bridge_launch.xml'
            )
        )
    )

    #service call for putting odrive in closed loop control
    service_call_node = Node(
        package='rover_bringup',
        executable='send_service_call',
        name='service_call_node'
    )

    #odrive nodes for front right leg
    #odrive can node front_right_upper_suspension_12
    odrive_can_node_suspension_12 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='suspension_12_node',
        namespace='front_right_upper_suspension_12', #potential problem!!!!!
        parameters=[{
            'node_id': 12,
            'interface': 'can1'}]
    )

    #odrive can node front_right_steer_22
    odrive_can_node_steer_22 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='steer_22_node',
        namespace='front_right_steer_22',
        parameters=[{
            'node_id': 22,
            'interface': 'can0'}]
    )

    #odrive can node front_right_drive_32
    odrive_can_node_drive_32 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='drive_32_node',
        namespace='front_right_drive_32',
        parameters=[{
            'node_id': 32,
            'interface': 'can0'}]
    )

    #odrive can node front_right_drive_42
    odrive_can_node_drive_42 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='drive_42_node',
        namespace='front_right_drive_42',
        parameters=[{
            'node_id': 42,
            'interface': 'can0'}]
    )

    #odrive joint states for front right leg
    #publish joint states from odrive to /joint_states topic
    odrive_joint_state_publisher_suspension_12= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='suspension_12_joint_publisher',
            parameters=[{
                'odrive_topic': '/front_right_upper_suspension_12/controller_status',
                'joint_name': 'front_right_upper_suspension_joint'
            }]
    )

    #publish joint states from odrive to /joint_states topic
    odrive_joint_state_publisher_steer_22= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='steer_22_joint_publisher',
            parameters=[{
                'odrive_topic': "/front_right_steer_22/controller_status",
                'joint_name': 'front_right_steer_joint'
            }]
    )

    odrive_joint_state_publisher_drive_32= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='drive_32_joint_publisher',
            parameters=[{
                'odrive_topic': "/front_right_drive_32/controller_status",
                'joint_name': 'front_right_drive_joint'
            }]
    )    

    odrive_joint_state_publisher_drive_42= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='drive_42_joint_publisher',
            parameters=[{
                'odrive_topic': "/front_right_drive_42/controller_status",
                'joint_name': 'front_right_drive_joint'
            }]
    )

    #odrive nodes for front left leg
    #odrive can node front_right_upper_suspension_11
    odrive_can_node_suspension_11 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='suspension_11_node',
        namespace='front_left_upper_suspension_11',
        parameters=[{
            'node_id': 11,
            'interface': 'can1'}]
    )

    #odrive can node front_left_steer_21
    odrive_can_node_steer_21 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='steer_21_node',
        namespace='front_left_steer_21',
        parameters=[{
            'node_id': 21,
            'interface': 'can0'}]
    )

    #odrive can node front_left_drive_31
    odrive_can_node_drive_31 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='drive_31_node',
        namespace='front_left_drive_31',
        parameters=[{
            'node_id': 31,
            'interface': 'can0'}]
    )

    #odrive can node front_left_drive_41
    odrive_can_node_drive_41 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='drive_41_node',
        namespace='front_left_drive_41',
        parameters=[{
            'node_id': 41,
            'interface': 'can0'}]
    )

    #odrive joint states for front left leg
    #publish joint states from odrive to /joint_states topic
    odrive_joint_state_publisher_suspension_11= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='suspension_11_joint_publisher',
            parameters=[{
                'odrive_topic': '/front_left_upper_suspension_11/controller_status',
                'joint_name': 'front_left_upper_suspension_joint'
            }]
    )

    #publish joint states from odrive to /joint_states topic
    odrive_joint_state_publisher_steer_21= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='steer_21_joint_publisher',
            parameters=[{
                'odrive_topic': "/front_left_steer_21/controller_status",
                'joint_name': 'front_left_steer_joint'
            }]
    )

    odrive_joint_state_publisher_drive_31= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='drive_31_joint_publisher',
            parameters=[{
                'odrive_topic': "/front_left_drive_31/controller_status",
                'joint_name': 'front_left_drive_joint'
            }]
    )    

    odrive_joint_state_publisher_drive_41= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='drive_41_joint_publisher',
            parameters=[{
                'odrive_topic': "/front_left_drive_41/controller_status",
                'joint_name': 'front_left_drive_joint'
            }]
    )

    #odrive nodes for middle right leg
    #odrive can node middle_right_upper_suspension_14
    odrive_can_node_suspension_14 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='suspension_14_node',
        namespace='middle_right_upper_suspension_14',
        parameters=[{
            'node_id': 14,
            'interface': 'can1'}]
    )

    #odrive can node middle_right_steer_22
    odrive_can_node_steer_24 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='steer_24_node',
        namespace='middle_right_steer_24',
        parameters=[{
            'node_id': 24,
            'interface': 'can0'}]
    )

    #odrive can node middle_right_drive_34
    odrive_can_node_drive_34 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='drive_34_node',
        namespace='middle_right_drive_34',
        parameters=[{
            'node_id': 34,
            'interface': 'can0'}]
    )

    #odrive can node middle_right_drive_44
    odrive_can_node_drive_44 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='drive_44_node',
        namespace='middle_right_drive_44',
        parameters=[{
            'node_id': 44,
            'interface': 'can0'}]
    )

    #odrive joint states for middle right leg
    #publish joint states from odrive to /joint_states topic
    odrive_joint_state_publisher_suspension_14= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='suspension_14_joint_publisher',
            parameters=[{
                'odrive_topic': '/middle_right_upper_suspension_14/controller_status',
                'joint_name': 'middle_right_upper_suspension_joint'
            }]
    )

    #publish joint states from odrive to /joint_states topic
    odrive_joint_state_publisher_steer_24= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='steer_24_joint_publisher',
            parameters=[{
                'odrive_topic': "/middle_right_steer_24/controller_status",
                'joint_name': 'middle_right_steer_joint'
            }]
    )

    odrive_joint_state_publisher_drive_34= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='drive_34_joint_publisher',
            parameters=[{
                'odrive_topic': "/middle_right_drive_34/controller_status",
                'joint_name': 'middle_right_drive_joint'
            }]
    )    

    odrive_joint_state_publisher_drive_44= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='drive_44_joint_publisher',
            parameters=[{
                'odrive_topic': "/middle_right_drive_44/controller_status",
                'joint_name': 'front_right_drive_joint'
            }]
    )

    #odrive nodes for middle left leg
    #odrive can node middle_left_upper_suspension_13
    odrive_can_node_suspension_13 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='suspension_13_node',
        namespace='middle_left_upper_suspension_13',
        parameters=[{
            'node_id': 13,
            'interface': 'can1'}]
    )

    #odrive can node middle_left_steer_23
    odrive_can_node_steer_23 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='steer_23_node',
        namespace='middle_left_steer_23',
        parameters=[{
            'node_id': 23,
            'interface': 'can0'}]
    )

    #odrive can node middle_left_drive_33
    odrive_can_node_drive_33 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='drive_33_node',
        namespace='middle_left_drive_33',
        parameters=[{
            'node_id': 33,
            'interface': 'can0'}]
    )

    #odrive can node middle_left_drive_43
    odrive_can_node_drive_43 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='drive_43_node',
        namespace='middle_left_drive_43',
        parameters=[{
            'node_id': 43,
            'interface': 'can0'}]
    )

    #odrive joint states for middle left leg
    #publish joint states from odrive to /joint_states topic
    odrive_joint_state_publisher_suspension_13= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='suspension_13_joint_publisher',
            parameters=[{
                'odrive_topic': '/middle_left_upper_suspension_13/controller_status',
                'joint_name': 'middle_left_upper_suspension_joint'
            }]
    )

    #publish joint states from odrive to /joint_states topic
    odrive_joint_state_publisher_steer_23= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='steer_23_joint_publisher',
            parameters=[{
                'odrive_topic': "/middle_left_steer_23/controller_status",
                'joint_name': 'middle_left_steer_joint'
            }]
    )

    odrive_joint_state_publisher_drive_33= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='drive_33_joint_publisher',
            parameters=[{
                'odrive_topic': "/middle_left_drive_33/controller_status",
                'joint_name': 'middle_left_drive_joint'
            }]
    )    

    odrive_joint_state_publisher_drive_43= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='drive_43_joint_publisher',
            parameters=[{
                'odrive_topic': "/middle_left_drive_43/controller_status",
                'joint_name': 'middle_left_drive_joint'
            }]
    )

    #odrive nodes for rear left leg
    #odrive can node rear_left_upper_suspension_15
    odrive_can_node_suspension_15 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='suspension_15_node',
        namespace='rear_left_upper_suspension_15',
        parameters=[{
            'node_id': 15,
            'interface': 'can1'}]
    )

    #odrive can node rear_left_steer_25
    odrive_can_node_steer_25 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='steer_25_node',
        namespace='rear_left_steer_25',
        parameters=[{
            'node_id': 25,
            'interface': 'can0'}]
    )

    #odrive can node rear_left_drive_35
    odrive_can_node_drive_35 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='drive_35_node',
        namespace='rear_left_drive_35',
        parameters=[{
            'node_id': 35,
            'interface': 'can0'}]
    )

    #odrive can node rear_left_drive_45
    odrive_can_node_drive_45 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='drive_45_node',
        namespace='rear_left_drive_45',
        parameters=[{
            'node_id': 45,
            'interface': 'can0'}]
    )

    #odrive joint states for rear left leg
    #publish joint states from odrive to /joint_states topic
    odrive_joint_state_publisher_suspension_15= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='suspension_15_joint_publisher',
            parameters=[{
                'odrive_topic': '/rear_left_upper_suspension_15/controller_status',
                'joint_name': 'rear_left_upper_suspension_joint'
            }]
    )

    #publish joint states from odrive to /joint_states topic
    odrive_joint_state_publisher_steer_25= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='steer_25_joint_publisher',
            parameters=[{
                'odrive_topic': "/rear_left_steer_25/controller_status",
                'joint_name': 'rear_left_steer_joint'
            }]
    )

    odrive_joint_state_publisher_drive_35= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='drive_35_joint_publisher',
            parameters=[{
                'odrive_topic': "/rear_left_drive_35/controller_status",
                'joint_name': 'rear_left_drive_joint'
            }]
    )    

    odrive_joint_state_publisher_drive_45= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='drive_45_joint_publisher',
            parameters=[{
                'odrive_topic': "/rear_left_drive_45/controller_status",
                'joint_name': 'rear_left_drive_joint'
            }]
    )

    #odrive nodes for rear right leg
    #odrive can node rear_right_upper_suspension_16
    odrive_can_node_suspension_16 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='suspension_16_node',
        namespace='rear_right_upper_suspension_16',
        parameters=[{
            'node_id': 16,
            'interface': 'can1'}]
    )

    #odrive can node rear_right_steer_26
    odrive_can_node_steer_26 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='steer_26_node',
        namespace='rear_right_steer_26',
        parameters=[{
            'node_id': 26,
            'interface': 'can0'}]
    )

    #odrive can node rear_right_drive_36
    odrive_can_node_drive_36 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='drive_36_node',
        namespace='rear_right_drive_36',
        parameters=[{
            'node_id': 36,
            'interface': 'can0'}]
    )

    #odrive can node rear_right_drive_46
    odrive_can_node_drive_46 = Node(
        package='odrive_can',
        executable='odrive_can_node',
        name='drive_46_node',
        namespace='rear_right_drive_46',
        parameters=[{
            'node_id': 46,
            'interface': 'can0'}]
    )

    #odrive joint states for rear right leg
    #publish joint states from odrive to /joint_states topic
    odrive_joint_state_publisher_suspension_16= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='suspension_16_joint_publisher',
            parameters=[{
                'odrive_topic': '/rear_right_upper_suspension_16/controller_status',
                'joint_name': 'rear_right_upper_suspension_joint'
            }]
    )

    #publish joint states from odrive to /joint_states topic
    odrive_joint_state_publisher_steer_26= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='steer_26_joint_publisher',
            parameters=[{
                'odrive_topic': "/rear_right_steer_26/controller_status",
                'joint_name': 'rear_right_steer_joint'
            }]
    )

    odrive_joint_state_publisher_drive_36= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='drive_36_joint_publisher',
            parameters=[{
                'odrive_topic': "/rear_right_drive_36/controller_status",
                'joint_name': 'rear_right_drive_joint'
            }]
    )    

    odrive_joint_state_publisher_drive_46= Node(
            package='odrive_joint_publisher',
            executable='odrive_joint_publisher',
            name='drive_46_joint_publisher',
            parameters=[{
                'odrive_topic': "/rear_right_drive_46/controller_status",
                'joint_name': 'rear_right_drive_joint'
            }]
    )
    
    #robot state publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        remappings=[],
    )

    #rviz
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz',
    )

    return LaunchDescription([
        # joint_state_publisher_gui_node,
        declare_urdf_path,
        robot_state_publisher_node,
        LogInfo(msg=["Launching with URDF: ", urdf_file]),  # Log the URDF being loaded
        rviz2_node,
        odrive_can_node_steer_22, #front right
        odrive_can_node_suspension_12,
        service_call_node,
        odrive_joint_state_publisher_steer_22,
        odrive_joint_state_publisher_suspension_12,
        odrive_joint_state_publisher_drive_32,
        odrive_joint_state_publisher_drive_42,
        odrive_can_node_drive_42,
        odrive_can_node_drive_32,
        odrive_can_node_steer_21, #front left
        odrive_can_node_suspension_11,
        odrive_joint_state_publisher_steer_21,
        odrive_joint_state_publisher_suspension_11,
        odrive_joint_state_publisher_drive_31,
        odrive_joint_state_publisher_drive_41,
        odrive_can_node_drive_41,
        odrive_can_node_drive_31,
        odrive_can_node_steer_23, #middle left
        odrive_can_node_suspension_13,
        odrive_joint_state_publisher_steer_23,
        odrive_joint_state_publisher_suspension_13,
        odrive_joint_state_publisher_drive_33,
        odrive_joint_state_publisher_drive_43,
        odrive_can_node_drive_43,
        odrive_can_node_drive_33,
        odrive_can_node_steer_24, #middle right
        odrive_can_node_suspension_14,
        odrive_joint_state_publisher_steer_24,
        odrive_joint_state_publisher_suspension_14,
        odrive_joint_state_publisher_drive_34,
        odrive_joint_state_publisher_drive_44,
        odrive_can_node_drive_44,
        odrive_can_node_drive_34,
        odrive_can_node_steer_25, #rear left
        odrive_can_node_suspension_15,
        odrive_joint_state_publisher_steer_25,
        odrive_joint_state_publisher_suspension_15,
        odrive_joint_state_publisher_drive_35,
        odrive_joint_state_publisher_drive_45,
        odrive_can_node_drive_45,
        odrive_can_node_drive_35,
        odrive_can_node_steer_26, #rear right
        odrive_can_node_suspension_16,
        odrive_joint_state_publisher_steer_26,
        odrive_joint_state_publisher_suspension_16,
        odrive_joint_state_publisher_drive_36,
        odrive_joint_state_publisher_drive_46,
        odrive_can_node_drive_46,
        odrive_can_node_drive_36,
        foxglove_launch
    ])
