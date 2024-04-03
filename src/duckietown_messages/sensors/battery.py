from ..base import BaseMessage
from ..standard.header import Header, AUTO

## TODO: Fully define the BatteryState message to be compatible with the ROS message definition 
##      http://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/BatteryState.html
 
class BatteryState(BaseMessage):
    header: Header = AUTO

    voltage: float
    present: bool


