import Adafruit_BNO055

sensor = Adafruit_BNO055.BNO055()


print('Temperature: {} degrees C'.format(sensor.temperature))
print('Accelerometer (m/s^2): {}'.format(sensor.accelerometer))
print('Magnetometer (microteslas): {}'.format(sensor.magnetometer))
print('Gyroscope (deg/sec): {}'.format(sensor.gyroscope))
print('Euler angle: {}'.format(sensor.euler))
print('Quaternion: {}'.format(sensor.quaternion))
print('Linear acceleration (m/s^2): {}'.format(sensor.linear_acceleration))
print('Gravity (m/s^2): {}'.format(sensor.gravity))
