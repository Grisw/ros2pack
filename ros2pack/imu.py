import roslibpy
import math
import time
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


class IMU:

    def __init__(self, host='localhost', port=9090):
        self.ros = roslibpy.Ros(host=host, port=port)
        self.ros.run()
        self.listener = roslibpy.Topic(self.ros, '/imu', 'sensor_msgs/msg/Imu')
        self.listener.subscribe(self._on_msg)
        self.RPY = (0, 0, 0)
        self.angular_velocity = (0, 0, 0)
        self.linear_acceleration = (0, 0, 0)
        self.received = False
        while not self.received:
            time.sleep(0.1)

    def _on_msg(self, msg):
        self.received = True
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
            (1, -0.1, -0.7),
            (1, 0.1, -0.7),
            (-1, 0.1, -0.7),
            (-1, -0.1, -0.7),
            (1, -0.1, 0.7),
            (1, 0.1, 0.7),
            (-1, -0.1, 0.7),
            (-1, 0.1, 0.7)
            )

        edges = (
            (0,1),
            (0,3),
            (0,4),
            (2,1),
            (2,3),
            (2,7),
            (6,3),
            (6,4),
            (6,7),
            (5,1),
            (5,4),
            (5,7)
            )

        def Cube():
            glBegin(GL_LINES)
            for edge in edges:
                for vertex in edge:
                    glVertex3fv(verticies[vertex])
            glEnd()

        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

        glTranslatef(0.0, 0.0, -5)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

            glPushMatrix()
            glRotatef(self.RPY[0], 0, 0, 1)
            glRotatef(self.RPY[1], 1, 0, 0)
            glRotatef(self.RPY[2], 0, 1, 0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            Cube()
            glPopMatrix()
            pygame.display.flip()
            pygame.time.wait(10)

    def close(self):
        self.listener.unsubscribe()
        self.ros.terminate()

    def __del__(self):
        self.close()
