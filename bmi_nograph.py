import smbus,time,csv
import sys, getopt 
from time import sleep
import plotly.plotly as py
#from plotly.graph_objs import Scatter, Layout, Figure

#username = 'akre96'
#api_key='cC6LIzUltGaMR953sVxH'
#stream_token = 'a7adx0bmhu'
#stream_token_2 = 'e9w7o9hj9a'
#stream_token_3 = 'd5izfqfdn7'
#
#py.sign_in(username, api_key)
#
#trace1 = Scatter(
#    x=[],
#    y=[],
#    stream=dict(
#        token=stream_token,
#        maxpoints=200
#    )
#)
#trace2 = Scatter(
#    x=[],
#    y=[],
#    stream=dict(
#        token=stream_token_2,
#        maxpoints=200
#    )
#)
#
#trace3 = Scatter(
#    x=[],
#    y=[],
#    stream=dict(
#        token=stream_token_3,
#        maxpoints=200
#    )
#)
#layout = Layout(
#    title='Acc 1 and 2'
#)
#
#fig = Figure(data=[trace1,trace2], layout=layout)
#
#print py.plot(fig, filename='Raspberry Pi Streaming Example Values')
#
#stream = py.Stream(stream_token)
#stream.open()
#stream_2 = py.Stream(stream_token_2)
#stream_2.open()
#stream_3 = py.Stream(stream_token_3)
#stream_3.open()

bus=smbus.SMBus(1)

BMI160_DEVICE_ADDRESS = 0x69
BMI160_DEVICE_ADDRESS_2 = 0x68

BMI160_REGA_USR_CHIP_ID      = 0x00
BMI160_REGA_USR_ACC_CONF_ADDR     = 0x40 
BMI160_REGA_USR_ACC_RANGE_ADDR    = 0x41
BMI160_REGA_USR_GYR_CONF_ADDR     = 0x42
BMI160_REGA_USR_GYR_RANGE_ADDR    = 0x43

BMI160_REGA_CMD_CMD_ADDR          =   0x7e
BMI160_REGA_CMD_EXT_MODE_ADDR     =   0x7f

CMD_SOFT_RESET_REG      = 0xb6

CMD_PMU_ACC_SUSPEND     = 0x10
CMD_PMU_ACC_NORMAL      = 0x11
CMD_PMU_ACC_LP1         = 0x12
CMD_PMU_ACC_LP2         = 0x13
CMD_PMU_GYRO_SUSPEND    = 0x14
CMD_PMU_GYRO_NORMAL     = 0x15
CMD_PMU_GYRO_FASTSTART  = 0x17

BMI160_USER_DATA_14_ADDR = 0X12 # accel x 
BMI160_USER_DATA_15_ADDR = 0X13 # accel x 
BMI160_USER_DATA_16_ADDR = 0X14 # accel y 
BMI160_USER_DATA_17_ADDR = 0X15 # accel y 
BMI160_USER_DATA_18_ADDR = 0X16 # accel z 
BMI160_USER_DATA_19_ADDR = 0X17 # accel z 

BMI160_USER_DATA_8_ADDR  = 0X0C 
BMI160_USER_DATA_9_ADDR  = 0X0D
BMI160_USER_DATA_10_ADDR = 0X0E
BMI160_USER_DATA_11_ADDR = 0X0F
BMI160_USER_DATA_12_ADDR = 0X10
BMI160_USER_DATA_13_ADDR = 0X11

if len(sys.argv) == 1 :
  print "Usage : bmi160.py [ A | G ] "
  sys.exit()

chipid = bus.read_byte_data(BMI160_DEVICE_ADDRESS, BMI160_REGA_USR_CHIP_ID )

print "---------"
if chipid == 0xD1 :
  print "chip id is 0x%X, BMI160" % chipid
else :
  print "Exit"
  sys.exit()
print "---------" 

