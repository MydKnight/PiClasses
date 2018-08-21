import logging


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())


logging.basicConfig(
    level=logging.DEBUG,
    # format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
    format='{"Time": %(asctime)s, "Level": %(levelname)s, "Name": %(name)s, "Message": %(message)s}',
    filename="/home/pi/Python/Logs/out.log",
    filemode='a'
)
