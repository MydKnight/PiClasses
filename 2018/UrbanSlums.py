import datetime
import sys
import vlc

sys.path.insert(0, '/home/pi/Python')
import sys, os, Logger, logging

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

# Play audio on loop
player = vlc.MediaPlayer("/home/pi/Python/2018/Assets/slums.mp3")
player.play()

# No Scan for this gag. Run if between 4pm and 2am
while True:  # Runs until break is encountered. We want to set it to break on a particular ID.
    currentDT = datetime.datetime.now()
    if currentDT.hour >= 16 or 0 <= currentDT.hour <= 2:
        print
        # Higher volume from 7pm til Midnight
        if 19 <= currentDT.hour <= 24:
            player.audio_set_volume(100)
        else:
            player.audio_set_volume(50)

        # If Audio ended. Restart.
        if player.get_state() == vlc.State.Ended:
            player = vlc.MediaPlayer("/home/pi/Python/2018/Assets/slums.mp3")
            player.play()
    else:
        player.stop()
