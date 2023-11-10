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

	# Argumentos de lançamento
	world = LaunchConfiguration('world')
	world_arg = DeclareLaunchArgument('world', 
									default_value=os.path.join(get_package_share_directory('robovisor'), 'worlds', 'barrier.world'), 
									description='Gazebo world file')
	
	use_sim_time = LaunchConfiguration('use_sim_time')
	use_sim_time_arg = DeclareLaunchArgument('use_sim_time', 
											default_value='true', 
											description='Use simulation (Gazebo) clock if true')
	
	gazebo_gui = LaunchConfiguration('gazebo_gui')
	gazebo_gui_arg = DeclareLaunchArgument(
		'gazebo_gui',
		default_value='false',
		description='Flag to enable/disable GUI for Gazebo')

	# Launches
	gazebo = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([FindPackageShare('gazebo_ros'), '/launch/gazebo.launch.py']),
		launch_arguments={'use_sim_time': use_sim_time, 'world': world, 'gui': gazebo_gui}.items()
	)

	spawn_entity = Node(
		package='gazebo_ros',
		executable='spawn_entity.py',
		arguments=['-topic', 'robot_description', '-entity', 'robovisor', '-z', '0.5'],
		output='screen'
	)



	return LaunchDescription([
		world_arg,
		use_sim_time_arg,
		gazebo_gui_arg,
		gazebo,
		spawn_entity
	])