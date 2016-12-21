__author__ = 'Ajay'

import urllib2
import zipfile
import logging
import calendar
import traceback
from urllib2 import *
from PySide.QtGui import QMessageBox
import data_calculations
import url_constructor


def get_selected_date(import_obj):
    q_date = import_obj.calendarWidget.selectedDate()
    return q_date.year(), q_date.month(), q_date.day()


def download_from_nseindia(file_name, url):
    directory = "data"
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) '
                         'Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    try:
        req = urllib2.Request(url, headers=hdr)
        file_url = urllib2.urlopen(req)
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
            file_name_obj = open(os.path.join(directory, file_name), 'wb')
            file_name_obj.write(file_url.read())
            file_name_obj.close()
        except IOError:
            logging.info("Exception occurred while doing file operation")
            logging.info("Filename : %s" % file_name)
            logging.info(traceback.format_exc())
            logging.exception("Exception occurred for file %s" % file_name)
    except HTTPError, err:
        logging.exception("Exception occurred")
        return err
    except URLError, err:
        logging.exception("Exception Occurred")
        return err
    return 1



def file_extractor(file_name):
    directory = "data"
    try:
        file_handle = open(os.path.join(directory, file_name), 'rb')
        zip_obj = zipfile.ZipFile(file_handle)
        for name in zip_obj.filelist:
            zip_obj.extract(name, directory)
        zip_obj.close()
        file_handle.close()
    except IOError, zipfile.BadZipfile:
        logging.info("\nException occurred while unzipping the file."
                     "\n" + traceback.format_exc())
        return IOError
    return 1


def download_wrapper(import_obj):
    """
    Download the file for the given date
    """
    year, month, day = get_selected_date(import_obj)
    file_lists = []
    result = dict()
    #Get the url and file name constructed here for downloading. Append all it in the list for downloading further
    cnx_nifty_file_name, cnx_nifty_url = url_constructor.construct_cnx_nifty_url(year, month, day)
    #file_lists.append([cnx_nifty_file_name, cnx_nifty_url])
    cnx_bank_file_name, cnx_bank_url = url_constructor.construct_cnx_bank_url(year, month, day)
    #file_lists.append([cnx_bank_file_name, cnx_bank_url])
    nse_file_name, nse_url = url_constructor.construct_nse_url(year, month, day)
    file_lists.append([nse_file_name, nse_url])
    cnx_50_file_name, cnx_50_url = url_constructor.construct_nifty_50_url()
    file_lists.append([cnx_50_file_name, cnx_50_url])
    cnx_200_file_name, cnx_200_url = url_constructor.construct_nifty_200_url()
    file_lists.append([cnx_200_file_name, cnx_200_url])

    #Download all files here. If error occurred then appropriate error message return back to Main UI
    for file_details in file_lists:
        logging.info("Downloading file: %s from: %s" % (file_details[0], file_details[1]))
        download_result = download_from_nseindia(file_details[0], file_details[1])
        if download_result != 1:
            result['Error'] = str(download_result)
            return result
        logging.info("Download successfully file: %s" % file_details[0])

    #NSE bhavcopy is in zip format. It needs to be unzipped. Appropriate Error message uis sent back to UI
    extract_result = file_extractor(nse_file_name)
    if extract_result != 1:
        result['Error'] = str(extract_result)
        return result

    #Get the name only here. Trim the .zip extension
    nse_file_name = nse_file_name.rsplit('.', 1)[0]

    #Creating dictionary to return the file names of downloaded files for further processing.
    result['nse_file_name'] = nse_file_name
    result['cnx_nifty_file_name'] = cnx_nifty_file_name
    result['cnx_bank_file_name'] = cnx_bank_file_name
    result['cnx_50_file_name'] = cnx_50_file_name
    result['cnx_200_file_name'] = cnx_200_file_name
    return result