import launch
import launch_ros
import os
from ament_index_python.packages import get_package_share_directory
import launch_ros.parameter_descriptions

def generate_launch_description():
    # 获取默认的urdf路径
    autopartol_robot_path = get_package_share_directory('autopartol_robot')
    default_partol_config_path = autopartol_robot_path + '/config/partol_config.yaml'
    action_partol_node = launch_ros.actions.Node(
        package='autopartol_robot',
        executable='partol_node',
        output = 'screen',
        parameters=[default_partol_config_path]
    )

    return launch.LaunchDescription([
        action_partol_node,
    ])