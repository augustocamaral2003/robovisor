import os
import xacro
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

	rviz_robot = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([FindPackageShare('robovisor'), '/launch', '/robovisor_state_pub.launch.py']),
		launch_arguments={'use_sim_time': 'true'}.items()
	)

	gazebo = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([FindPackageShare('gazebo_ros'), '/launch', '/gazebo.launch.py'])
	)

	spawn_entity = Node(
		package='gazebo_ros',
		executable='spawn_entity.py',
		arguments=['-topic', 'robot_description', '-entity', 'robovisor'],
		output='screen'
	)

	return LaunchDescription([
		rviz_robot,
		gazebo,
		spawn_entity
	])