
import logging

# add filemode="w" to overwrite
logging.basicConfig(filename="sample.log", level=logging.DEBUG)


logging.debug("This is a debug message")
logging.info("New 3")
logging.error("An error has happened!")