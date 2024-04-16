from duckietown_messages.standard.header import AUTO
from duckietown_msgs.msg import BaseMessage
from geometry_msgs.msg import Quaternion, Vector3

class Imu(BaseMessage):
    """Imu message, used to store the IMU data.
    Refer to the ROS message definition for more information.
    http://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/Imu.html
    """
    
    def __init__(self):
        super(Imu, self).__init__()
        self.header = AUTO
        self.orientation = Quaternion()
        self.orientation_covariance = [0.0] * 9
        self.angular_velocity = Vector3()
        self.angular_velocity_covariance = [0.0] * 9
        self.linear_acceleration = Vector3()
        self.linear_acceleration_covariance = [0.0] * 9