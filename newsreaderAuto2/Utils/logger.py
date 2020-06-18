import logging
import logging.handlers
import os
import time

# class Logger(object):
#     def __init__(self):
#         self.initialized = True

def get_logger(name):
    # self.init_logging()
    logger = logging.getLogger(name)
    return logger

def init_logging(deviceId):
    # if self.initialized:
    #     pass
    # logger = logging.root
    # use 'airtest' as root logger name to prevent changing other modules' logger
    print 'init log'
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s : %(funcName)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S"

    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs"))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # fh = logging.FileHandler(os.path.join(log_dir, 'neteaseAuto.log'))
    fh = logging.handlers.RotatingFileHandler(os.path.join(log_dir, 'neteaseAuto_' + deviceId + '.log'), maxBytes= 30 * 1024 * 1024, backupCount=10)
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    # logging.basicConfig(filename=os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs")),
    #                                 TIME + '.log'), level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)
    # logging.getLogger().addHandler(logging.StreamHandler())

    # logger.setLevel(logging.DEBUG)
    # handler = logging.StreamHandler()
    # formatter = logging.Formatter(
    #     fmt='[%(asctime)s][%(levelname)s]<%(name)s> %(message)s',
    #     datefmt='%I:%M:%S'
    # )
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)


