import roslibpy
import threading
import time


class ROS:
    _instance_lock = threading.Lock()

    def __new__(cls, host='localhost', port=9090):
        with ROS._instance_lock:
            if not hasattr(ROS, '_instance'):
                ROS._instance = super().__new__(cls, host, port)
            assert host == ROS._instance.host and port == ROS._instance.port, 'Host and port must be consistent.'
        return ROS._instance

    def __init__(self, host='localhost', port=9090):
        self.host = host
        self.port = port
        self.ros = roslibpy.Ros(host=host, port=port)
        self.ros.run()

    def __del__(self):
        self.ros.terminate()
        while self.ros.is_connected:
            time.sleep(0.1)
