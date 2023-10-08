import os
import xacro
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

	gazebo = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([FindPackageShare('robovisor'), '/launch', '/gazebo_simulator.launch.py']),
		launch_arguments={'use_sim_time': 'true'}.items()
	)

	slam = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([FindPackageShare('slam_toolbox'), '/launch', '/online_async_launch.py']),
		launch_arguments={'use_sim_time': 'true', 'params_file': 'config/mapper_params_online_async.yaml'}.items()
	)

	return LaunchDescription([
		gazebo,
		slam
	])