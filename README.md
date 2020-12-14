# ros2pack

## Install

`pip install git+https://github.com/Robot-Course/ros2pack.git`

## Uninstall

`pip uninstall ros2pack`

## Usage

```python
import ros2pack

imu = ros2pack.IMU()
print(imu.RPY)
print(imu.angular_velocity)
print(imu.linear_acceleration)
```
