import serial, time

class MotorControl:
    def __init__(self, motorid='BD16'):
        self.ser = serial.Serial('/dev/ttyUSB0')
        self.controller = motorid

    def turn(self, direction):
        if direction == 'clockwise':
            self.ser.write(self.controller + '\r')
            self.ser.write('H+\r')
        elif direction == 'counterclockwise':
            self.ser.write(self.controller + '\r')
            self.ser.write('H-\r')
        else:
            return "Incorrect Paramter. Valid options are 'Clockwise' and 'Counterclockwise'"

    def stop(self):
        self.ser.write(self.controller + '\r')
        self.ser.write('H0\r')

    def speed(self, speed=2000):
        if 200 <= speed <= 65535:
            self.ser.write(self.controller + '\r')
            self.ser.write('SD'+str(speed)+'\r')
        else:
            return "Speed Value Incorrect: "+ str(speed)

    def home(self, homePin=5, direction='cw'):
        if 1 <= homePin <= 10 and direction == 'cw' or direction == 'ccw':
            self.ser.write(self.controller + '\r')
            if direction == 'cw':
                self.ser.write('TC' + str(homePin) + '\r')
                self.ser.write('H+\r')
            else:
                self.ser.write('TC' + str(homePin) + '\r')
                self.ser.write('H-\r')

            #Check to see if we've stopped moving
            pos = None
            while True:
                self.ser.write('RC\r')
                newPos = self.ser.readline()
                print "Position: " + newPos
                if pos == newPos:
                    print "Motor Stopped. Exiting"
                    break
                else:
                    pos = newPos
                time.sleep(.5)

            # Write the position as the new home
            print "Setting home"
            self.ser.write('HM0\r')
        else:
            return "Inappropriate value for home pin or direction. "
        return

    def setAccel(self, speed=100):
        self.ser.write(self.controller + '\r')
        return

    def moveAbs(self, location=20):
        self.ser.write(self.controller + '\r')
        time.sleep(.01)
        self.ser.write('MI' + str(location) + '\r')

    def moveRelative(self, location=20):
        self.ser.write(self.controller + '\r')
        self.ser.write('II' + str(location) + '\r')

    def getPosition(self):
        self.ser.write(self.controller + '\r')
        time.sleep(.01)
        self.ser.write('RC\r')
        line = self.ser.readline()
        print "Position: " + line

    def pinOn(self, pinNum):
        self.ser.write(self.controller + '\r')
        time.sleep(.01)
        self.ser.write('PS' + str(pinNum) + '\r')

    def pinOff(self, pinNum):
        self.ser.write(self.controller + '\r')
        time.sleep(.01)
        self.ser.write('PC' + str(pinNum) + '\r')