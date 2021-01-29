import roslibpy
import time
from .camera import Camera
from .imu import IMU
from .lidar import Lidar
from .motor import Motor


class Robot:
    # _instance_lock = threading.Lock()
    #
    # def __new__(cls, host='localhost', port=9090):
    #     with Robot._instance_lock:
    #         if not hasattr(Robot, '_instance'):
    #             Robot._instance = super().__new__(cls, host, port)
    #         assert host == Robot._instance.host and port == Robot._instance.port, 'Host and port must be consistent.'
    #     return Robot._instance

    def __init__(self, host='localhost', port=9090):
        self.host = host
        self.port = port
        self.ros = roslibpy.Ros(host=host, port=port)
        self.ros.run()

    def __del__(self):
        self.ros.terminate()
        while self.ros.is_connected:
            time.sleep(0.1)

    def get(self, device):
        if device == 'camera':
            return Camera(self)
        elif device == 'imu':
            return IMU(self)
        elif device == 'lidar':
            return Lidar(self)
        elif device == 'motor':
            return Motor(self)
        else:
            raise NotImplementedError('Supported devices: camera, imu, lidar, motor')