#bus.write_byte_data(BMI160_DEVICE_ADDRESS, 0x03, 0x19 )
#tmp = bus.read_byte_data(BMI160_DEVICE_ADDRESS, 0x03)
#print "tmp 0x%X, BMI160" % tmp 

#chip init
bus.write_byte_data(BMI160_DEVICE_ADDRESS, BMI160_REGA_USR_ACC_CONF_ADDR, 0x25)
bus.write_byte_data(BMI160_DEVICE_ADDRESS, BMI160_REGA_USR_ACC_RANGE_ADDR, 0b1100)
bus.write_byte_data(BMI160_DEVICE_ADDRESS, BMI160_REGA_USR_GYR_CONF_ADDR, 0x26)
bus.write_byte_data(BMI160_DEVICE_ADDRESS, BMI160_REGA_USR_GYR_RANGE_ADDR, 0x1)

#bus.write_byte_data(BMI160_DEVICE_ADDRESS_2, BMI160_REGA_USR_ACC_CONF_ADDR, 0x25)
#bus.write_byte_data(BMI160_DEVICE_ADDRESS_2, BMI160_REGA_USR_ACC_RANGE_ADDR, 0b1100)
#bus.write_byte_data(BMI160_DEVICE_ADDRESS_2, BMI160_REGA_USR_GYR_CONF_ADDR, 0x26)
#bus.write_byte_data(BMI160_DEVICE_ADDRESS_2, BMI160_REGA_USR_GYR_RANGE_ADDR, 0x1)

#command register
#bus.write_byte_data(BMI160_DEVICE_ADDRESS, BMI160_REGA_CMD_CMD_ADDR, CMD_SOFT_RESET_REG)

def enable_accel( ) :
  acc_value = [ 0, 0, 0, 0, 0, 0]
  #op_mode set to 0 and go to normal mode
  sleep(0.1)
  bus.write_byte_data(BMI160_DEVICE_ADDRESS, BMI160_REGA_CMD_CMD_ADDR, CMD_PMU_ACC_NORMAL)
  sleep(0.1)

  #read acc xyz
  acc_value = bus.read_i2c_block_data(BMI160_DEVICE_ADDRESS, BMI160_USER_DATA_14_ADDR, 6)

  print "0x%X, 0x%X 0x%X" % ( acc_value[0], acc_value[1], acc_value[2])  
  print "0x%X, 0x%X 0x%X" % ( acc_value[3], acc_value[4], acc_value[5])  
  acc_x =  (acc_value[1] << 8) | acc_value[0]
  acc_y =  (acc_value[3] << 8) | acc_value[2]
  acc_z =  (acc_value[5] << 8) | acc_value[4]

  #Need to be remap according to 1 pin postion
  print "accel x = %d, y = %d z = %d" % (acc_x, acc_y, acc_z)
  return;

def enable_gyro( ) :
  gyro_value = [ 0, 0, 0, 0, 0, 0]
  #op_mode set to 0 and go to normal mode
  sleep(0.1)
  bus.write_byte_data(BMI160_DEVICE_ADDRESS, BMI160_REGA_CMD_CMD_ADDR, CMD_PMU_GYRO_NORMAL)
  sleep(0.1)

  #read gyro xyz
  gyro_value = bus.read_i2c_block_data(BMI160_DEVICE_ADDRESS, BMI160_USER_DATA_8_ADDR, 6)

  print gyro_value
  gyro_x =  (gyro_value[1] << 8) | gyro_value[0]
  gyro_y =  (gyro_value[3] << 8) | gyro_value[2]
  gyro_z =  (gyro_value[5] << 8) | gyro_value[4]

  #Need to be remap according to 1 pin postion
  print "gyro x = %d, y = %d z = %d" % (gyro_x, gyro_y, gyro_z)

  return;

