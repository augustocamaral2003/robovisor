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

	# default world
	world = LaunchConfiguration('world')
	default_world = os.path.join(get_package_share_directory('robovisor'), 'worlds', 'barrier.world')
	declare_world = DeclareLaunchArgument('world', default_value=default_world, description='Gazebo world file')

	rviz_robot = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([FindPackageShare('robovisor'), '/launch', '/robovisor_state_pub.launch.py']),
		launch_arguments={'use_sim_time': 'true'}.items()
	)

	gazebo = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([FindPackageShare('gazebo_ros'), '/launch', '/gazebo.launch.py']),
		launch_arguments={'use_sim_time': 'true'}.items()
	)

	spawn_entity = Node(
		package='gazebo_ros',
		executable='spawn_entity.py',
		arguments=['-topic', 'robot_description', '-entity', 'robovisor', '-z', '0.5'],
		output='screen'
	)

	return LaunchDescription([
		declare_world,
		rviz_robot,
		gazebo,
		spawn_entity
	])