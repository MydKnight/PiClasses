__author__ = 'madsens'
import Movies
import datetime
import time
import os

print 'Starting'
Movies.StartLoop('/home/pi/Python/Assets/Day')
time.sleep(5)

while True:
    now = datetime.datetime.now()
    now_time = now.time()
    #If between 6AM and 5PM, Play Daytime
    if datetime.time(6,00) <= now.time() <= datetime.time(11,00):
        print "Its Daytime"
        Movies.StopLoop()
        time.sleep(2)
        Movies.StartLoop('/home/pi/Python/Assets/Day')
    else:
        print "Its Night Time"
        Movies.StopLoop()
        time.sleep(2)
        Movies.StartLoop('/home/pi/Python/Assets/Night')
        while True:
            n = raw_input("Scanned ID: ")
            if n == "STOP":
                Movies.StopLoop()
                break  # stops the loop
            else :
                print "You typed: ", n
                #Log Activation of PI - Disabled until we're configured on the castle network
                #Logging.LogAccess(n)

                #Turn off the reader until function finishes.
                os.system("/home/pi/Python/Scripts/disableRFID.sh")

                #Play Furnace Video - Test
                Movies.PlayMovie()

                time.sleep(20)

                #Turn the reader back on.
                os.system("/home/pi/Python/Scripts/enableRFID.sh")
    print "Sleeping for one hour"
    time.sleep(3600)