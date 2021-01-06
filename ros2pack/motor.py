import roslibpy
import time


class Motor:

    def __init__(self, host='localhost', port=9090):
        self.ros = roslibpy.Ros(host=host, port=port)
        self.ros.run()
        self.talker = roslibpy.Topic(self.ros, '/cmd_vel', 'geometry_msgs/msg/Twist')
        self.talker.advertise()
        while not self.talker.is_advertised:
            time.sleep(0.1)

    def move(self, linear, angular):
        self.talker.publish(roslibpy.Message({'linear': {'x': float(linear)}, 'angular': {'z': float(angular)}}))

    def close(self):
        self.talker.unadvertise()
        self.ros.terminate()
        while self.ros.is_connected:
            time.sleep(0.1)

    def __del__(self):
        self.close()
