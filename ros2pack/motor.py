import roslibpy


class Motor:

    def __init__(self, host='localhost', port=9090):
        self.ros = roslibpy.Ros(host=host, port=port)
        self.ros.run()
        self.talker = roslibpy.Topic(self.ros, '/cmd_vel', 'geometry_msgs/msg/Twist')

    def move(self, linear, angular):
        if self.ros.is_connected:
            self.talker.publish(roslibpy.Message({'linear': {'x': linear}, 'angular': {'z': angular}}))

    def close(self):
        self.talker.unadvertise()
        self.ros.terminate()

    def __del__(self):
        self.close()
