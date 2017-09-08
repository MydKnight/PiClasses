__author__ = 'madsens'
import sys
sys.path.append("/home/pi/PiClasses")
import Logging
import os
import Movies
import time
from termios import tcflush, TCIOFLUSH

dbConn = Logging.Logging()
dbConn.logBoot()

Movies.StartLoop('/home/pi/Assets')

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    # Logging.HeartBeat()
    n = raw_input("Scanned ID: ")
    if n == "STOP":
        Movies.StopLoop()
        #print "Stopping."
        break  # stops the loop
    else :
        # We're only logging access if there is a connection to the DB. if not, we dont do this.
        # if dbConn:
            #dbConn.logAccess(n)

        time.sleep(.5)

        # print "Playing."
        Movies.PlayMovie()
        time.sleep(25)

        Movies.PlayLoop()

        # flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)