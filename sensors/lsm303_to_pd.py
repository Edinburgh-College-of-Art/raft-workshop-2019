""" Python file to demonstrate reading the LSM303 and pass data to Pure Data

    Author: Cameron MacLeod
    Date: 2018/03/17
    Contact: github.com/notexactlyawe
"""
import time
import argparse
import Adafruit_LSM303

from math import atan2, pi

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
OSC_ADDR = "/readings"

# Create objects used to read LSM303 and communicate with remote OSC server
lsm303 = Adafruit_LSM303.LSM303()
client = udp_client.SimpleUDPClient(PD_IP, PD_PORT)

def compute_heading(mag_read):
    """ Computes the compass heading from the magnetometer X and Y.

        Returns a float in degrees between 0 and 360.
    """
    return ((atan2(mag_read[1], mag_read[0]) * 180) / pi) + 180

# was (atan2(mag_read[0], mag_read[1]) * 180) / pi + 180 added brackets (unesc.) and swapped inputs to arcTan2.

def send_readings_to_pd(accel, mag, heading):
    """ Sends compass, accelerometer and heading readings to PD

        In the order acc_x, acc_y, acc_z, mag_x, mag_y, mag_z, heading
    """
    msg = osc_message_builder.OscMessageBuilder(address=OSC_ADDR)

    msg.add_arg(accel[0], arg_type="i")
    msg.add_arg(accel[1], arg_type="i")
    msg.add_arg(accel[2], arg_type="i")
    msg.add_arg(mag[0], arg_type="i")
    msg.add_arg(mag[1], arg_type="i")
    msg.add_arg(mag[2], arg_type="i")
    msg.add_arg(heading, arg_type="f")

    client.send_message(OSC_ADDR, msg.build())

while True:
    accel, mag = lsm303.read()
    heading = compute_heading(mag)

    send_readings_to_pd(accel, mag, heading)

    # Wait .075 seconds and repeat.
    time.sleep(0.05)
        