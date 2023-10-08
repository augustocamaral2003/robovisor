import os
import xacro
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    bringup_dir = get_package_share_directory('robovisor')

    map_yaml_file = LaunchConfiguration('map')
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    params_file = LaunchConfiguration('params_file')
    lifecycle_nodes = ['map_server', 'amcl']

    map_arg = DeclareLaunchArgument(
        'map',
        default_value=os.path.join(bringup_dir, 'maps', 'barrier.yaml'),
        description='Full path to map file to load')
    
    sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')
    
    params_file_arg = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(bringup_dir, 'config', 'nav2_params.yaml'),
        description='Full path to the ROS2 parameters file to use for all launched nodes')

    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'yaml_filename': map_yaml_file, 'use_sim_time': use_sim_time}],
        remappings=[('/tf', 'tf')]
    )

    amcl_node = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}, {'node_names': lifecycle_nodes}],
    )

    lifecycle_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}, {'node_names': lifecycle_nodes}],
    )

    return LaunchDescription([
        map_arg,
        sim_time_arg,
        map_server_node,
        amcl_node
    ])