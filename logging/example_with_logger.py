import logging


def setup_logger():
    cursor_logger = logging.getLogger("cursor")
    cursor_logger.setLevel("DEBUG")
    c_handler = logging.FileHandler(filename='first_logger.yaml')
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    cursor_logger.addHandler(c_handler)
    return cursor_logger


if __name__ == "__main__":
    cursor_logger = setup_logger()
    cursor_logger.warning("Hello")
    cursor_logger.info("Hello from info")
    cursor_logger.debug("Debug_info")

