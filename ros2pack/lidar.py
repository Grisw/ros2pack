import roslibpy
import numpy as np
import cv2
import math
import time


class Lidar:

    def __init__(self, robot):
        self.ros = robot.ros
        self.listener = roslibpy.Topic(self.ros, '/scan', 'sensor_msgs/msg/LaserScan')
        self.listener.subscribe(self._on_msg)
        self.distances = [0] * 360
        self.received = False
        while not self.received:
            time.sleep(0.1)

    def _on_msg(self, msg):
        self.received = True
        self.distances = msg['ranges']

    def show(self, winname='lidar'):
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
                cv2.imshow(winname, img)
            if cv2.waitKey(1) == 27:
                break

    def __del__(self):
        self.listener.unsubscribe()
        while self.listener.is_subscribed:
            time.sleep(0.1)
