#!/usr/bin/env python
#
# This is the code for Grove - Ultrasonic Ranger
# (https://www.seeedstudio.com/Grove-Ultrasonic-Ranger-p-960.html)
# which is a non-contact distance measurement module which works with 40KHz sound wave.
#
# This is the library for Grove Base Hat which used to connect grove sensors for raspberry pi.

# However, in the absence of a Grove Base Hat, raft workshop has hacked this code to force the sensor to connect to the GPIO pin # 5
# we have added some functionality enabling the sensor to pass its data to other applications across the network using OSC.
# Give the script an argument --ip to specify the IP address you want to send the data to, --port allows you to specify the port
# 
#-------------------------------------------------------------------------------
'''
    ## License
    
    The MIT License (MIT)
    
    Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
    Copyright (C) 2018  Seeed Technology Co.,Ltd.
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
    '''
#-------------------------------------------------------------------------------
import sys
import time
import argparse
from grove.gpio import GPIO
from pythonosc import udp_client
from pythonosc import osc_message_builder
#-------------------------------------------------------------------------------

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
OSC_ADDR = "/ranger"

# Create objects used to communicate with remote OSC server
client = udp_client.SimpleUDPClient(PD_IP, PD_PORT)

#----------------------------------------------------------------------------------
def send_readings_to_pd(range):
    """ Sends compass, accelerometer and heading readings to PD
        
        In the order range
        """
    msg = osc_message_builder.OscMessageBuilder(address=OSC_ADDR)
        
    msg.add_arg(range, arg_type="f")
    
    client.send_message(OSC_ADDR, msg.build())
#-------------------------------------------------------------------------------------

usleep = lambda x: time.sleep(x / 1000000.0)

_TIMEOUT1 = 1000
_TIMEOUT2 = 10000

class GroveUltrasonicRanger(object):
    def __init__(self, pin):
        self.dio = GPIO(pin)
    
    def _get_distance(self):
        self.dio.dir(GPIO.OUT)
        self.dio.write(0)
        usleep(2)
        self.dio.write(1)
        usleep(10)
        self.dio.write(0)
        
        self.dio.dir(GPIO.IN)
        
        t0 = time.time()
        count = 0
        while count < _TIMEOUT1:
            if self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT1:
            return None
        
        t1 = time.time()
        count = 0
        while count < _TIMEOUT2:
            if not self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT2:
            return None
    
        t2 = time.time()
        
        dt = int((t1 - t0) * 1000000)
        if dt > 530:
            return None

        distance = ((t2 - t1) * 1000000 / 29 / 2)    # cm
    
        return distance
    
    def get_distance(self):
        while True:
            dist = self._get_distance()
            if dist:
                return dist

Grove = GroveUltrasonicRanger
#-------------------------------------------------------------------------------
def main():
    print("Plug sensor into pin 5\n")
    pin = 5
    sonar = GroveUltrasonicRanger(pin)
    
    print('Detecting distance...')
    while True:
        range = (sonar.get_distance())
        print('{} cm'.format(sonar.get_distance())) # you can comment out this line when you're happy that you're getting your data in PD
        send_readings_to_pd(range)
        time.sleep(0.075)
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
