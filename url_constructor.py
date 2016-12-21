__author__ = 'Ajay'

import calendar
import os

__NSE_URL = "http://www.nseindia.com/content/historical/EQUITIES/"
__CNX_NIFTY_URL = "http://www.nseindia.com/content/indices/histdata/NIFTY%2050"
__CNX_BANK_URL = "http://www.nseindia.com/content/indices/histdata/CNX%20BANK"
__CNX_NIFTY_50_LIST = "http://www.nseindia.com/content/indices/ind_niftylist.csv"
__CNX_NIFTY_200_LIST = "https://www1.nseindia.com/content/indices/ind_nifty200list.csv"

def construct_nse_url(year, month, day):
    nse_file_name = "cm%02d%s%sbhav.csv.zip" % (day, calendar.month_abbr[month].upper(), year)
    nse_url = "%s/%s/%s/%s" % (__NSE_URL, year, calendar.month_abbr[month].upper(), nse_file_name)
    return nse_file_name, nse_url


def construct_cnx_nifty_url(year, month, day):
    cnx_nifty_file_name = "CNX NIFTY%02d-%02d-%d-%02d-%02d-%d.csv" % (day, month, year, day, month, year)
    cnx_nifty_url = "%s%02d-%02d-%d-%02d-%02d-%d.csv" % (__CNX_NIFTY_URL, day, month, year, day, month, year)
    return cnx_nifty_file_name, cnx_nifty_url


def construct_cnx_bank_url(year, month, day):
    cnx_bank_file_name = "CNX BANK%02d-%02d-%d-%02d-%02d-%d.csv" % (day, month, year, day, month, year)
    cnx_bank_url = "%s%02d-%02d-%d-%02d-%02d-%d.csv" % (__CNX_NIFTY_URL, day, month, year, day, month, year)
    return cnx_bank_file_name, cnx_bank_url

def construct_nifty_50_url():
    cnx_nifty_50_file = os.path.basename(__CNX_NIFTY_50_LIST)
    return cnx_nifty_50_file, __CNX_NIFTY_50_LIST

def construct_nifty_200_url():
    cnx_nifty_200_file = os.path.basename(__CNX_NIFTY_200_LIST)
    return cnx_nifty_200_file, __CNX_NIFTY_200_LIST