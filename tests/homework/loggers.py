import functools
import logging
import time
import psycopg2


class LogDBHandler(logging.Handler):
    def __init__(self, psql_conn, psql_cursor, db_tbl_log):
        logging.Handler.__init__(self)
        self.psql_conn = psql_conn
        self.psql_cursor = psql_cursor
        self.db_tbl_log = db_tbl_log

    def emit(self, record):
        # set current time
        tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # Clear the log message so it can be put to db via sql (escape quotes)
        self.log_msg = record.msg
        self.log_msg = self.log_msg.strip()
        self.log_msg = self.log_msg.replace('\'', '\'\'')
        # Make the SQL insert
        sql = """INSERT INTO info_logger (line, level_name, module, created_at, created_by, message) 
                 VALUES ('{}', '{}', '{}', '{}', '{}', '{}');"""\
                 .format(record.lineno, record.levelname, record.module, tm, record.name, self.log_msg)

        self.psql_cursor.execute(sql)
        self.psql_conn.commit()


def create_info_logger():
    connection = psycopg2.connect(user='cursor',
                                  password='password',
                                  host='localhost',
                                  port='5432',
                                  database='tests_db')
    db_tbl_log = 'info_logging'
    cursor = connection.cursor()

    logger = logging.getLogger('info_logger')
    logger.setLevel(logging.INFO)

    db_handler = LogDBHandler(connection, cursor, db_tbl_log)

    file_handler = logging.FileHandler('info.log')
    fmt = '%(asctime)s - %(funcName)s - %(name)s - %(levelname)s -%(message)s'
    formater = logging.Formatter(fmt)
    file_handler.setFormatter(formater)

    logger.addHandler(file_handler)
    logger.addHandler(db_handler)
    return logger


def exception(logger):
    def decorator(func):
        def wraper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                err = 'There was an exception in '
                err += func.__name__
                logger.exception(err)
                raise

        return wraper

    return decorator

logger = create_info_logger()




