import roslibpy
from .rosbridge import ROS
import math
import time
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


class IMU:

    def __init__(self, host='localhost', port=9090):
        self.ros = ROS(host=host, port=port).ros
        self.listener = roslibpy.Topic(self.ros, '/imu', 'sensor_msgs/msg/Imu')
        self.listener.subscribe(self._on_msg)
        self.RPY = (0, 0, 0)
        self.quaternion = (0, 0, 0, 0)
        self.angular_velocity = (0, 0, 0)
        self.linear_acceleration = (0, 0, 0)
        self.received = False
        while not self.received:
            time.sleep(0.1)

    def _on_msg(self, msg):
        self.received = True
        self.quaternion = msg['orientation']['w'], msg['orientation']['x'], msg['orientation']['y'], msg['orientation']['z']
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

    def show(self):
        verticies = (
            (-0.7, 1, -0.1),
            (-0.7, 1, 0.1),
            (-0.7, -1, 0.1),
            (-0.7, -1, -0.1),
            (0.7, 1, -0.1),
            (0.7, 1, 0.1),
            (0.7, -1, -0.1),
            (0.7, -1, 0.1)
            )

        quads = (
            (0, 3, 6, 4),
            (1, 2, 7, 5),
            (0, 1, 2, 3),
            (4, 5, 7, 6),
            (0, 1, 5, 4),
            (2, 3, 6, 7)
        )

        colors = (
            (0, 100, 255, 255),
            (0, 100, 255, 255),
            (128, 128, 128, 255),
            (128, 128, 128, 255),
            (128, 128, 128, 255),
            (128, 128, 128, 255)
        )

        def Cube():
            glBegin(GL_QUADS)
            for quad, color in zip(quads, colors):
                for vertex in quad:
                    glColor4ub(*color)
                    glVertex3fv(verticies[vertex])
            glEnd()

        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

        glEnable(GL_DEPTH_TEST)

        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

        glTranslatef(0.0, 0.0, -5)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

            matrix = np.array([
                (self.quaternion[0] * self.quaternion[0]) + (self.quaternion[1] * self.quaternion[1]) - (self.quaternion[2] * self.quaternion[2]) - (self.quaternion[3] * self.quaternion[3]),
                (2 * self.quaternion[1] * self.quaternion[2]) + (2 * self.quaternion[0] * self.quaternion[3]),
                (2 * self.quaternion[1] * self.quaternion[3]) - (2 * self.quaternion[0] * self.quaternion[2]),
                0,
                (2 * self.quaternion[1] * self.quaternion[2]) - (2 * self.quaternion[0] * self.quaternion[3]),
                (self.quaternion[0] * self.quaternion[0]) - (self.quaternion[1] * self.quaternion[1]) + (self.quaternion[2] * self.quaternion[2]) - (self.quaternion[3] * self.quaternion[3]),
                (2 * self.quaternion[2] * self.quaternion[3]) + (2 * self.quaternion[0] * self.quaternion[1]),
                0,
                (2 * self.quaternion[1] * self.quaternion[3]) + (2 * self.quaternion[0] * self.quaternion[2]),
                (2 * self.quaternion[2] * self.quaternion[3]) - (2 * self.quaternion[0] * self.quaternion[1]),
                (self.quaternion[0] * self.quaternion[0]) - (self.quaternion[1] * self.quaternion[1]) - (self.quaternion[2] * self.quaternion[2]) + (self.quaternion[3] * self.quaternion[3]),
                0,
                0,
                0,
                0,
                1
            ])

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glPushMatrix()
            glMultMatrixf(matrix)
            Cube()
            glPopMatrix()
            pygame.display.flip()
            pygame.time.wait(10)

    def __del__(self):
        self.listener.unsubscribe()
        while self.listener.is_subscribed:
            time.sleep(0.1)
