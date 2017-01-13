import sys

__author__ = 'Ajay'

import csv
import os, time
import logging
import data_db_wrapper
from decimal import Decimal
import math_calculation

TWO_PLACES = Decimal(10) ** -2

class DataCalc():

    def __init__(self):
        self.nse_file_name = None
        self.cnx_nifty_file_name = None
        self.cnx_bank_file_name = None
        self.existing_table = []
        self.data_db_obj = data_db_wrapper.DataDB()
        self.get_existing_tables()
        self.empty_all_signals()
        self.update_cnx_list()

    def get_existing_tables(self):
        self.existing_table = self.data_db_obj.get_all_tables()

    def empty_all_signals(self):
        self.data_db_obj.truncate_all_signals()

    def update_cnx_list(self):
        cnx_file_list = ['ind_niftylist.csv', 'ind_nifty200list.csv']
        cnx_file_obj = None
        for file_name in cnx_file_list:
            try:
                 cnx_file_obj = open(os.path.join("data", file_name), "r")
            except (OSError, IOError) as e:
                 logging.exception('\nException occurred while calculating averages')
            csv_input = csv.DictReader(cnx_file_obj)
            for row in csv_input:
                company_name = row['Symbol']
                self.data_db_obj.update_cnx_nifty_list(file_name, company_name)
            cnx_file_obj.close()

    def close_db_connection(self):
        self.data_db_obj.close_connection()

    def handle_nse(self, file_name):
        file_obj = None
        try:
            file_obj = open(os.path.join("data", file_name), "r")
        except (OSError, IOError) as e:
            logging.exception('\nException occurred while calculating averages')
            yield 'Error'
            sys.exit(1)
        csv_input = csv.DictReader(file_obj)

        #get the counts of companies for maintaining the progress bar
        table_count = 0
        for row in csv_input:
            if row['SERIES'] == 'EQ':
                table_count += 1
        self.math_obj = math_calculation.Mathematics()
        batch = table_count/20
        done_count = 0
        progress = 0
        file_obj.seek(0)
        csv_input = csv.DictReader(file_obj)
        for company_details in csv_input:
            if company_details['SERIES'] == 'EQ':
                self.create_insert(company_details)
                #Here call another function for calculation of data. Like here get the data last Extra ling
                # average value. And pass this list of list to math calculation class to get all formulae evaluated
                done_count += 1
                if done_count % batch == 0:
                    progress += 5
                    yield (progress)
        yield 101
        #self.close_db_connection()

    def create_insert(self, company_details):
        tab_name = company_details['SYMBOL']
        open_val = Decimal(company_details['OPEN']).quantize(TWO_PLACES)
        high_val = Decimal(company_details['HIGH']).quantize(TWO_PLACES)
        low_val = Decimal(company_details['LOW']).quantize(TWO_PLACES)
        close_val = Decimal(company_details['CLOSE']).quantize(TWO_PLACES)
        time_stamp = company_details['TIMESTAMP']

        if not tab_name in self.existing_table:
            logging.info('Creating table :' + tab_name)
            self.data_db_obj.create_table(tab_name=tab_name)

        company_info = [time_stamp, open_val, high_val, low_val, close_val]
        calculated_details = self.math_obj.calculate_avg(company_details)
        company_info.extend(calculated_details)
        logging.info("Inserting into table %s " % tab_name)
        self.data_db_obj.insert_company_data(tab_name, company_info)
        time.sleep(0.001)
        print "Inserted into : ", tab_name