def enable_both( ) :


    acc_value = [ 0, 0, 0, 0, 0, 0]
    gyro_value = [ 0, 0, 0, 0, 0, 0]
    #op_mode set to 0 and go to normal mode
    sleep(0.1)
    bus.write_byte_data(BMI160_DEVICE_ADDRESS, BMI160_REGA_CMD_CMD_ADDR, CMD_PMU_ACC_NORMAL)
    bus.write_byte_data(BMI160_DEVICE_ADDRESS_2, BMI160_REGA_CMD_CMD_ADDR, CMD_PMU_ACC_NORMAL)
    sleep(0.1)
    bus.write_byte_data(BMI160_DEVICE_ADDRESS, BMI160_REGA_CMD_CMD_ADDR, CMD_PMU_GYRO_NORMAL)
    bus.write_byte_data(BMI160_DEVICE_ADDRESS_2, BMI160_REGA_CMD_CMD_ADDR, CMD_PMU_GYRO_NORMAL)
    sleep(0.1)

    #read acc xyz
    with open ('testData.csv','wb') as csvfile:
        writer= csv.writer(csvfile)
        header=['time','ax','ay','az','gx','gy','gz','ax2','ay2','az2','gx2','gy2','gz2']
        writer.writerow(header)
        i=1
        z=0
        t0=int(round(time.time() * 1000))
        while (True):
            acc_value = bus.read_i2c_block_data(BMI160_DEVICE_ADDRESS, BMI160_USER_DATA_14_ADDR, 6)
            acc_value_2 = bus.read_i2c_block_data(BMI160_DEVICE_ADDRESS_2, BMI160_USER_DATA_14_ADDR, 6)
            gyro_value = bus.read_i2c_block_data(BMI160_DEVICE_ADDRESS, BMI160_USER_DATA_8_ADDR, 6)
            gyro_value_2 = bus.read_i2c_block_data(BMI160_DEVICE_ADDRESS_2, BMI160_USER_DATA_8_ADDR, 6)

            #print "0x%X, 0x%X 0x%X" % ( acc_value[0], acc_value[1], acc_value[2])  
            #print "0x%X, 0x%X 0x%X" % ( acc_value[3], acc_value[4], acc_value[5])  
            ax =  (acc_value[1] << 8) | acc_value[0]
            ay =  (acc_value[3] << 8) | acc_value[2]
            az =  (acc_value[5] << 8) | acc_value[4]
            gx =  (gyro_value[1] << 8) | gyro_value[0]
            gy =  (gyro_value[3] << 8) | gyro_value[2]
            gz =  (gyro_value[5] << 8) | gyro_value[4]
            ax_2 =  (acc_value_2[1] << 8) | acc_value_2[0]
            ay_2 =  (acc_value_2[3] << 8) | acc_value_2[2]
            az_2 =  (acc_value_2[5] << 8) | acc_value_2[4]
            gx_2 =  (gyro_value_2[1] << 8) | gyro_value_2[0]
            gy_2 =  (gyro_value_2[3] << 8) | gyro_value_2[2]
            gz_2 =  (gyro_value_2[5] << 8) | gyro_value_2[4]


            data=[ax,ay,az,gx,gy,gz,ax_2,ay_2,az_2,gx_2,gy_2,gz_2]
            t=[int(round(time.time() * 1000))-t0]
           
            #stream.write({'x':t[0],'y':ax})
            #stream_2.write({'x':t[0],'y':ax_2})
            #if z==0:
            #    x=t[0]
            #    y=ax
            #    points=axs.plot(x,y,'o')[0]
            #    z=1
            #
            #points.set_data(x,y)
            #fig.canvas.restore_region(background)
            #plt.draw()
            #axs.draw_artist(points)
            #fig.canvas.blit(axs.box)

            print(t+data)
            writer.writerow(t+data)
            csvfile.flush()
            i=i+1
        #plt.close(fig)
        


if sys.argv[1] == "A" :
    while True:
        enable_accel( )

elif sys.argv[1] == "G" :
  enable_gyro( )

else:
    enable_both( );

sys.exit()
