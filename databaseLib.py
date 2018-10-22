import logging
import os
import sys

import MySQLdb
import yaml

import Logger

# Set Up Logging
script = os.path.basename(__file__)
stdout_logger = logging.getLogger(script + '_Out')
sl = Logger.StreamToLogger(stdout_logger, logging.DEBUG)
sys.stdout = sl

stderr_logger = logging.getLogger(script + '_Err')
sl = Logger.StreamToLogger(stderr_logger, logging.ERROR)
sys.stderr = sl


class DBConn(object):
    def __init__(self):
        print os.getcwd()
        with open("/home/pi/Python/Configs/configs.yml", 'r') as ymlfile:
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

    def __del__(self):
        # Close connection on object deletion
        self.cursor.close()