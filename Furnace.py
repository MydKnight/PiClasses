__author__ = 'madsens'
import sys
sys.path.append("/home/pi/PiClasses")
import Logging
import os
import Movies
import time
from termios import tcflush, TCIOFLUSH

dbConn = Logging.Logging()
Movies.StartLoop('/media/usb0/Assets')

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    #Logging.HeartBeat()
    n = raw_input("Scanned ID: ")
    if n == "STOP":
        Movies.StopLoop()
        #print "Stopping."
        break  # stops the loop
    else :
        dbConn.logAccess(n)

        # On Input, Disable Reader
        os.system("/home/pi/Python/Scripts/disableRFID.sh")
        print "Playing."
        Movies.PlayMovie()
        time.sleep(6
                   )
        # Reenable reader.
        os.system("/home/pi/Python/Scripts/enableRFID.sh")
        Movies.PlayLoop()

        # flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)