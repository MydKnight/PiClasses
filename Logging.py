__author__ = 'madsens'

import logging.handlers

import MySQLdb
import yaml

# Defaults
LOG_FILENAME = "/home/pi/Python/Logs/db.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)


# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
    def __init__(self, logger, level):
        """Needs a logger and a logger level."""
        self.logger = logger
        self.level = level

    def write(self, message):
        # Only log if there is a message (not just a new line)
        if message.rstrip() != "":
            self.logger.log(self.level, message.rstrip())


class DBConn(object):
    # Replace stdout with logging to file at INFO level -- May not need this. Only want errors
    # sys.stdout = MyLogger(logger, logging.INFO)
    # Replace stderr with logging to file at ERROR level
    # sys.stderr = MyLogger(logger, logging.ERROR)

    # Grab Database Config Settings
    try:
        with open("configs.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        host = cfg['mysql']['host']
        un = cfg['mysql']['user']
        pw = cfg['mysql']['passwd']
        db = cfg['mysql']['db']
    except IOError:
        print "No Config File Found."

    conn = None
    cursor = None

    def __init__(self):
        # Initiate Connection to DB if cfg exists
        if self.cfg in locals():
            db = MySQLdb.connect(host=self.host, user=self.un, passwd=self.pw, db=self.db)
            self.cursor = db.cursor()
        else:
            print ("No Config File was found. No necessary Parameters to connect")

    def query(self, query, params):
        # Send a CRUD query to database if cursor exists
        if (self.cursor):
            self.cursor.execute("""SELECT * FROM Members""")
        else:
            print ("No cursor exists")

    def __del__(self):
        # Close connection on object deletion
        self.cursor.close()