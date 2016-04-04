import sys
sys.path.append("/home/pi/Python/PiClasses")
import InfoBeamer

ibVideo = InfoBeamer.InfoBeamer("/media/usb0/ShilohLoop")

#dbConn.logBoot()

#numTimesToRepeat = 5
#while True:
#    dbConn.logHeartbeat()
#    numTimesToRepeat -= 1
#    if numTimesToRepeat==0:
#        break
#    else:
#        time.sleep(5)

#dbConn.logAccess(55555)



print "done"
