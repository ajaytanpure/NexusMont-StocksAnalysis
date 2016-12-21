import logging
from pypyodbc import paramstyle

__author__ = 'Ajay'

import db_operations


class DataDB():

    _SYSTEM_TABLE = None

    def __init__(self):
        self.db_obj = db_operations.DBOps()
        self._SYSTEM_TABLE = ['CUSTOM_SIGNAL', 'CUSTOM_SETTINGS', 'CNX NIFTY 50',
                     'CNX NIFTY 200', 'ALL COMPANIES', 'CERTUS BUY', 'CERTUS SELL',
                     'VELOX BUY', 'VELOX SELL', 'SHORT BUY', 'SHORT SELL',
                     'MID BUY', 'MID SELL', 'LONG BUY', 'LONG SELL',
                     'XSHORT BUY', 'XSHORT SELL', 'XLONG BUY', 'XLONG SELL',
                     'CERTUS-VELOX BUY', 'CERTUS-VELOX SELL']


    def get_all_tables(self):
        query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES"
        db_curs = self.db_obj.run_query(query)
        temp_list = []
        for row in db_curs.fetchall():
            temp_list.append(row[0])
        return temp_list

    def get_averages(self):
        query = "SELECT * FROM CUSTOM_SETTINGS"
        db_curs = self.db_obj.run_query(query)
        return dict(db_curs.fetchall())

    def get_recent_data(self, limit, tab_name):
        query = "SELECT TOP " + str(limit) + " * FROM [dbo].["+tab_name+"] ORDER BY REC_DATE DESC"
        db_curs = self.db_obj.run_query(query)
        #Here convert the data into the dictionary for easy calculation
        headers = [ head[0] for head in db_curs.description ]
        result_dict = [ dict(zip(headers, row)) for row in db_curs.fetchall()]
        return result_dict

    def get_all_table_data(self, tab_name):
        query = "SELECT * FROM [%s] " % tab_name
        db_curs = self.db_obj.run_query(query)
        #Here convert the data into the dictionary for easy calculation
        headers = [head[0] for head in db_curs.description ]
        result_dict = [dict(zip(headers, row)) for row in db_curs.fetchall()]
        return result_dict

    def create_table(self, tab_name):
        query = "CREATE TABLE [dbo].[" + tab_name + "] (REC_DATE DATE NOT NULL," \
                                                     "OPEN_PRICE DECIMAL(8,2) NOT NULL," \
                                                     "HIGH_PRICE DECIMAL(8,2) NOT NULL," \
                                                     "LOW_PRICE DECIMAL(8,2) NOT NULL," \
                                                     "CLOSE_PRICE DECIMAL(8,2) NOT NULL," \
                                                     "SHRT_SIG TINYINT," \
                                                     "SHRT_AVG DECIMAL(8,2)," \
                                                     "SHRT_CHNG DECIMAL(6,2)," \
                                                     "MID_SIG TINYINT," \
                                                     "MID_AVG DECIMAL(8,2)," \
                                                     "MID_CHNG DECIMAL(6,2)," \
                                                     "LONG_SIG TINYINT," \
                                                     "LONG_AVG DECIMAL(8,2)," \
                                                     "LONG_CHNG DECIMAL(6,2)," \
                                                     "CERTUS TINYINT," \
                                                     "VELOX TINYINT," \
                                                     "FUTURO TINYINT," \
                                                     "PIVOT_VALUE DECIMAL(8,2)," \
                                                     "PIVOT_CHNG DECIMAL(6,2)," \
                                                     "STOCHASTIC DECIMAL(8,2)," \
                                                     "MNTM DECIMAL(8,2)," \
                                                     "MNTM_CHNG DECIMAL(6,2)," \
                                                     "QUANTITY INT," \
                                                     "TRADERS INT," \
                                                     "EX_SHRT_SIG TINYINT," \
                                                     "EX_SHRT_AVG DECIMAL(8,2)," \
                                                     "EX_SHRT_CHNG DECIMAL(6,2)," \
                                                     "EX_LONG_SIG TINYINT," \
                                                     "EX_LONG_AVG DECIMAL(8,2)," \
                                                     "MACD DECIMAL(8,2)," \
                                                     "MACD_CHNG DECIMAL(6,2)," \
                                                     "MACD_D_CHNG DECIMAL(6,2)," \
                                                     "PRIMARY KEY (REC_DATE)," \
                                                     "FOREIGN KEY (CERTUS) REFERENCES CUSTOM_SIGNAL(ID)," \
                                                     "FOREIGN KEY (VELOX) REFERENCES CUSTOM_SIGNAL(ID)," \
                                                     "FOREIGN KEY (FUTURO) REFERENCES CUSTOM_SIGNAL(ID)," \
                                                     "FOREIGN KEY (SHRT_SIG) REFERENCES CUSTOM_SIGNAL(ID)," \
                                                     "FOREIGN KEY (MID_SIG) REFERENCES CUSTOM_SIGNAL(ID)," \
                                                     "FOREIGN KEY (LONG_SIG) REFERENCES CUSTOM_SIGNAL(ID)," \
                                                     "FOREIGN KEY (EX_SHRT_SIG) REFERENCES CUSTOM_SIGNAL(ID)," \
                                                     "FOREIGN KEY (EX_LONG_SIG) REFERENCES CUSTOM_SIGNAL(ID))"
        print query
        self.db_obj.run_query(query, commit=True)

    def insert_company_data(self, tab_name, params):
        query = "INSERT INTO [dbo].[" + tab_name + "] values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        print query
        logging.info("Using query : %s" % query)
        self.db_obj.run_query(query, params, commit=True)

    def update_cnx_nifty_list(self, tab_name, company_name):
        if tab_name == 'ind_niftylist.csv':
            query = "INSERT INTO [CNX NIFTY 50] values(?)"
            self.db_obj.run_query(query, params=[company_name], commit=True)
        elif tab_name == 'ind_cnx200list.csv':
            query = "INSERT INTO [CNX NIFTY 200] values(?)"
            self.db_obj.run_query(query, params=[company_name], commit=True)

    def truncate_all_signals(self):
        query = "TRUNCATE TABLE  [CNX NIFTY 50]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [CNX NIFTY 200]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [ALL COMPANIES]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [CERTUS BUY]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [CERTUS SELL]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [VELOX BUY]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [VELOX SELL]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [VELOX]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [FUTURO BUY]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [FUTURO SELL]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [SHORT BUY]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [SHORT SELL]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [MID BUY]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [MID SELL]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [LONG BUY]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [LONG SELL]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [XSHORT BUY]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [XSHORT SELL]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [XLONG BUY]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [XLONG BUY]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [CERTUS-VELOX BUY]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [CERTUS-VELOX SELL]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [FUTURO-VELOX BUY]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [FUTURO-VELOX SELL]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [CERTUS-FUTURO BUY]"
        self.db_obj.run_query(query, params=None, commit=True)
        query = "TRUNCATE TABLE  [CERTUS-FUTURO SELL]"
        self.db_obj.run_query(query, params=None, commit=True)

    def add_to_all_companies(self, company_name):
        query = "INSERT INTO [ALL COMPANIES] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_certus_buy(self,company_name):
        query = "INSERT INTO [CERTUS BUY] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_certus_sell(self,company_name):
        query = "INSERT INTO [CERTUS SELL] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_velox_buy(self,company_name):
        query = "INSERT INTO [VELOX BUY] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_velox_sell(self,company_name):
        query = "INSERT INTO [VELOX SELL] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_velox(self, company_name):
        query = "INSERT INTO [VELOX] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_futuro_buy(self,company_name):
        query = "INSERT INTO [FUTURO BUY] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_futuro_sell(self,company_name):
        query = "INSERT INTO [FUTURO SELL] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_short_buy(self,company_name):
        query = "INSERT INTO [SHORT BUY] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_short_sell(self,company_name):
        query = "INSERT INTO [SHORT SELL] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_mid_buy(self,company_name):
        query = "INSERT INTO [MID BUY] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_mid_sell(self,company_name):
        query = "INSERT INTO [MID SELL] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_long_buy(self,company_name):
        query = "INSERT INTO [LONG BUY] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_long_sell(self,company_name):
        query = "INSERT INTO [LONG SELL] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_xshort_buy(self,company_name):
        query = "INSERT INTO [XSHORT BUY] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_xshort_sell(self,company_name):
        query = "INSERT INTO [XSHORT SELL] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_xlong_buy(self,company_name):
        query = "INSERT INTO [XLONG BUY] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_xlong_sell(self,company_name):
        query = "INSERT INTO [XLONG SELL] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_certus_velox_buy(self, company_name):
        query = "INSERT INTO [CERTUS-VELOX BUY] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_certus_velox_sell(self, company_name):
        query = "INSERT INTO [CERTUS-VELOX SELL] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_futuro_velox_buy(self, company_name):
        query = "INSERT INTO [FUTURO-VELOX BUY] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_futuro_velox_sell(self, company_name):
        query = "INSERT INTO [FUTURO-VELOX SELL] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_certus_futuro_buy(self, company_name):
        query = "INSERT INTO [CERTUS-FUTURO BUY] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def add_to_certus_futuro_sell(self, company_name):
        query = "INSERT INTO [CERTUS-FUTURO SELL] values(?)"
        self.db_obj.run_query(query, params=[company_name], commit=True)

    def get_companies_from_filter(self, filter):
        filtered_companies = []
        query = "SELECT * FROM ["+ filter +"]"
        db_curs = self.db_obj.run_query(query)
        tuple_companies =db_curs.fetchall()
        for item in tuple_companies:
            filtered_companies.append(item[0])
        return filtered_companies

    def get_company_data(self, company):
        query = "SELECT [REC_DATE],[OPEN_PRICE],[HIGH_PRICE],[LOW_PRICE],[CLOSE_PRICE]," \
                "[SHRT_SIG],[SHRT_AVG],[SHRT_CHNG]," \
                "[MID_SIG],[MID_AVG],[MID_CHNG]," \
                "[LONG_SIG],[LONG_AVG],[LONG_CHNG]," \
                "[CERTUS],[VELOX],[FUTURO]," \
                "[PIVOT_VALUE],[PIVOT_CHNG]," \
                "[STOCHASTIC]," \
                "[MACD],[MACD_CHNG],[MACD_D_CHNG], " \
                "[EX_SHRT_SIG],[EX_SHRT_AVG],[EX_SHRT_CHNG]," \
                "[QUANTITY],[TRADERS]," \
                "[EX_LONG_SIG],[EX_LONG_AVG]," \
                "[MNTM],[MNTM_CHNG] " \
                "FROM [NexusMont].[dbo].["+company+"]"
        db_curs = self.db_obj.run_query(query)
        company_info = db_curs.fetchall()
        return company_info

    def delete_before(self, selected_date):
        all_tables = self.get_all_tables()
        for settings_tab in self._SYSTEM_TABLE:
            if settings_tab in all_tables:
                all_tables.remove(settings_tab)
        all_tables.sort()
        logging.info('Deleting data before date %s' % selected_date)
        for table in all_tables:
            logging.info('Deleting data from table %s' % table)
            query = "DELETE FROM [%s] WHERE REC_DATE < ? " % table
            db_curs = self.db_obj.run_query(query, [selected_date], True)
            if db_curs == 0:
                logging.exception('Exception occurred while deleting data')

    def delete_after(self, selected_date):
        all_tables = self.get_all_tables()
        for settings_tab in self._SYSTEM_TABLE:
            if settings_tab in all_tables:
                all_tables.remove(settings_tab)
        all_tables.sort()
        logging.info('Deleting data before date %s' % selected_date)
        for table in all_tables:
            logging.info('Deleting data from table %s' % table)
            query = "DELETE FROM [%s] WHERE REC_DATE > ? " % table
            db_curs = self.db_obj.run_query(query, [selected_date], True)
            if db_curs == 0:
                logging.exception('Exception occurred while deleting data')

    def delete_signals(self, table):
        query = "UPDATE [%s] SET VELOX=?, CERTUS=?, FUTURO=?" % table
        logging.info('Deleting existing signals from %s' % table)
        db_curs = self.db_obj.run_query(query, [None, None, None], True)
        if db_curs == 0:
            logging.exception('Exception while deleting the existing signals')

    def update_signals(self, table, velox, certus,futuro, date):
        query = "UPDATE [%s] SET VELOX=?, CERTUS=?, FUTURO=? WHERE REC_DATE=?" % table
        logging.info('Updating existing signals from %s' % table)
        db_curs = self.db_obj.run_query(query, [velox, certus,futuro, date], True)
        if db_curs == 0:
            logging.exception('Exception while updating the existing signals')

    def update_averages(self, table, macd_d_chng, date):
        query = "UPDATE [%s] SET MACD_D_CHNG=? WHERE REC_DATE=?" % table
        logging.info('Updating existing signals from %s' % table)
        db_curs = self.db_obj.run_query(query, [macd_d_chng, date], True)
        if db_curs == 0:
            logging.exception('Exception while updating the existing signals')

    def close_connection(self):
        self.db_obj.close()

