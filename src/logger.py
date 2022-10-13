import logging
from datetime import datetime


class Logger:
    def __init__(self):
        now = datetime.now()
        date_time = now.strftime("%m-%d-%Y-%H-%M")
        log_file_name = "src/logs/" + date_time + ".log"
        logging.basicConfig(filename=log_file_name, encoding='utf-8', level=logging.INFO)

    @staticmethod
    def log(msg):
        logging.info(msg)

    @staticmethod
    def error(msg):
        logging.error(msg)
