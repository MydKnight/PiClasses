import glob
import os
import random
import subprocess

import serial

# Need Logging Code input Still

# Setup Serial - This may be the wrong USB port
serInput = serial.Serial('/dev/ttyUSB0', 115200)

# Define good and bad videos
PassVideo = glob.glob(os.path.join('/home/pi/Python/2018/Assets/PassVids', '*.mp4'))
FailVideo = glob.glob(os.path.join('/home/pi/Python/2018/Assets/FailVids', '*.mp4'))

# Nonstop loop listening for serial input
while True:
    data = serInput.readline()
    if data:
        # Proccess Good Knock
        if (data == 'PASS\r\n'):
            try:
                player = subprocess.Popen(['omxplayer', '-b', random.choice(PassVideo)])
                player.wait()
                data = ''
            except subprocess.CalledProcessError:
                print "Problem calling Subprocess"
            data = ''

        #  Process Bad Knock
        if (data == 'FAIL\r\n'):
            player = subprocess.Popen(['omxplayer', '-b', random.choice(FailVideo)])
            player.wait()
            data = ''

        else:
            # Placeholder in case we want to act on lines that arent PASS/Fail
            pass
