import sys,time,logging
from Adafruit_BNO055 import BNO055

bno1= BNO055.BNO055(address=0x28)
bno2= BNO055.BNO055(address=0x29)
# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not (bno1.begin() and bno2.begin()):
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status1, self_test1, error2 = bno1.get_system_status()
status2, self_test2, error2 = bno2.get_system_status()

print('System status 1: {0}'.format(status1))
print('Self test result 1 (0x0F is normal): 0x{0:02X}'.format(self_test1))
# Print out an error if system status is in error mode.
if status1 == 0x01:
    print('System 1 error: {0}'.format(error1))
    print('See datasheet section 4.3.59 for the meaning.')

print('System status 2: {0}'.format(status2))
print('Self test result 2 (0x0F is normal): 0x{0:02X}'.format(self_test2))
# Print out an error if system status is in error mode.
if status2 == 0x01:
    print('System 2 error: {0}'.format(error2))
    print('See datasheet section 4.3.59 for the meaning.')

sw1, bl1, accel1, mag1, gyro1 = bno1.get_revision()
sw2, bl2, accel2, mag2, gyro2 = bno2.get_revision()

print('Reading BNO055 data, press Ctrl-C to quit...')
while True:
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    #heading, roll, pitch = bno.read_euler()
    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    sys, gyro, accel, mag = bno1.get_calibration_status()
    sys, gyro, accel, mag = bno2.get_calibration_status()
    # Print everything out.
    #print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
    #      heading, roll, pitch, sys, gyro, accel, mag))
    # Other values you can optionally read:
    # Orientation as a quaternion:
    print('bno1')
    x,y,z,w = bno1.read_quaternion()
    print('x={0:0.2F}, y={1:0.2F},z={2:0.2F},w={3:0.2F}'.format(x,y,z,w))
    print('bno2')
    x,y,z,w = bno2.read_quaternion()
    print('x={0:0.2F}, y={1:0.2F},z={2:0.2F},w={3:0.2F}'.format(x,y,z,w))
    # Sensor temperature in degrees Celsius:
    #temp_c = bno.read_temp()
    # Magnetometer data (in micro-Teslas):
    #x,y,z = bno.read_magnetometer()
    # Gyroscope data (in degrees per second):
    #x,y,z = bno.read_gyroscope()
    # Accelerometer data (in meters per second squared):
    #x,y,z = bno.read_accelerometer()
    # Linear acceleration data (i.e. acceleration from movement, not gravity--
    # returned in meters per second squared):
    #x,y,z = bno.read_linear_acceleration()
    # Gravity acceleration data (i.e. acceleration just from gravity--returned
    # in meters per second squared):
    #x,y,z = bno.read_gravity()
    # Sleep for a second until the next reading.
    time.sleep(1)
