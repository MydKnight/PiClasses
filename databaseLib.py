import Logger
import MySQLdb
import logging
import sys
import yaml

# Set Up Logging
stdout_logger = logging.getLogger('DBOUT')
sl = Logger.StreamToLogger(stdout_logger, logging.INFO)
sys.stdout = sl

stderr_logger = logging.getLogger('DBERR')
sl = Logger.StreamToLogger(stderr_logger, logging.ERROR)
sys.stderr = sl


class DBConn(object):
    def __init__(self):
        with open("configs.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        _host = cfg['mysql']['host']
        _un = cfg['mysql']['user']
        _pw = cfg['mysql']['passwd']
        _db = cfg['mysql']['db']
        conn = None
        cursor = None

        # Initiate Connection to DB
        try:
            db = MySQLdb.connect(host=_host, user=_un, passwd=_pw, db=_db)
            self.cursor = db.cursor()
        except MySQLdb.OperationalError as e:
            stderr_logger.log(logging.ERROR, e)

    def query(self, query):
        # Send a CRUD query to database if cursor exists
        try:
            return self.cursor.execute(query)
        except Exception as e:
            stderr_logger.log(logging.ERROR, e)

    def __del__(self):
        # Close connection on object deletion
        self.cursor.close()
