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

bno1= BNO055.BNO055(address=0x28)
bno2= BNO055.BNO055(address=0x29)

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

time.sleep(10)
print('Reading BNO055 data, press Ctrl-C to quit...')
with open ('BNO_testData.csv','wb') as csvfile:
    GPIO.output(B,GPIO.LOW)
    writer= csv.writer(csvfile)
    header=['time (ms)','x','y','z','w','x2','y2','z2','w2']
    writer.writerow(header)
    t0=int(round(time.time() * 1000))
    for i in range(10000):
        GPIO.output(G,GPIO.HIGH)
        # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
        sys, gyro, accel, mag = bno1.get_calibration_status()
        print('SysCal:{0:0.2F}'.format(sys))
        sys, gyro, accel, mag = bno2.get_calibration_status()

        # Print everything out.
        print('bno1')
        x1,y1,z1,w1 = bno1.read_quaternion()
        print('x={0:0.2F}, y={1:0.2F},z={2:0.2F},w={3:0.2F}'.format(x1,y1,z1,w1))

        print('bno2')
        x2,y2,z2,w2 = bno2.read_quaternion()
        print('x={0:0.2F}, y={1:0.2F},z={2:0.2F},w={3:0.2F}'.format(x2,y2,z2,w2))
        
        
        t=int(round(time.time() * 1000))-t0
        print(t)
        data=[t,x1,y1,z1,w1,x2,y2,z2,w2]
        writer.writerow(data)
        csvfile.flush()
         






