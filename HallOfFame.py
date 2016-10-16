#!/usr/bin/python
__author__ = 'madsens'
# Hall of Fame gag. Will run laser show, 10 DJ lights and play sound.

import time, sys, os
sys.path.append("/home/pi/PiClasses")
import Logging
from termios import tcflush, TCIOFLUSH
from DmxPy import DmxPy

#Instantiate Logging and DMX Classes
dbConn = Logging.Logging()
dmx = DmxPy('/dev/ttyUSB0')

dmx.setChannel(6, 255)
dmx.setChannel(7, 255)
dmx.setChannel(8, 159)
dmx.setChannel(10, 40)
dmx.render()

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else :
        dbConn.logAccess(n)



        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)