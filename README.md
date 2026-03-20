# Robot_Master_Task2
导航思路基于B站中鱼香ros的思路，并进行了思考和理解
## 1.导航前的准备
首先在fishbot_description中进行机器人部件的urdf文件的编写，采用xcaro，声明宏文件等来进行编写，对里程计，雷达，平衡轮等进行编写
### 通过launch脚本文件启动gazebo仿真，并将机器人加载进世界中
## 2.编写导航相关的launch文件和copy yaml文件
在fishbot_navigation2文件夹中
### I.使用get_packae_share_directory来通过文件夹的名字来获取share路径，并通过os.path.join来拼接文件路径
### II.提前使用launch.substitutions.LaunchConfiguration来提起进行参数的引用，后续用DeclareLaunchArgument来复用，并1使用其默认值
### III.launch文件会写，但是yaml文件孩子是真不会了，但是好像膨胀值和误差就是在这个文件中进行修改的
## 3.进行单点导航的代码编写
在fishbot_application文件夹中
### I.通过init_robot_pose来自动的进行位置的初始化
### II.在通过nav_to_pose来进行单点的位置导航
### III.有一个get_robot_pose通过tf树来获取车的实时位姿
## 3.进行多点导航的代码编写
使用了两种---一种是在fishbot_application下的waypoint_follow；第二种是在autopartol_robot下的将fishbot_applition中的进行整合
## 4.作者
25 AI 赵荣豪