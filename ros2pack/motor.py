import roslibpy
import time
import matplotlib.pyplot as plt


class Motor:

    def __init__(self, robot):
        self.ros = robot.ros
        self.talker = roslibpy.Topic(self.ros, '/cmd_vel', 'geometry_msgs/msg/Twist')
        self.encoder_listener = roslibpy.Topic(self.ros, '/encoder', 'motor_msgs/msg/Encoder')
        self.talker.advertise()
        self.encoder_listener.subscribe(self._on_encoder_msg)
        self.encoders = {
            'l_rpm': [0] * 200,
            'r_rpm': [0] * 200,
            'l_target': [0] * 200,
            'r_target': [0] * 200,
        }
        while not self.talker.is_advertised:
            time.sleep(0.1)

    def _on_encoder_msg(self, msg):
        self.encoders['l_rpm'].append(msg['l_rpm'])
        self.encoders['l_rpm'].pop(0)
        self.encoders['r_rpm'].append(msg['r_rpm'])
        self.encoders['r_rpm'].pop(0)
        self.encoders['l_target'].append(msg['l_target'])
        self.encoders['l_target'].pop(0)
        self.encoders['r_target'].append(msg['r_target'])
        self.encoders['r_target'].pop(0)

    def move(self, linear, angular):
        self.talker.publish(roslibpy.Message({'linear': {'x': float(linear)}, 'angular': {'z': float(angular)}}))
        time.sleep(0.01)

    def show_encoders(self):
        plt.ion()
        while True:
            plt.clf()

            plt.subplot(211)
            plt.plot(list(range(len(self.encoders['l_rpm']))), self.encoders['l_rpm'], c='r')
            plt.plot(list(range(len(self.encoders['l_target']))), self.encoders['l_target'], c='b')

            plt.subplot(212)
            plt.plot(list(range(len(self.encoders['r_rpm']))), self.encoders['r_rpm'], c='r')
            plt.plot(list(range(len(self.encoders['r_target']))), self.encoders['r_target'], c='b')

            plt.pause(0.05)
            plt.ioff()

    def __del__(self):
        self.talker.unadvertise()
        while self.talker.is_advertised:
            time.sleep(0.1)
