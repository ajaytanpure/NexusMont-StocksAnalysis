__author__ = 'Ajay'

import pyodbc

DATE = '2015-07-06'
SERVER = 'PRAKASH-PC'
DATABASE = 'NexusMont'
USER = 'share'
PASSWORD = 'admin123'


def delete_data():
    print 'Connecting to database:'
    db_connection = pyodbc.connect(driver='{SQL Server}', server=SERVER, database=DATABASE, uid=USER, pwd=PASSWORD)
    cursor = db_connection.cursor()
    if not cursor:
        print 'Unable to connect database. Exiting.'
        return
    get_table_query = 'SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES'
    result = cursor.execute(get_table_query)
    raw_all = result.fetchall()
    all_tables = []
    for item in raw_all:
        all_tables.append(item[0])

    removal = ['CUSTOM_SIGNAL', 'CUSTOM_SETTINGS', 'CNX NIFTY 50',
               'CNX NIFTY 200', 'ALL COMPANIES', 'CERTUS BUY', 'CERTUS SELL',
               'VELOX BUY', 'VELOX SELL', 'SHORT BUY', 'SHORT SELL',
               'MID BUY', 'MID SELL', 'LONG BUY', 'LONG SELL',
               'XSHORT BUY', 'XSHORT SELL', 'XLONG BUY', 'XLONG SELL',
               'CERTUS-VELOX BUY', 'CERTUS-VELOX SELL']
    # Remove configurations tables using removal list.
    for removal_tab in removal:
        if removal_tab in all_tables:
            print 'removing %s' % removal_tab
            all_tables.remove(removal_tab)

    print 'Starting deleting of the records from %s onwards...' % DATE
    import time

    time.sleep(5)
    all_tables.sort()
    for item in all_tables:
        print 'deleting records from : %s ' % item
        query = "DELETE FROM [%s] WHERE REC_DATE >='%s' " % (item, DATE)
        cursor.execute(query)
        cursor.commit()
    print 'Deletion of records completed successfully'


if __name__ == "__main__":
    delete_data()