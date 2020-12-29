import roslibpy
import numpy as np
import cv2
import math


class Lidar:

    def __init__(self, host='localhost', port=9090):
        self.ros = roslibpy.Ros(host=host, port=port)
        self.ros.run()
        self.listener = roslibpy.Topic(self.ros, '/scan', 'sensor_msgs/msg/LaserScan')
        self.listener.subscribe(self._on_msg)
        self.distances = [0] * 360

    def _on_msg(self, msg):
        self.distances = msg['ranges']

    def show(self):
        center = (320, 320)
        point_size = 1
        point_color = (0, 0, 255)  # BGR
        thickness = 1
        while True:
            img = np.zeros((640, 640, 3), np.uint8)
            cv2.circle(img, center, point_size, (0, 255, 0), 3)
            for i, d in enumerate(self.distances):
                if d is None or np.isinf(d) or np.isnan(d):
                    continue
                p_x = d * 50 * -math.cos(i * (2 * math.pi) / 360)
                p_y = d * 50 * math.sin(i * (2 * math.pi) / 360)
                cv2.circle(img, (int(center[0] + p_x), int(center[1] + p_y)), point_size, point_color, thickness)
                cv2.imshow('image', img)
            if cv2.waitKey(1) == 27:
                break

    def close(self):
        self.listener.unsubscribe()
        self.ros.terminate()

    def __del__(self):
        self.close()
