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

# GPIO to trigger power to the Projector
gpio = GPIOLib.GPIOLib("BOARD", "HIGH", [11])

def standBy():
    offset = 0
    for x in range(1, 10):
        rndColor = randint(4, 255)
        dmx.setChannel(4 + offset, 204)
        dmx.setChannel(5 + offset, 64)
        dmx.setChannel(7 + offset, 127)
        dmx.setChannel(8 + offset, 0)
        dmx.setChannel(9 + offset, 0)
        dmx.setChannel(10 + offset, 0)

        offset += 20

    dmx.render()
    return

def disco():
    # Turn on the Projector
    gpio.on([11])
    time.sleep(5)

    #Play Music
    if (n == '0005784121'):
        # Play My Sharona Sound - If shiloh scans
        os.system('mpg321 -k 1600 /home/pi/Python/EasterEgg/deadmansparty-live.mp3 -q &')
        timer = 500
    else:
        os.system('mpg321 /media/usb0/Assets/audio1.mp3 -q &')
        timer = 28

    for x in range (0, timer):
        offset = 0
        for x in range (1,10):
            rndColor = randint(4,255)

            dmx.setChannel(8+offset, 222)
            dmx.setChannel(7+offset, 255)
            dmx.setChannel(9 + offset, rndColor)

            offset += 20

        dmx.render()
        time.sleep(.5)

    # Projector Off
    gpio.off([11])
    return

standBy()

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else :
        dbConn.logAccess(n)

        disco()
        standBy()

        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)


