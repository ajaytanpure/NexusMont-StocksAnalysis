__author__ = 'Ajay'

import pyodbc
import nexusmont_config
import logging
import traceback


class DBOps():

    _db_connection = None
    _db_cur =None

    def __init__(self):
        pass

    def connect(self):
        database_option = nexusmont_config.get_database_details()
        logging.debug("Read the database configuration from configuration file")
        server = database_option['server']
        database = database_option['database']
        user = database_option['user']
        password = database_option['password']
        logging.debug("Connecting to database")
        self._db_connection = pyodbc.connect(driver='{SQL Server}', server=server, database=database, uid=user, pwd=password)
        logging.debug("Connected to database")
        self._db_cur = self._db_connection.cursor()

    def run_query(self, query, params=None, commit=False):
        if params == None:
            params = []
        if not self._db_connection:
            logging.debug("Not connected to Database, Trying to connect")
            self.connect()
        try:
            self._db_cur.execute(query, params)
        except AttributeError:
            self.connect()
            self._db_cur.execute(query, params)
        except Exception as e:
            logging.exception("Exception occurred while executing the sql query"
                              + query + " with parameters" + str(params))
            return 0
        if commit:
            self._db_cur.commit()
        return self._db_cur

    def close(self):
        if self._db_connection:
            self._db_connection.close()
            logging.debug("Closed database connection")

