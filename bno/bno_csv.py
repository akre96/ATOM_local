import smbus,time,csv,logging
import sys, getopt 
from Adafruit_BNO055 import BNO055
import RPi.GPIO as GPIO

def wait():
    m.getch()



# Pin Def LED

R= 17
G=27
B=22


#LED SETUP

GPIO.setmode(GPIO.BCM)

GPIO.setup(R,GPIO.OUT)
GPIO.setup(G,GPIO.OUT)
GPIO.setup(B,GPIO.OUT)
GPIO.output(R,GPIO.LOW)
GPIO.output(G,GPIO.LOW)
GPIO.output(B,GPIO.LOW)

bno1= BNO055.BNO055(address=0x28) # Sensor at default register
bno2= BNO055.BNO055(address=0x29) # Sensor at 

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not (bno1.begin() and bno2.begin()):
    GPIO.output(R,GPIO.HIGH)
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status1, self_test1, error2 = bno1.get_system_status()
status2, self_test2, error2 = bno2.get_system_status()

print('System status 1: {0}'.format(status1))
print('Self test result 1 (0x0F is normal): 0x{0:02X}'.format(self_test1))


# Print out an error if system status is in error mode.
if status1 == 0x01:
    GPIO.output(R,GPIO.HIGH)
    print('System 1 error: {0}'.format(error1))
    print('See datasheet section 4.3.59 for the meaning.')

print('System status 2: {0}'.format(status2))
print('Self test result 2 (0x0F is normal): 0x{0:02X}'.format(self_test2))

if status2 == 0x01:
    GPIO.output(R,GPIO.HIGH)
    print('System 2 error: {0}'.format(error2))
    print('See datasheet section 4.3.59 for the meaning.')


GPIO.output(B,GPIO.HIGH)
sw1, bl1, accel1, mag1, gyro1 = bno1.get_revision()
sw2, bl2, accel2, mag2, gyro2 = bno2.get_revision()

# Wait for interaction before moving forward
print ("Press Enter to Begin Data Collection")
raw_input()

# Data Collection
print('Reading BNO055 data, press Ctrl-C to quit...')
with open ('BNO_testData.csv','wb') as csvfile:
    GPIO.output(B,GPIO.LOW)
    writer= csv.writer(csvfile)
    header=['time (ms)','qx','qy','qz','qw','qx2','qy2','qz2','qw2','mx1','my1','mz1','mx2','my2','mz2','gx1','gy1','gz1','gx2','gy2','gz2','ax1','ay1','az1','ax2','ay2','az2','lx1','ly1','lz1','lx2','ly2','lz2','grx1','gry1','grz1','grx2','gry2','grz2']
    writer.writerow(header)
    t0=int(round(time.time() * 1000))
    GPIO.output(G,GPIO.HIGH)

    # @ ~50Hz gets 8-10 minutes of data
    for i in range(10000):
        # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
        #sys, gyro, accel, mag = bno1.get_calibration_status()
        #print('SysCal:{0:0.2F}'.format(sys))
        #sys, gyro, accel, mag = bno2.get_calibration_status()

        # Print everything out.
        #print('bno1')
        qx1,qy1,qz1,qw1 = bno1.read_quaternion()
        #print('x={0:0.2F}, y={1:0.2F},z={2:0.2F},w={3:0.2F}'.format(x1,y1,z1,w1))

        #print('bno2')
        qx2,qy2,qz2,qw2 = bno2.read_quaternion()
        #print('x={0:0.2F}, y={1:0.2F},z={2:0.2F},w={3:0.2F}'.format(x2,y2,z2,w2))

        # Magnetometer data (in micro-Teslas):
        mx1,my1,mz1 = bno1.read_magnetometer()
        mx2,my2,mz2 = bno2.read_magnetometer()

        # Gyroscope data (in degrees per second):
        gx1,gy1,gz1 = bno1.read_gyroscope()
        gx2,gy2,gz2 = bno2.read_gyroscope()

        # Accelerometer data (in meters per second squared):
        ax1,ay1,az1 = bno1.read_accelerometer()
        ax2,ay2,az2 = bno2.read_accelerometer()

        # Linear acceleration data (i.e. acceleration from movement, not gravity--
        # returned in meters per second squared):
        lx1,ly1,lz1 = bno1.read_linear_acceleration()
        lx2,ly2,lz2 = bno2.read_linear_acceleration()

        # Gravity acceleration data (i.e. acceleration just from gravity--returned
        # in meters per second squared):
        grx1,gry1,grz1 = bno1.read_gravity()
        grx2,gry2,grz2 = bno2.read_gravity()
        
        
        t=int(round(time.time() * 1000))-t0
        data=[t,qx1,qy1,qz1,qw1,qx2,qy2,qz2,qw2,mx1,my1,mz1,mx2,my2,mz2,gx1,gy1,gz1,gx2,gy2,gz2,ax1,ay1,az1,ax2,ay2,az2,lx1,ly1,lz1,lx2,ly2,lz2,grx1,gry1,grz1,grx2,gry2,grz2]
        writer.writerow(data)
        csvfile.flush()
         



GPIO.output(G,GPIO.LOW)
GPIO.cleanup()



