import sys

sys.path.insert(0, '/home/pi/Python')
import glob, os, random, subprocess, Logger, logging, serial, time, socket

# Add Logging Code
script = os.path.basename(__file__)
stdout_logger = logging.getLogger(script + '_Out')
sl = Logger.StreamToLogger(stdout_logger, logging.INFO)
sys.stdout = sl  # For Headless Operations

stderr_logger = logging.getLogger(script + '_Err')
sl = Logger.StreamToLogger(stderr_logger, logging.ERROR)
sys.stderr = sl

# Setup Serial - This may be the wrong USB port
shutterOutput = serial.Serial('/dev/ttyUSB0', 115200)
knockInput = serial.Serial('/dev/ttyUSB1', 115200)


# Define good and bad videos
PassVideo = glob.glob(os.path.join('/home/pi/Python/2018/Assets/PassVids', '*.mp4'))
FailVideo = glob.glob(os.path.join('/home/pi/Python/2018/Assets/FailVids', '*.mp4'))

# Video Times
VideoTiming = {
    '/home/pi/Python/2018/Assets/PassVids/BC_PeepHole_Pos01_ComeOnIn_v1.mp4': 14,
    '/home/pi/Python/2018/Assets/PassVids/BC_PeepHole_Pos02_RightKnock_v1.mp4': 16,
    '/home/pi/Python/2018/Assets/PassVids/BC_PeepHole_Pos03_OhItsYou_v1.mp4': 16,
    '/home/pi/Python/2018/Assets/PassVids/BC_PeepHole_Pos04_NeverMakeIt_v1.mp4': 16,
    '/home/pi/Python/2018/Assets/PassVids/BC_PeepHole_Neg06_QuitKnockin_v1.mp4': 12,
    '/home/pi/Python/2018/Assets/FailVids/BC_PeepHole_Neg01_LookingLikeThat_v1.mp4': 15,
    '/home/pi/Python/2018/Assets/FailVids/BC_PeepHole_Neg02_WhoIsIt_v1.mp4': 11,
    '/home/pi/Python/2018/Assets/FailVids/BC_PeepHole_Neg03_BuggerOff_v1.mp4': 13,
    '/home/pi/Python/2018/Assets/FailVids/BC_PeepHole_Neg04_DontWantNone_v1.mp4': 13,
    '/home/pi/Python/2018/Assets/FailVids/BC_PeepHole_Neg05_NonVerbal_v1.mp4': 13
}

# UDP ports for sending to "Windows"
UDP_IP = ["192.168.200.179", "192.168.200.245", "192.168.200.147"]
UDP_PORT = 5005
MESSAGE = "Hello, World!"


def ProcessKnock(status):
    # Play Video
    if status == "PASS":
        stdout_logger.info("Activation||1")
        video = random.choice(PassVideo)
    elif status == "FAIL":
        stdout_logger.info("Activation||2")
        video = random.choice(FailVideo)
    elif status == "TWO BITS":
        stdout_logger.info("Activation||3")
    else:
        stdout_logger.info("Activation||4")
        print "Unhandled status"
        return

    try:
        print video
        sleepTime = VideoTiming[video] - 6
    except KeyError:
        sleepTime = 10

    try:
        player = subprocess.Popen(['omxplayer', '-b', video])
    except subprocess.CalledProcessError:
        print "Problem calling Subprocess"

    time.sleep(2)

    # Open Shutter
    for i in range(3):
        shutterOutput.write("O")

    print sleepTime
    time.sleep(sleepTime)

    # Close Shutter
    for i in range(3):
        shutterOutput.write("C")

    if status == "PASS":
        # Send code to play video in all windows if pass
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for IP in UDP_IP:
            sock.sendto("1", (IP, UDP_PORT))

# Nonstop loop listening for serial input
while True:
    data = knockInput.readline()
    if data:
        print data
        # Proccess Good Knock
        if (data == 'PASS\r\n'):
            ProcessKnock("PASS")
            data = ''
            knockInput.flushInput()
            time.sleep(3)

        #  Process Bad Knock
        if (data == 'FAIL\r\n'):
            ProcessKnock("FAIL")
            knockInput.flushInput()
            time.sleep(3)

        else:
            # Placeholder in case we want to act on lines that arent PASS/Fail
            pass

