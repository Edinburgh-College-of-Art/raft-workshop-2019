# Simple Adafruit BNO055 sensor reading example.  Will print the orientation
# and calibration data every second.
#
# Copyright (c) 2015 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import logging
import sys

import time
import argparse
import Adafruit_BNO055

from Adafruit_BNO055 import BNO055
from pythonosc import udp_client
from pythonosc import osc_message_builder

# Parse command line arguments
parser = argparse.ArgumentParser()

parser.add_argument('--ip', type=str, help="IP address of the OSC server")
parser.add_argument('--port', type=int, help="Port OSC server is listening on")

args = parser.parse_args()

# This is the IP and port of your Pure Data instance
PD_IP = "127.0.0.1"
if args.ip is not None:
    PD_IP = args.ip
PD_PORT = 8000
if args.port is not None:
    PD_PORT = args.port

# This can be set to whatever you like and will be the address the OSC message
# is sent with
OSC_ADDR = "/compass"

# Create and configure the BNO sensor connection.  Make sure only ONE of the
# below 'bno = ...' lines is uncommented:
# Raspberry Pi configuration with serial UART and RST connected to GPIO 17:
bno = BNO055.BNO055(serial_port='/dev/ttyS0', rst=17)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

##bno055 = Adafruit_BNO055.BNO055()
client = udp_client.SimpleUDPClient(PD_IP, PD_PORT)

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))
print('Reading BNO055 data, press Ctrl-C to quit...')

def send_readings_to_pd(heading, roll, pitch, x_acc, y_acc, z_acc):
    """ Sends BNO055 readings to PD
        
        In the order heading, roll, pitch, x_acc, y_acc, z_acc
        """
    msg = osc_message_builder.OscMessageBuilder(address=OSC_ADDR)
    
    msg.add_arg(heading, arg_type="f")
    msg.add_arg(roll, arg_type="f")
    msg.add_arg(pitch, arg_type="f")
    msg.add_arg(x_acc, arg_type="f")
    msg.add_arg(y_acc, arg_type="f")
    msg.add_arg(z_acc, arg_type="f")
    client.send_message(OSC_ADDR, msg.build())

while True:
    heading, roll, pitch = bno.read_euler()
    x_acc,y_acc,z_acc = bno.read_linear_acceleration()
    send_readings_to_pd(heading, roll, pitch, x_acc, y_acc, z_acc)
    
    # Wait .075 seconds and repeat.
    time.sleep(0.075)


#while True:
#    # Read the Euler angles for heading, roll, pitch (all in degrees).
#    
#    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
#    sys, gyro, accel, mag = bno.get_calibration_status()
#    # Other values you can optionally read:
#    # Orientation as a quaternion:
#    #x,y,z,w = bno.read_quaterion()
#    # Sensor temperature in degrees Celsius:
#    temp_c = bno.read_temp()
#    # Magnetometer data (in micro-Teslas):
#    # x,y,z = bno.read_magnetometer()
#    # Gyroscope data (in degrees per second):
#    # x,y,z = bno.read_gyroscope()
#    # Accelerometer data (in meters per second squared):
#    #x,y,z = bno.read_accelerometer()
#    # Linear acceleration data (i.e. acceleration from movement, not gravity--
#    # returned in meters per second squared):
#    x_acc,y_acc,z_acc = bno.read_linear_acceleration()
#    # Gravity acceleration data (i.e. acceleration just from gravity--returned
#    # in meters per second squared):
#    # x,y,z = bno.read_gravity()
#
#    # Print everything out.
#    print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
#          heading, roll, pitch, sys, gyro, accel, mag))
#    # Sleep for a 10th of a second until the next reading.
#time.sleep(0.09)
