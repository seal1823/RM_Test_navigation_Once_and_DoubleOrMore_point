import rclpy
from geometry_msgs.msg import PoseStamped,Pose    #PoseStamped描述机器人在某个坐标系下、某个时间点的位置和姿态
from nav2_simple_commander.robot_navigator import BasicNavigator,TaskResult
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer
from tf_transformations import euler_from_quaternion,quaternion_from_euler
import rclpy.time

class PartolNode(BasicNavigator):
    def __init__(self, node_name='partol_node'):
        super().__init__(node_name)
        self.declare_parameter('initial_point',[0.0, 0.0, 0.0])
        self.declare_parameter('target_points',[0.0, 0.0, 0.0, 1.0, 1.0, 1.57])
        self.declare_parameter('img_save_path','')
        self.initial_point_ = self.get_parameter('initial_point').value
        self.target_points_ = self.get_parameter('target_points').value
        self.img_save_path = self.get_parameter('img_save_path').value
        self.buffer = Buffer()

    def get_pose_by_xyyaw(self,x,y,yaw):
        '''
        return PoseStamped对象
        '''
        pose = PoseStamped()
        pose.header.frame_id ='map'
        pose.pose.position.x = x
        pose.pose.position.y = y
        quat = quaternion_from_euler(0,0,yaw)
        pose.pose.orientation.x = quat[0]
        pose.pose.orientation.y = quat[1]
        pose.pose.orientation.z = quat[2]
        pose.pose.orientation.w = quat[3]
        return pose
    
    def init_robot_pose(self):
        '''
        初始化机器人位姿
        '''
        self.initial_point_ = self.get_parameter('initial_point').value
        init_pose = self.get_pose_by_xyyaw(self.initial_point_[0],self.initial_point_[1],self.initial_point_[2])
        self.setInitialPose(init_pose)
        self.waitUntilNav2Active()

    def get_target_point(self):
        '''
        通过参数值获取目标点的集合
        '''
        points = []
        self.target_points_ = self.get_parameter('target_points').value
        for index in range(int(len(self.target_points_)/3)):
            x = self.target_points_[index*3]
            y = self.target_points_[index*3+1]
            yaw = self.target_points_[index*3+2]
            points.append([x,y,yaw])
            self.get_logger().info(f'获取到目标点{index}->{x},{y},{yaw}')
        return points

    def nav_to_pose(self,target_point):
        '''
        导航到目标点
        '''
        self.goToPose(target_point)
        while not self.isTaskComplete():
            feedback = self.getFeedback()
            self.get_logger().info(f'剩余距离:{feedback.distance_remaining}')
        result = self.getResult()
        self.get_logger().info(f'导航结果:{result}')

    def get_curren_pose(self):
        '''
        获取当前机器人的位置
        '''
        while rclpy.ok():
            try:
                tf = self.buffer.lookup_transform(
                    'map', 'base_footprint', rclpy.time.Time(seconds=0), rclpy.time.Duration(seconds=1))
                transform = tf.transform
                self.get_logger().info(f"平移:{transform.translation}")
                return transform
            except Exception as e:
                self.get_logger().warn(f'不能够获取坐标变换，原因: {str(e)}')


def main():
    rclpy.init()
    partol = PartolNode()
    partol.init_robot_pose()

    while rclpy.ok():
        points = partol.get_target_point()
        for point in points:
            x,y,yaw = point[0],point[1],point[2]
            target_pose = partol.get_pose_by_xyyaw(x,y,yaw)
            partol.nav_to_pose(target_pose)
            
    rclpy.shutdown()