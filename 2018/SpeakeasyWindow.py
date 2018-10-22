import sys

sys.path.insert(0, '/home/pi/Python')
import time, sys, os, Logger, logging, socket, fcntl, struct, Movies

# Add Logging Code
script = os.path.basename(__file__)
stdout_logger = logging.getLogger(script + '_Out')
sl = Logger.StreamToLogger(stdout_logger, logging.INFO)
sys.stdout = sl  # For Headless Operations

stderr_logger = logging.getLogger(script + '_Err')
sl = Logger.StreamToLogger(stderr_logger, logging.ERROR)
sys.stderr = sl

# Log Bootup
stdout_logger.info("Bootup")


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15]))[20:24])


# Setup UDP listener
UDP_IP = str(get_ip_address('wlan0'))
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

# Start Movie Loop
Movies.StartLoop('/home/pi/Python/2018/Assets')

# Listen for Scan
while True:  # Runs until break is encountered. We want to set it to break on a particular ID.
    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
    if data == "1":
        # Play Movie
        Movies.PlayMovie()
        time.sleep(8)

        Movies.PlayLoop()

    else:
        time.sleep(7)
    print "received message:", data
