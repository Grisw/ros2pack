import roslibpy
import math


class IMU:

    def __init__(self, host='localhost', port=9090):
        self.ros = roslibpy.Ros(host=host, port=port)
        self.ros.run()
        self.listener = roslibpy.Topic(self.ros, '/imu', 'sensor_msgs/msg/Imu')
        self.listener.subscribe(self._on_msg)
        self.RPY = (0, 0, 0)
        self.angular_velocity = (0, 0, 0)
        self.linear_acceleration = (0, 0, 0)

    def _on_msg(self, msg):
        self.RPY = self.quaternion_to_euler(msg['orientation']['w'], msg['orientation']['x'], msg['orientation']['y'], msg['orientation']['z'])
        self.angular_velocity = msg['angular_velocity']['x'], msg['angular_velocity']['y'], msg['angular_velocity']['z']
        self.linear_acceleration = msg['linear_acceleration']['x'], msg['linear_acceleration']['y'], msg['linear_acceleration']['z']

    def quaternion_to_euler(self, w, x, y, z):
        """w、x、y、z to euler angles"""
        r = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
        p = math.asin(2 * (w * y - z * x))
        y = math.atan2(2 * (w * z + x * y), 1 - 2 * (z * z + y * y))

        roll = r * 180 / math.pi
        pitch = p * 180 / math.pi
        yaw = y * 180 / math.pi

        return roll, pitch, yaw

    def close(self):
        self.listener.unsubscribe()
        self.ros.terminate()

    def __del__(self):
        self.close()
