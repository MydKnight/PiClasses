import sys
sys.path.append("/home/pi/PiClasses")
import Logging
import time

dbConn = Logging.Logging()
dbConn.logBoot()

while True:
    dbConn.logHeartbeat()
    time.sleep(3600)
