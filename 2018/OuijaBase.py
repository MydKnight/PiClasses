import sys

sys.path.insert(0, '/home/pi/Python')
import sys, os, Logger, logging, databaseLib, socket, random, time
from termios import tcflush, TCIOFLUSH

# Add Logging Code
script = os.path.basename(__file__)
stdout_logger = logging.getLogger(script + '_Out')
sl = Logger.StreamToLogger(stdout_logger, logging.INFO)
# sys.stdout = sl #For Headless Operations

stderr_logger = logging.getLogger(script + '_Err')
sl = Logger.StreamToLogger(stderr_logger, logging.ERROR)
# sys.stderr = sl

# Log Bootup
stdout_logger.info("Bootup")

conn = databaseLib.DBConn()

# UDP ports for sending to "OuijaRemote"
UDP_IP = ["192.168.40.45"]
UDP_PORT = 5005
MESSAGE = "Hello, World!"

NamedPhrases = [
    "%s did it",
    "%s dies tonight",
    "where were you last night, %s"
    "%s knows who killed him",
    "behind you %s",
    "Boo %s"
]

AnonPhrases = [
    "Welcome to the Castle",
    "He knows"
    "She knows"
    "Tip the bartender",
    "Ben did it",
    "Erin did it",
    "Marisol did it",
    "Josh did it",
    "We know you know",
    "Youre next"
]


def processDoubleLetter(phrase):
    prevLetter = ''
    newPhrase = ''
    for letter in phrase:
        if letter == prevLetter:
            newPhrase += '#'
        else:
            newPhrase += letter
        prevLetter = letter
    return newPhrase


def processSpaces(phrase):
    newPhrase = ''
    for letter in phrase:
        if letter == ' ':
            newPhrase += '.'
        else:
            newPhrase += letter
    return newPhrase


# Listen for Scan
while True:  # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else:
        stdout_logger.info("Activation||" + n)
        # Lookup User
        try:
            res = conn.cursor.execute("SELECT FirstName FROM Members WHERE RFID = %s" % (int(n)))
            fName = conn.cursor.fetchone()
        except:
            stderr_logger.log(logging.ERROR, "No Connection to DB.")

        # Construct Phrase/Select from list
        if fName is not None:
            message = random.choice(NamedPhrases)
            message = (message % (fName))
        else:
            message = random.choice(AnonPhrases)

        # Run phrase through processing functions (handle double letters, insert space commands in place of actual spaces.
        message = processSpaces(message)
        message = processDoubleLetter(message)

        print (message)

        # Send Message to Ouija-Remote
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message, (UDP_IP, UDP_PORT))

        # Wait for response from remote
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        while True:
            if data:
                break
            else:
                print "Waiting..."
                time.sleep(1)

        # flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)
