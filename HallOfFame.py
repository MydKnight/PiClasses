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
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [11,13])

def standBy():
    offset = 0

    for x in range(1, 10):
        rndRed = randint(4, 255)
        rndGreen = randint(4, 255)
        rndBlue = randint(4, 255)
        dmx.setChannel(1 + offset, rndRed)
        dmx.setChannel(2 + offset, rndGreen)
        dmx.setChannel(3 + offset, rndBlue)
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
    time.sleep(.1)
    gpio.off([11])
    time.sleep(2)

    #Play Music
    if (n == '0006701791' or n == '0005785109'):
        # Play Dead Man's party to make Shiloh Happy
        print "Shiloh"
        os.system('mpg321 /home/pi/Assets/deadmansparty-live.mp3 -q &')
        timer = 250
    else:
        print "Standard"
        os.system('mpg321 /home/pi/Assets/audio1.mp3 -q &')
        timer = 14

    for x in range (0, timer):
        offset = 0
        for x in range (1,10):
            rndColor = randint(4,255)

            dmx.setChannel(8+offset, 159)
            dmx.setChannel(7+offset, 255)
            dmx.setChannel(9 + offset, rndColor)

            offset += 20

        dmx.render()
        time.sleep(1)

    # Projector Off
    gpio.on([13])
    time.sleep(.1)
    gpio.off([13])
    time.sleep(.1)

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


