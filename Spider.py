#!/usr/bin/python
__author__ = 'madsens'
# Runs the RFID Tester in the lobby. When triggered spins a wheel with sounds.

import time, sys, os
sys.path.append("/home/pi/PiClasses")
import Logging
import GPIOLib
from termios import tcflush, TCIOFLUSH
from random import randint

# Instantiate Logging and GPIO Classes (11 - power drill, 13 - Change Polarity)
dbConn = Logging.Logging()
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [11])

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else :
        dbConn.logAccess(n)

        # Play Wraith on even n, Wilhelm on odd n
        if (int(n) % 2 == 0):
            audio = "/home/pi/Assets/wraith.mp3"
        else:
            audio = "/home/pi/Assets/wilhelm.mp3"

        # Trigger GPIO Pins. Need to make a random number of "pulses" with a random number of "micro-pulses" each with a random duration pulse, flipping the "polarity pin" with each micro pulse
        # Play an mp3 during each "pulse"
        pulses = randint(1,4)
        for x in range (0, pulses):
            os.system('mpg321 ' + audio + ' -q &')
            #Micropulses also random between 4 and 10
            micropulse = randint(6,10)
            for y in range (0, micropulse):
                gpio.on([11])
                time.sleep(.15)
                gpio.off([11])
                time.sleep(.1)

            time.sleep(2)

        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)