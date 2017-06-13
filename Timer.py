__author__ = 'madsens'
import Movies
import datetime
import time
import os

#Swaps the day/night process based on time of day.
while True:
    now = datetime.datetime.now()
    now_time = now.time()
    #If between 6AM and 5PM, Play Daytime
    if datetime.time(6,00) <= now.time() <= datetime.time(12,00):
        print "Its Daytime"
        Movies.StopLoop()
        time.sleep(2)
        Movies.StartLoop('/home/pi/Python/Assets/DayLoop')
    else:
        print "Its Night Time"
        Movies.StopLoop()
        time.sleep(2)
        Movies.StartLoop('/home/pi/Python/Assets/NightLoop')

    print "Sleeping for one hour"
    time.sleep(3600)