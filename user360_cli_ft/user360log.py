import logging
import logging.handlers
import datetime
import time

now = datetime.datetime.now()
log_file = 'user360clift_' + now.strftime('%Y%m%d%H%M%S') +'.log'
#create logger
logger = logging.getLogger(log_file)
logger.setLevel(logging.DEBUG)
 
 
# create console handler and set level to debug
printout_log = logging.StreamHandler()
printout_log.setLevel(logging.INFO)
# create file handler and set level to warning
toFile_log = logging.FileHandler(log_file)
toFile_log.setLevel(logging.DEBUG)
# create formatter
formatter_printout = logging.Formatter('%(asctime)s - %(message)s')
#formatter_toFile_log = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
formatter_toFile_log = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# add formatter to ch and fh
printout_log.setFormatter(formatter_printout)
toFile_log.setFormatter(formatter_toFile_log)
# add ch and fh to logger
logger.addHandler(printout_log)
logger.addHandler(toFile_log)

# 'application' code
'''
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
'''