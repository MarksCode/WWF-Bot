import os
import logging
from datetime import datetime
import config


class Logger:
    def __init__(self):
        now = datetime.now()
        date_time = now.strftime("%m-%d-%Y-%H-%M")
        player_num = os.environ['PLAYER']
        log_file_name = "logs/player_" + player_num + '_' + date_time + ".log"
        logging.basicConfig(filename=os.path.join(config.root, log_file_name), encoding='utf-8', level=logging.INFO)

    @staticmethod
    def log(msg):
        logging.info(msg)

    @staticmethod
    def error(msg):
        logging.error(msg)


logger = Logger()
