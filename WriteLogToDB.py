#!/usr/bin/python
import sys

sys.path.insert(0, '/home/pi/Python')

import logging, os, socket, datetime, fcntl, struct
from uuid import getnode as get_mac
import Logger
import databaseLib

# Set Up Logging
script = os.path.basename(__file__)
stdout_logger = logging.getLogger(script + '_Out')
sl = Logger.StreamToLogger(stdout_logger, logging.DEBUG)
# sys.stdout = sl

stderr_logger = logging.getLogger(script + '_Err')
sl = Logger.StreamToLogger(stderr_logger, logging.ERROR)


# sys.stderr = sl


def main():
    conn = databaseLib.DBConn()

    # Read the MAC address of the PI to retrieve PIID
    mac = get_mac()
    host = socket.gethostname()
    ip = str(get_ip_address('wlan0'))
    piID = 0

    # Check if the Mac Address exists in the DB. Create or Update if need be. Retreieve PIID
    conn.cursor.execute("SELECT PIID, IPAddress, PIDesc FROM PIS WHERE MacAddress = %s", (mac,))
    piRow = conn.cursor.fetchone()
    if (piRow is None):
        # If Mac Address does not exist. Create. Store PIID
        host = socket.gethostname()
        installed = datetime.datetime.now().strftime('%Y-%m-%d')
        ip = str(get_ip_address('wlan0'))
        conn.cursor.execute(
            "INSERT INTO PIS (Status, PiDesc, InstallDate, IPAddress, MacAddress) VALUES (1,%s,%s, %s, %s);",
            (host, installed, ip, str(mac)))
        piID = conn.cursor.lastrowid
    else:
        # If so, check that the name matches the Host Name and the IP matches the IP. If not, Update. Store PIID
        piID = piRow[0]
        piIP = piRow[1]
        piName = piRow[2]
        if (piIP != ip) or (piName != host):
            conn.cursor.execute("UPDATE PIS SET PiDesc = %s, IPAddress = %s WHERE PIID = %s;", (host, ip, piID))

    # If we still dont have a PIID, something went wrong. Bail.
    if piID == 0:
        return

    # Regardless of a log file existing, log a ping to the table indicating the PI is online.
    logPiHeartbeat(conn, piID)

    # We don't want to do anything if there is no log file. Check to see if the file exists, if not, bail.
    if (os.path.isfile('/home/pi/Python/Logs/Data.log') and (os.stat("/home/pi/Python/Logs/Data.log").st_size != 0)):

        # Grab a local copy of the file before renaming
        with open('/home/pi/Python/Logs/Data.log', 'r') as f:
            dataToInsert = f.read()

        # Rename log file - Any script writing to the log file will create a new one once we rename the old one.
        os.rename('/home/pi/Python/Logs/Data.log',
                  '/home/pi/Python/Logs/Archive/Data_{date:%Y-%m-%d %H:%M:%S}.txt'.format(date=datetime.datetime.now()))

        errors = insertLog(conn, piID, dataToInsert)

        # Write a local errors file for anything that could not be inserted.
        file = '/home/pi/Python/Logs/Archive/Errors_{date:%Y-%m-%d %H:%M:%S}.txt'.format(date=datetime.datetime.now())
        with open(file, 'w+') as filehandle:
            for line in errors:
                filehandle.write('%s\n' % line)
    else:
        return


def logPiHeartbeat(conn, piID):
    '''
    Logs the Current DateTime as a heartbeat to the PIs Table
    @param conn: Cursor to the Database
    @param piID: PI ID to update
    @return: void
    '''
    logTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.cursor.execute("UPDATE PIS SET HeartBeat = %s WHERE PIID = %s;", (logTime, piID))


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15]))[20:24])


def insertLog(conn, piID, dataToInsert):
    '''
    This parses the data array from the log and chooses to insert errors and activity type logs into the database.
    All logs of ERROR type will be inserted into the Errors Database.
    All logs of INFO type will be inspected for logger name to determine if they're of Activation, Power On, or other.
    The first two are inserted into the activations database. The last will be maintained for audting
    All logs of type DEBUG are preserved to be handled by another function. These are called by STDOUT being redirected in logging
    @param conn: Database Connection
    @param piID: ID Row in the PIs Database
    @param dataToInsert: array of data to insert
    @return: array of failed insertions
    '''

    dataLines = dataToInsert.split("\n")
    localLog = []
    for line in dataLines:
        data = line.split("||")

        # Handle for empty row
        try:
            data[1]
        except IndexError:
            continue

        if (data[1] == "ERROR"):
            # For each error type, write to database: PythonScript, PIID, ErrorMessage, ErrorTime
            conn.cursor.execute(
                "INSERT INTO Errors (PythonScript, PIID, ErrorMessage, ErrorTime) VALUES (%s, %s, %s, %s);",
                (data[2], piID, data[3], data[0]))

        elif data[1] == "INFO":
            # For Each info type, if activation, write to the Database: TimeStamp, PIID, RFID, Activation type (Activation, Bootup)
            if (data[3] == "Activation"):
                try:
                    RFID = data[4]
                except IndexError:
                    RFID = 0
                conn.cursor.execute(
                    "INSERT INTO Activity (ActivationTime, PIID, RFID, ActivationType) VALUES (%s,%s,%s,2);",
                    (data[0], piID, RFID))
            elif (data[3] == "Bootup"):
                conn.cursor.execute(
                    "INSERT INTO Activity (ActivationTime, PIID, ActivationType) VALUES (%s,%s,1);",
                    (data[0], piID))
            else:
                # We've logged some Info data that is not Marked as a Bootup or an Activation. Keep this data to write to a local file
                localLog.append(",".join(data))
        else:
            # We've logged something that is neither Error nor Info, Store it locally
            localLog.append(",".join(data))

    return localLog

main()
