__author__ = 'madsens'
import subprocess

class InfoBeamer:
    'Common base class for all Video Loops'
    # <editor-fold desc="Global Variables">
    UDP_IP = "localhost"
    UDP_PORT = 4444
    # </editor-fold>

    def __init__(self, LoopPath):
        '''
        :return:
        '''
        #Attempt to Play the movie at the refrenced endpoint
        try:
            subprocess.Popen(['sudo', '/home/pi/info-beamer-pi/info-beamer', LoopPath])
            print "Starting Movie Loop"
            return
        #If Playing fails, throw exception
        except Exception as e:
            print "Error: %s" %e