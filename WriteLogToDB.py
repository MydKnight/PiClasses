import logging
import os
import socket
import sys

import Logger
import databaseLib

# Set Up Logging
stdout_logger = logging.getLogger('SENDDBOUT')
sl = Logger.StreamToLogger(stdout_logger, logging.INFO)
# sys.stdout = sl

stderr_logger = logging.getLogger('SENDDBERR')
sl = Logger.StreamToLogger(stderr_logger, logging.ERROR)
sys.stderr = sl


def main():
    # We don't want to do anything if there is no log file. Check to see if the file exists, if not, bail.
    if (os.path.isfile('/home/pi/Python/Logs/Data.log')):
        # Grab a local copy of the file before renaming
        with open('/home/pi/Python/Logs/Data.log', 'r') as f:
            dataToInsert = f.read()

        # Rename log file - Any script writing to the log file will create a new one once we rename the old one.
        # os.rename('/home/pi/Python/Logs/Data.log', '/home/pi/Python/Logs/Data_{date:%Y-%m-%d %H:%M:%S}.txt'.format(date=datetime.datetime.now()))

        errors = insertLog(dataToInsert)
        # Write a local errors file for anything that could not be inserted.
    else:
        return


def insertLog(dataToInsert):
    '''
    This parses the data array from the log and chooses to insert errors and activity type logs into the database.
    All logs of ERROR type will be inserted into the Errors Database.
    All logs of INFO type will be inspected for logger name to determine if they're of Activation, Power On, Heartbeat or other.
    The first three are inserted into the activations database. The last will be maintained for audting
    @param dataToInsert: Array of log file entries read from log.
    @return: Array of logs that were NOT inserted to write to a new file
    '''

    # We're gonna need a DB cursor to do all of this, so establish our DB Instance
    conn = databaseLib.DBConn();

    dataLines = dataToInsert.split("\n")
    for line in dataLines:
        data = line.split("||")
    for entry in data:
        if (entry[1] == "ERROR"):
            # For each error type, write to database: Error, TimeStamp, PI ID(Retrieved via a select statement)
            errorMsg = entry[3]
            timeStamp = entry[2]
            hostName = socket.gethostname()
            piID = getPiIdFromHostname(hostName, conn)
            if (piID == -1):
                pass

            pass
        if entry[1] == "INFO":
            # For Each info type, if activation, write to the Database: TimeStamp PI ID, RFID, Activation type (Activation, Heartbeat, Bootup)
            pass


def getPiIdFromHostname(host, connection):
    '''
    Given a host name, looks that host name up in the database. Returns -1 if no row found.
    @param host: Hostname of PI
    @param connection: DB Connection
    @return: integer of PIID
    '''
    piid = connection.query("SELECT PIID FROM PIS WHERE PIDesc == %s", (host))
    if (piid > 0):
        pass
    else:
        return -1


main()
