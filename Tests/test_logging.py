import sys
sys.path.append("/home/pi/PiClasses")
import Logging
import time

dbConn = Logging.Logging()

#dbConn.logBoot()

#numTimesToRepeat = 5
while True:
    #dbConn.logHeartbeat()
    #numTimesToRepeat -= 1
    #if numTimesToRepeat==0:
    #    break
    #else:
    dbConn.getAccess(3333)