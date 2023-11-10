import os
import xacro
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

	# Diretórios e arquivos
	bringup_dir = get_package_share_directory('robovisor')

	# Argumentos de lançamento
	use_sim_time = LaunchConfiguration('use_sim_time')
	use_sim_time_arg = DeclareLaunchArgument('use_sim_time', 
											default_value='true', 
											description='Use simulation (Gazebo) clock if true')
	

	rviz_config_file = LaunchConfiguration('rviz_config_file')
	rviz_config_file_arg = DeclareLaunchArgument('rviz_config_file',
											default_value=os.path.join(bringup_dir, 'rviz', 'slam.rviz'),
											description='Full path to the RVIZ config file to use. Available: nav2, view, slam')

	gazebo_gui = LaunchConfiguration('gazebo_gui')
	gazebo_gui_arg = DeclareLaunchArgument('gazebo_gui',
											default_value='false',
											description='Flag to enable/disable GUI for Gazebo')

	# Launches
	simulation = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([FindPackageShare('robovisor'), '/launch/sim/simulation.launch.py']),
		launch_arguments={'use_sim_time': use_sim_time, 'gazebo_gui': gazebo_gui}.items(),
		condition=IfCondition(simulation)
	)

	publisher = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([FindPackageShare('robovisor'), '/launch/core/publisher.launch.py']),
		launch_arguments={'use_sim_time': use_sim_time, 'rviz_config_file': rviz_config_file}.items()
	)

	slam = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([FindPackageShare('slam_toolbox'), '/launch', '/online_async_launch.py']),
		launch_arguments={'use_sim_time': use_sim_time, 'params_file': 'config/mapper_params_online_async.yaml'}.items()
	)

	return LaunchDescription([
		use_sim_time_arg,
		rviz_config_file_arg,
		simulation_arg,
		gazebo_gui_arg,
		simulation,
		publisher,
		slam
	])