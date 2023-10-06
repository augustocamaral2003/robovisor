import os
import xacro
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Diretórios e arquivos
    robovisor_dir = get_package_share_directory('robovisor')
    xacro_file = os.path.join(robovisor_dir, 'urdf', 'robovisor.urdf.xacro')
    rviz_config_file = os.path.join(robovisor_dir, 'rviz', 'view.rviz')

    # Processar arquivo xacro para urdf
    doc = xacro.process_file(xacro_file)
    urdf = doc.toxml()

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': urdf}]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[{'use_sim_time': True}],
        arguments=['-d', rviz_config_file]
    )

    return LaunchDescription([
        robot_state_publisher_node,
        rviz_node
    ])
