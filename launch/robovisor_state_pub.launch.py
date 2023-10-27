import os
import xacro
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

	# Diretórios e arquivos
	robovisor_dir = get_package_share_directory('robovisor')
	xacro_file = os.path.join(robovisor_dir, 'urdf', 'robovisor.urdf.xacro')

	rviz_config_file = LaunchConfiguration('rviz_config_file')
	rviz_config_file_arg = DeclareLaunchArgument('rviz_config_file', 
											default_value=os.path.join(robovisor_dir, 'rviz', 'rsp.rviz'), 
											description='Full path to the RViz config file to use')


	use_sim_time = LaunchConfiguration('use_sim_time')
	use_sim_time_arg = DeclareLaunchArgument('use_sim_time', 
											default_value='true', 
											description='Use simulation (Gazebo) clock if true')

	joint_state_publisher = LaunchConfiguration('joint_state_publisher')
	joint_state_publisher_arg = DeclareLaunchArgument('joint_state_publisher', 
											default_value='false', 
											description='Use joint_state_publisher if true')

	# Processar arquivo xacro para urdf
	doc = xacro.process_file(xacro_file)
	urdf = doc.toxml() # type: ignore

	robot_state_publisher_node = Node(
		package='robot_state_publisher',
		executable='robot_state_publisher',
		output='screen',
		parameters=[{'robot_description': urdf}]
	)

	rviz_node = Node(
		package='rviz2',
		executable='rviz2',
		output='screen',
		parameters=[{'use_sim_time': use_sim_time}],
		arguments=['-d', rviz_config_file]
	)

	joint_state_publisher_node = Node(
		package='joint_state_publisher',
		executable='joint_state_publisher',
		output='screen',
		condition=IfCondition(joint_state_publisher),
		parameters=[{'use_sim_time': use_sim_time}]
	)

	return LaunchDescription([
		use_sim_time_arg,
		rviz_config_file_arg,
		joint_state_publisher_arg,
		robot_state_publisher_node,
		joint_state_publisher_node,
		rviz_node
	])
