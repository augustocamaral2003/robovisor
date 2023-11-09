import os
import xacro
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
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
											default_value=os.path.join(bringup_dir, 'rviz', 'nav2.rviz'),
											description='Full path to the RVIZ config file to use')

	simulation = LaunchConfiguration('simulation')
	simulation_arg = DeclareLaunchArgument('simulation',
											default_value='true',
											description='Use simulation if true')

	# Launches
	gazebo = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([FindPackageShare('robovisor'), '/launch', '/gazebo_simulator.launch.py']),
		launch_arguments={'use_sim_time': use_sim_time, 'rviz_config_file': rviz_config_file}.items()
		condidition=IfCondition(simulation)
	)

	slam = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([FindPackageShare('slam_toolbox'), '/launch', '/online_async_launch.py']),
		launch_arguments={'use_sim_time': use_sim_time, 'params_file': 'config/mapper_params_online_async.yaml'}.items()
	)

	return LaunchDescription([
		use_sim_time_arg,
		rviz_config_file_arg,
		simulation_arg,
		gazebo,
		slam
	])