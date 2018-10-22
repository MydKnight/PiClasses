import sys

sys.path.insert(0, '/home/pi/Python')
import os, Logger, logging, serial, time, socket, struct, fcntl

# Add Logging Code
script = os.path.basename(__file__)
stdout_logger = logging.getLogger(script + '_Out')
sl = Logger.StreamToLogger(stdout_logger, logging.INFO)
# sys.stdout = sl #For Headless Operations

stderr_logger = logging.getLogger(script + '_Err')
sl = Logger.StreamToLogger(stderr_logger, logging.ERROR)
# sys.stderr = sl

# Setup Serial
oujaComm = serial.Serial('/dev/ttyACM0', 115200)


# Set up UDP Listener
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15]))[20:24])


UDP_IP = str(get_ip_address('wlan0'))
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

# Nonstop loop listening for serial input
while True:
    data = raw_input("Scanned ID: ")

    if data:
        # Lookup User

        # Construct Phrase/Select from list

        # Send Message to Aurduino
        oujaComm.write(data)

        # Our movement is slow. Timeout of 30 seconds
        time.sleep(30)

    else:
        print "bad data recieved"
