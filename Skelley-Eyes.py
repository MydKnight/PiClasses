__author__ = 'madsens'
# Skeleton Eyes. Simply loops a single eyeball video for output to two screens in front of castle

import sys
sys.path.append("/home/pi/PiClasses")
import Logging
import os
import Movies
import time

dbConn = Logging.Logging()
Movies.StartLoop('/home/pi/Assets')

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    #Logging.HeartBeat()
    n = raw_input("Scanned ID: ")
    if n == "STOP":
        Movies.StopLoop()
        break  # stops the loop
    else :
        dbConn.logAccess(n)