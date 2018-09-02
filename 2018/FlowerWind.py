import sys

sys.path.insert(0, '/home/pi/Python')
import GPIOLib, time

# We're doing multiple things now. Pepper Flip = 11, Blue Light = 13, Fan = 15, Air Blast = 7
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [11])


# Add Logging Code

def FlutterFan(seconds):
    '''
    Simulate a PWM by pulsing the GPIO pin on and off for the number of seconds passed in
    @param seconds: Number of seconds to pulse
    @return: void
    '''
    for s in range(seconds):
        for i in range(2):
            gpio.on([11])
            time.sleep(.05)
            gpio.off([11])
            time.sleep(.5)


# Listen for Scan
while True:  # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else:
        # Trigger Sound Play

        # Trigger Fan Blow
        FlutterFan(2)

# Flutter GPIO 17

# Play Sound
