#!/usr/bin/python
__author__ = 'madsens'
# Hall of Fame gag. Will run laser show, 10 DJ lights and play sound.

import time, sys, os
sys.path.append("/home/pi/PiClasses")
import Logging, GPIOLib
from termios import tcflush, TCIOFLUSH
from DmxPy import DmxPy
from random import randint

#Instantiate Logging and DMX Classes
dbConn = Logging.Logging()
dmx = DmxPy('/dev/ttyUSB0')

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else :
        dbConn.logAccess(n)

        #Play Music File
        os.system('mpg321 /home/pi/Python/Assets/christmas.mp3 -q &')

        # Turn On Projectors
        dmx.setChannel(2,255)
        dmx.render()

        # Blink Lights
        count = 0
        while (count < 28):
            dmx.setChannel(1, 255)
            dmx.render()
            time.sleep(.5)
            dmx.setChannel(1, 0)
            dmx.render()
            time.sleep(.5)
            count = count + 1

        # Return Lights to normal. Turn off Projectors
        dmx.setChannel(2,0)
        dmx.setChannel(1,255)
        dmx.render()

        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)


