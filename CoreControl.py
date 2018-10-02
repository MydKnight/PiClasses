#!/usr/bin/python
__author__ = 'madsens'
# Hall of Fame gag. Will run laser show, 10 DJ lights and play sound.

import socket, sys, time
sys.path.append("/home/pi/PiClasses")
import Logging, GPIOLib
from DmxPy import DmxPy
from random import randint

# DMX Control Initilaization. Move to Main method?
dmx = DmxPy('/dev/ttyUSB0')

# Test Module for listening for serial communication
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 9988))
s.listen(1)

def standby():
    # Set Baseline
    for x in [1, 2, 4, 5, 6, 7, 8, 11, 12, 14, 15, 16, 17, 18, 21, 22, 24, 25, 26, 27, 28]:
        dmx.setChannel(x, 0)
    for x in [7, 17, 27]:
        dmx.setChannel(x, 255)
    dmx.render()

    # Fade up to blue from nothing
    for x in range(0, 255):
        for y in [3, 13, 23]:
            dmx.setChannel(y, x)
            dmx.render()
            time.sleep(.01)

    # Begin to pulse
    dmx.setChannel(8, 157)
    dmx.setChannel(18, 158)
    dmx.setChannel(28, 159)
    dmx.render()

while True:
    standby()
    conn, addr = s.accept()
    data = conn.recv(1024)
    conn.close()
    print data