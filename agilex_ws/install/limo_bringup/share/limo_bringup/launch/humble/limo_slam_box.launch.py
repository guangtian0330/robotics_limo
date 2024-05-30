import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time',default='false')
    slam_params_file = LaunchConfiguration('slam_params_file')
    rviz_config_dir = os.path.join(
        get_package_share_directory('limo_bringup'),
        'rviz',
        'slam_toolbox.rviz')

    # scout_node=IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([os.path.join(
    #     get_package_share_directory('scout_base'), 'launch'),
    #     '/scout_mini_base.launch.py']),
    #     launch_arguments={'control_rate':50}.items()
    #     ),

    # declare_use_sim_time_argument = DeclareLaunchArgument(
    #     'use_sim_time',
    #     default_value='false',
    #     description='Use simulation/Gazebo clock')
    # declare_slam_params_file_cmd = DeclareLaunchArgument(
    #     'slam_params_file',
    #     default_value=os.path.join(get_package_share_directory("limo_bringup"),
    #                                'config', 'slam_toolbox.yaml'),
    #     description='Full path to the ROS2 parameters file to use for the slam_toolbox node')

    # start_sync_slam_toolbox_node = Node(
    #     parameters=[
    #       slam_params_file,
    #       {'use_sim_time': use_sim_time}
    #     ],
    #     package='slam_toolbox',
    #     executable='sync_slam_toolbox_node',
    #     name='slam_toolbox',
    #     output='screen')

    # ld = LaunchDescription()

    # ld.add_action(declare_use_sim_time_argument)
    # ld.add_action(declare_slam_params_file_cmd)
    # ld.add_action(start_sync_slam_toolbox_node)
    # ld.add_action(scout_node)

    return LaunchDescription([
        # Node(
        #     package='rf2o_laser_odometry',
        #     executable='rf2o_laser_odometry_node',
        #     name='rf2o_laser_odometry',
        #     output='screen',
        #     parameters=[{
        #         'laser_scan_topic' : '/scan',
        #         'odom_topic' : '/odom',
        #         'publish_tf' : True,
        #         'base_frame_id' : 'base_link',
        #         'odom_frame_id' : 'odom',
        #         'init_pose_from_topic' : '',
        #         'freq' : 20.0}],),
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation/Gazebo clock'),
            
        DeclareLaunchArgument(
            'slam_params_file',
            default_value=os.path.join(get_package_share_directory("limo_bringup"),
                                    'config_files', 'slam_box.yaml'),
            description='Full path to the ROS2 parameters file to use for the slam_toolbox node'),
        Node(
            parameters=[
                slam_params_file,
                {'use_sim_time': use_sim_time}
            ],
            package='slam_toolbox',
            executable='sync_slam_toolbox_node',
            name='slam_toolbox',
            output='screen'),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'),
    ])