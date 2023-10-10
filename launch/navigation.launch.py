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

	map_file = LaunchConfiguration('map')
	map_file_arg = DeclareLaunchArgument(
		'map',
		default_value=os.path.join(bringup_dir, 'maps', 'barrier.yaml'),
		description='Full path to map file to load')
	
	use_sim_time = LaunchConfiguration('use_sim_time')
	sim_time_arg = DeclareLaunchArgument(
		'use_sim_time',
		default_value='true',
		description='Use simulation (Gazebo) clock if true')
	
	params_file = LaunchConfiguration('params_file')
	params_file_arg = DeclareLaunchArgument(
		'params_file',
		default_value=os.path.join(bringup_dir, 'config', 'nav2_params.yaml'),
		description='Full path to the ROS2 parameters file to use for all launched nodes')
	
	slam_params_file = LaunchConfiguration('slam_params_file')
	slam_params_file_arg = DeclareLaunchArgument(
		'slam_params_file',
		default_value=os.path.join(bringup_dir, 'config', 'localization_params.yaml'),
		description='Full path to the ROS2 parameters file to use for all launched nodes')
	
	rviz_config_file = LaunchConfiguration('rviz_config_file')
	rviz_config_file_arg = DeclareLaunchArgument(
		'rviz_config_file',
		default_value=os.path.join(bringup_dir, 'rviz', 'nav2.rviz'),
		description='Full path to the RVIZ config file to use')
	
	gazebo_gui = LaunchConfiguration('gui')
	gazebo_gui_arg = DeclareLaunchArgument(
		'gui',
		default_value='false',
		description='Flag to enable/disable GUI for Gazebo')
	
	slam = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([FindPackageShare('slam_toolbox'), '/launch', '/online_async_launch.py']),
		launch_arguments={'use_sim_time': use_sim_time, 'slam_params_file': slam_params_file}.items()   
	)

	gazebo = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([FindPackageShare('robovisor'), '/launch', '/gazebo_simulator.launch.py']),
		launch_arguments={'use_sim_time': use_sim_time, 'gui': gazebo_gui, 'rviz_config_file': rviz_config_file}.items()
	)

	nav2 = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([FindPackageShare('nav2_bringup'), '/launch', '/bringup_launch.py']),
		launch_arguments={'map': map_file, 'use_sim_time': use_sim_time, 'params_file': params_file}.items()
	)

	return LaunchDescription([
		map_file_arg,
		params_file_arg,
		slam_params_file_arg,
		sim_time_arg,
		rviz_config_file_arg,
		gazebo,
		slam,
		nav2
	])