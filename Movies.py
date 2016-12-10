__author__ = 'shilohmadsen'
#This file sends the UDP commands to localhost to trigger the play movie
import socket
import subprocess
import os

blackhole = open(os.devnull, 'w')

def PlayMovie ():
    #print ("playing movie")

    UDP_IP = "localhost"
    UDP_PORT = 4444
    MESSAGE = "looper/play:intermission.mp4"

    sock = socket.socket(socket.AF_INET, # Internet
                 socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    os.system('stty sane')
    #print "done playing movie"
    return

def StartLoop(LoopPath):
    subprocess.Popen(['sudo', '/home/pi/info-beamer-pi/info-beamer', LoopPath], stdout=blackhole)
    #print "Starting Movie Loop"
    return

def StopLoop():
    subprocess.Popen(['sudo' ,'pkill', 'info-beamer'])
    #print "Starting Movie Loop"
    return

def PlayLoop ():
    UDP_IP = "localhost"
    UDP_PORT = 4444
    MESSAGE = "looper/loop:"

    sock = socket.socket(socket.AF_INET, # Internet
                 socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    os.system('stty sane')
    return