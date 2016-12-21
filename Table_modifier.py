__author__ = 'Ajay'
from db_operations import DBOps
import data_db_wrapper
import PySide
import locale


locale.setlocale(locale.LC_ALL)

def callme():
    last = 835
    latest = '2460'
    latest = int (latest)
    if latest >= 1.5 * last:
        print 'Yes it is'

if __name__ == "__main__":

    db_obj_parent = data_db_wrapper.DataDB()
    table_list = db_obj_parent.get_all_tables()
    print len(table_list)
    system_tables = ['CUSTOM_SIGNAL','CUSTOM_SETTINGS','CNX NIFTY 50','CNX NIFTY 200','ALL COMPANIES','CERTUS BUY','CERTUS SELL','VELOX','VELOX BUY','VELOX SELL',
                     'FUTURO BUY','FUTURO SELL','SHORT BUY','SHORT SELL','MID BUY','MID SELL','LONG BUY','LONG SELL','XSHORT BUY','XSHORT SELL',
                     'XLONG BUY','XLONG SELL','CERTUS-VELOX BUY','CERTUS-VELOX SELL','FUTURO-VELOX BUY','FUTURO-VELOX SELL']

    for table in table_list:
        if table in system_tables:
            table_list.remove(table)

    table_list.sort()
    for table in table_list:
        query = "ALTER TABLE ["+table+"] ADD MACD_D_CHNG [decimal](6, 2) NULL"
        db_obj_parent.db_obj.run_query(query,commit=True)
        print 'Updated table %s ' %table
