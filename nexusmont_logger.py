__author__ = 'Ajay'
import nexusmont_config
import datetime
import logging
import os


def set_logging():
    logging_options = nexusmont_config.get_logging_details()

    log_dir = logging_options['log_dir']

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_name = "NexusMont-%s.log" % (datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    log_name = os.path.join(log_dir, log_name)

    log_level = None
    if logging_options['log_level'] == 'debug':
        log_level = logging.DEBUG
    elif logging_options['log_level'] == 'info':
        log_level = logging.INFO
    elif logging_options['log_level'] == 'warning':
        log_level = logging.WARNING
    elif logging_options['log_level'] == 'critical':
        log_level = logging.CRITICAL

    log_format = '%(asctime)s : %(levelname)s : %(message)s'

    print logging_options['log_dir']
    logging.basicConfig(filename=log_name, format=log_format, level=log_level, datefmt="%Y-%m-%d %H:%M:%S")
    logging.info("This is first log")