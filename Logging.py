__author__ = 'madsens'

import MySQLdb
from uuid import getnode as get_mac
import socket
#TODO: fcntl doesnt work on windows. Reenable when testing on PI
#import fcntl
import struct
import datetime
import sys

#TODO: Times are off on the logging table. Test log times are accurately reflected.

class Logging:
    'Common base class for all Logs'
    # <editor-fold desc="Global Variables">
    host = "mysql.shilohmadsen.com"
    un = "shilohmadsencom"
    pw = "6DNN7Snp"
    db = "themagiccastle"
    conn = None
    cursor = None
    # </editor-fold>

    def __init__(self):
        '''
        :param database: The URL of the database to access. In most cases the IP address of the pi (or network it is on) must be whitelisted to conned
        :param un: The username to connect to the database
        :param pw: The password to connect to the database
        :param db: Database to connect to
        :return:
        '''
        #Attempt to open a connection to the database
        try:
            self.conn = MySQLdb.connect(host=self.host,
                  user= self.un,
                  passwd=self.pw,
                  db=self.db)
            self.cursor = self.conn.cursor()
        #If DB Connection fails, throw exception.
        except MySQLdb.Error as e:
            print "Error: %s" %e
        myVar = "foo"

    def logBoot(self):
        '''
        This function writes the current date and time as well as an int value of 0 to the database to indicate the date and time the Pi was last booted
        If the MAC address has not previously reported in, it creates a record in the PIS table.
        :return: No Return values from function
        '''
        #Code to log a boot instance of the pi
        #MAC address of the booting PI
        mac = get_mac()
        #Current Time
        logTime = datetime.datetime.now()
        logTime = logTime.strftime('%Y-%m-%d %H:%M:%S')

        #Retrieve any DB rows matching our MAC address
        resp = self.cursor.execute("SELECT * FROM  PIS WHERE MacAddress = %s;",str(mac))

        #If no Rows returned. Create a new row
        if resp == 0:
            #This function only works on a PI...disabling it for testing purposes TODO: Test that get IP works.
            ip = get_ip_address('wlan0')
            #ip = "192.168.255.255"
            try:
                createPiRow = self.cursor.execute("INSERT INTO PIS (Status, InstallDate, IPAddress, MacAddress) VALUES (1,%s,%s, %s);",(logTime,str(ip), str(mac)))
            except MySQLdb.Error as e:
                print "Error: %s" %e
        #If rows returned, update the first row returned. Should only be one.
        else:
            #This function only works on a PI...disabling it for testing purposes TODO: Test that get IP works.
            #ip = get_ip_address('wlan0')
            ip = "192.168.255.255"
            try:
                self.cursor.execute("SELECT PIID FROM PIS WHERE MacAddress = %s;",str(mac))
                piid = self.cursor.fetchone()[0]
                # Create new item for the Power On Activity
                res = self.cursor.execute("""INSERT INTO Activity (ActivationTime, ActivationType, PIID) VALUES (%s, 0, %s);""", (logTime, piid))
                # Update the pis table with IP address
                res = self.cursor.execute("UPDATE PIS SET IPAddress = %s, HeartBeat = %s WHERE PIID = %s;",(ip, logTime, piid))
                print res
            except MySQLdb.Error as e:
                print "Error: %s" %e

    def logHeartbeat(self):
        '''
        This function is called by another program (generally on a timer) to write a line to the database indicating that the program continues to run
        :return: No return values from this function
        '''
        #MAC address of the booting PI
        mac = get_mac()
        #Current Time
        logTime = datetime.datetime.now()
        logTime = logTime.strftime('%Y-%m-%d %H:%M:%S')

        #This function only works on a PI...disabling it for testing purposes TODO: Test that get IP works.
        #ip = get_ip_address('wlan0')
        ip = "192.168.255.255"
        try:
            pis = self.cursor.execute("SELECT * FROM  PIS WHERE MacAddress = %s;",str(mac))
            #If no rows returned, create a new row.
            if pis == 0:
                #print "Row not found. Need to create a new entry."
                res = self.cursor.execute("INSERT INTO PIS (Status, InstallDate, IPAddress, MacAddress) VALUES (1,%s,%s, %s);",(logTime,str(ip), str(mac)))

            #Then, get the PI ID to update the activities table.
            self.cursor.execute("SELECT PIID FROM PIS WHERE MacAddress = %s;",str(mac))
            piid = self.cursor.fetchone()[0]
            # Create new item for the Power On Activity
            res = self.cursor.execute("""INSERT INTO Activity (ActivationTime, ActivationType, PIID) VALUES (%s, 1, %s);""", (logTime, piid))
            # Update the pis table with IP address
            res = self.cursor.execute("UPDATE PIS SET IPAddress = %s, HeartBeat = %s WHERE PIID = %s;",(ip, logTime, piid))
            print "Logging Hearbeat"
        except MySQLdb.Error as e:
            print "Error: %s" %e

    def logAccess(self, rfid):
        '''
        This function is called when an rfid reader is triggered. It writes the time of the scan plus the rfid value scanned by the reader to the database.
        :param rfid: The RFID value scanned when this function is called.
        :return:
        '''
        #MAC address of the booting PI
        mac = get_mac()
        #Current Time
        logTime = datetime.datetime.now()
        logTime = logTime.strftime('%Y-%m-%d %H:%M:%S')

        #This function only works on a PI...disabling it for testing purposes TODO: Test that get IP works.
        #ip = get_ip_address('wlan0')
        ip = "192.168.255.255"

        getPi = self.cursor.execute("SELECT * FROM  PIS WHERE MacAddress = %s;",str(mac))
        #If no rows returned, create a new row.
        if getPi == 0:
            #print "Row not found. Need to create a new entry."
            create = self.cursor.execute("INSERT INTO PIS (Status, InstallDate, IPAddress, MacAddress) VALUES (1,%s,%s, %s);",(logTime,str(ip), str(mac)))
            print create

        #Then Update the Activity table with the RFID Access
        # Get the PI ID
        self.cursor.execute("SELECT PIID FROM PIS WHERE MacAddress = %s;",str(mac))
        piid = self.cursor.fetchone()[0]
        # Try to write access of the pi to a log file
        update = self.cursor.execute("""INSERT INTO Activity (RFID, ActivationTime, ActivationType, PIID) VALUES (%s, %s, 2, %s);""", (rfid, logTime, piid))
        print update

    def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])