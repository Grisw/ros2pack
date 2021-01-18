import roslibpy
from .rosbridge import ROS
import time


class Motor:

    def __init__(self, host='localhost', port=9090):
        self.ros = ROS(host=host, port=port).ros
        self.talker = roslibpy.Topic(self.ros, '/cmd_vel', 'geometry_msgs/msg/Twist')
        self.talker.advertise()
        while not self.talker.is_advertised:
            time.sleep(0.1)

    def move(self, linear, angular):
        self.talker.publish(roslibpy.Message({'linear': {'x': float(linear)}, 'angular': {'z': float(angular)}}))
        time.sleep(0.01)

    def __del__(self):
        self.talker.unadvertise()
        while self.talker.is_advertised:
            time.sleep(0.1)
