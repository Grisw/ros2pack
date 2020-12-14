import roslibpy


class Lidar:

    def __init__(self, host='localhost', port=9090):
        self.ros = roslibpy.Ros(host=host, port=port)
        self.ros.run()
        self.listener = roslibpy.Topic(self.ros, '/scan', 'sensor_msgs/msg/LaserScan')
        self.listener.subscribe(self._on_msg)
        self.distances = [0] * 360

    def _on_msg(self, msg):
        self.distances = msg['ranges']

    def __del__(self):
        self.ros.terminate()
