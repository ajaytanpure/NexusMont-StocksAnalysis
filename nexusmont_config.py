__author__ = 'Ajay'
import ConfigParser


def read_config():
    options = ConfigParser.ConfigParser()
    options.read('configuration.ini')
    return options


def get_logging_details():
    logging_options = read_config()._sections['LOGGING']
    return logging_options


def get_database_details():
    logging_options = read_config()._sections['DATABASE']
    return logging_options
