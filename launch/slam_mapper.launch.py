import os
import xacro
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

	use_sim_time = LaunchConfiguration('use_sim_time')
	use_sim_time_arg = DeclareLaunchArgument('use_sim_time', 
											default_value='true', 
											description='Use simulation (Gazebo) clock if true') 

	gazebo = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([FindPackageShare('robovisor'), '/launch', '/gazebo_simulator.launch.py']),
		launch_arguments={'use_sim_time': use_sim_time}.items()
	)

	slam = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([FindPackageShare('slam_toolbox'), '/launch', '/online_async_launch.py']),
		launch_arguments={'use_sim_time': use_sim_time, 'params_file': 'config/mapper_params_online_async.yaml'}.items()
	)

	return LaunchDescription([
		use_sim_time_arg,
		gazebo,
		slam
	])