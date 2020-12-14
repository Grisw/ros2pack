# ros2pack

## Install

1. `pip install git+https://github.com/Robot-Course/ros2pack.git`

## Usage

```python
import ros2pack

imu = ros2pack.IMU()
print(imu.RPY)
print(imu.angular_velocity)
print(imu.linear_acceleration)
```