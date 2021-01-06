import roslibpy
import cv2
import numpy as np
import time


class Camera:

    def __init__(self, host='localhost', port=9090):
        self.ros = roslibpy.Ros(host=host, port=port)
        self.ros.run()
        self.listener = roslibpy.Topic(self.ros, '/camera', 'sensor_msgs/msg/CompressedImage')
        self.listener.subscribe(self._on_msg)
        self.image = None
        while self.image is None:
            time.sleep(0.1)

    def _on_msg(self, msg):
        buf = np.ndarray(shape=(1, len(msg['data'])),
                         dtype=np.uint8, buffer=bytes(msg['data']))
        self.image = cv2.imdecode(buf, cv2.IMREAD_ANYCOLOR)

    def save(self, name):
        assert self.image is not None, 'No image received.'
        cv2.imwrite(name, self.image)

    def show(self, winname='camera'):
        assert self.image is not None, 'No image received.'
        while True:
            cv2.imshow(winname, self.image)
            k = cv2.waitKey(1)
            if k == 27:
                break

    def close(self):
        self.listener.unsubscribe()
        self.ros.terminate()
        while self.ros.is_connected:
            time.sleep(0.1)

    def __del__(self):
        self.close()
