import logging
from database import Base
from helpers.server import ORMObjectToDict

class CustomLogger(logging.Logger):
  '''
  Custom logger that prints database objects as dictionaries.

  Example usage:
    from logger import log
    log.info("Hello world!")
    log.info(myDatabaseObject)
    log.warning("Something went wrong!")    
  '''
  def __init__(self, name):
    super().__init__(name)

  def getMsg(self, msg):
    try:
      # Print database objects as dictionaries
      if isinstance(msg, Base):
        return f"{msg}: {ORMObjectToDict(msg)}"
      else:
        return msg
    except:
      return msg
  
  def info(self, msg, *args, **kwargs):
    super().info(self.getMsg(msg), *args, **kwargs)
  def warning(self, msg, *args, **kwargs):
    super().warning(self.getMsg(msg), *args, **kwargs)
  def error(self, msg, *args, **kwargs):
    super().error(self.getMsg(msg), *args, **kwargs)
  def critical(self, msg, *args, **kwargs):
    super().critical(self.getMsg(msg), *args, **kwargs)

# Set our custom logger as the default logger
logging.setLoggerClass(CustomLogger)

# Create a custom logger
log = logging.getLogger('global_logger')

# Set the level of logger. It can be DEBUG, INFO, WARNING, ERROR or CRITICAL
# TODO: From settings
log.setLevel(logging.DEBUG)

# Create handlers
# TODO: from settings
console_handler = logging.StreamHandler()  # logs to console
#file_handler = logging.FileHandler('logfile.log') # logs to a file

# Set the level of handler
console_handler.setLevel(logging.DEBUG)
#file_handler.setLevel(logging.DEBUG)

# Create formatter and add it to handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
console_handler.setFormatter(formatter)
#file_handler.setFormatter(formatter)

# Add handlers to the logger
log.addHandler(console_handler)
#log.addHandler(file_handler)