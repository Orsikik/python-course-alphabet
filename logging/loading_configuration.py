import logging
import logging.config
import yaml


def setupLogging():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)


def log_error(message):
    logger.error(message)


def log_info(message):
    logger.info(message)


if __name__ == "__main__":
    setupLogging()
    logger = logging.getLogger("sampleLogger")

    log_error("Lets see our error")
