# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from ui_files import settings_ui
import time
from math import ceil
import data_db_wrapper
import math_calculation

EXCLUSION_LIST = ['CNX NIFTY 50', 'CNX NIFTY 200', 'ALL COMPANIES',
                  'CERTUS BUY', 'CERTUS SELL','VELOX',
                  'SHORT BUY','SHORT SELL','MID BUY','MID SELL',
                  'LONG BUY','LONG SELL','XSHORT BUY','XSHORT SELL',
                  'XLONG BUY','XLONG SELL','CERTUS-VELOX BUY','CERTUS-VELOX SELL']

class SettingPage(settings_ui.Ui_Dialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.reload_status_bar.setValue(0)
        self.reload_worker = ReloadThread(setting_obj=self)
        self.delete_worker = DeleteThread(setting_obj=self)

        self.delete_button.clicked.connect(self.delete_data)
        self.delete_worker.update_delete_status.connect(self.update_delete_status)
        self.delete_worker.show_message.connect(self.show_delete_message)
        self.delete_worker.enable_disable_delete_button.connect(self.enable_disable_button)

        self.reload_data_button.clicked.connect(self.reload_data)
        self.reload_worker.show_message.connect(self.update_reload_status)
        self.reload_worker.update_progress.connect(self.update_progressbar)
        self.reload_worker.enable_disable_button.connect(self.enable_disable_button)
        self.reload_worker.update_status.connect(self.update_status_reload)


    def delete_data(self):
        self.delete_worker.start()

    def update_delete_status(self, status):
        self.delet_status.setText(status)

    def enable_disable_button(self, status):
        if status:
            self.delete_button.setEnabled(True)
            self.reload_data_button.setEnabled(True)
        else:
            self.delete_button.setEnabled(False)
            self.reload_data_button.setEnabled(False)

    def show_delete_message(self, message):
        QtGui.QMessageBox.critical(self,'Error',message)

    def reload_data(self):
        self.reload_worker.start()

    def update_reload_status(self, message):
        QtGui.QMessageBox.information(self,'Info', message)

    def update_progressbar(self, progress):
        self.reload_status_bar.setValue(progress)

    def update_status_reload(self, status):
        self.reload_status.setText(status)
##################################################################################


class ReloadThread(QtCore.QThread):

    update_status = QtCore.Signal(basestring)
    show_message = QtCore.Signal(basestring)
    update_progress = QtCore.Signal(int)
    enable_disable_button = QtCore.Signal(int)

    def __init__(self, setting_obj, parent=None):
        self.setting_ob = setting_obj
        super(ReloadThread, self).__init__(parent)
        self.data_db_obj = data_db_wrapper.DataDB()
        self.math_obj = math_calculation.Mathematics()


    def run(self):
        averages = self.math_obj.averages
        limit = averages['EX_LONG_TERM'] - 1
        limit = int(limit)
        all_tables = self.data_db_obj.get_all_tables()
        self.enable_disable_button.emit(0)
        self.update_status.emit('Started reloading the signals')
        system_tables = ['CUSTOM_SIGNAL', 'CUSTOM_SETTINGS', 'CNX NIFTY 50',
                         'CNX NIFTY 200', 'ALL COMPANIES', 'CERTUS BUY', 'CERTUS SELL',
                         'FUTURO BUY','FUTURO SELL','VELOX BUY','VELOX SELL', 'SHORT BUY', 'SHORT SELL',
                         'MID BUY', 'MID SELL', 'LONG BUY', 'LONG SELL',
                         'XSHORT BUY', 'XSHORT SELL', 'XLONG BUY', 'XLONG SELL',
                         'CERTUS-VELOX BUY', 'CERTUS-VELOX SELL','FUTURO-VELOX BUY', 'FUTURO-VELOX SELL',
                         'CERTUS-FUTURO BUY', 'CERTUS-FUTURO SELL']

        for sys_tab in system_tables:
            if sys_tab in all_tables:
                all_tables.remove(sys_tab)

        all_tables.sort()
        total_tables = len(all_tables)
        batch = total_tables/100
        done_count = 0
        progress = 0
        for table in all_tables:
            status = 'Reloading signals of %s ' % table
            self.update_status.emit(status)
            self.data_db_obj.delete_signals(table)
            # if table == 'BHARATFORG':
            #     import pdb;pdb.set_trace()
            all_historical_data = self.data_db_obj.get_all_table_data(table)
            recent = []
            for row in all_historical_data:
                today = row
                # if today['REC_DATE'] == '2015-02-11' and table == 'BHARATFORG':
                #     import pdb;pdb.set_trace()
                company_details = {'TOTTRDQTY':today['QUANTITY'],'TOTALTRADES':today['TRADERS']}
                short_details = [today['SHRT_SIG'],today['SHRT_AVG'],today['SHRT_CHNG']]
                ex_short_details = [today['EX_SHRT_SIG'],today['EX_SHRT_AVG'],today['EX_SHRT_CHNG']]
                mid_details = [today['MID_SIG'], today['MID_AVG'], today['MID_CHNG']]
                long_details = [today['LONG_SIG'], today['LONG_AVG'], today['LONG_CHNG']]
                pivot_details = [today['PIVOT_VALUE'], today['PIVOT_CHNG']]
                momentum_details = [today['MNTM'], today['MNTM_CHNG']]
                stochastic_details = [today['STOCHASTIC']]
                macd_details = [today['MACD'], today['MACD_CHNG'], ['MACD_D_CHNG']]

                certus_signal = self.math_obj.calculate_certus(details=recent[:3],
                                                               ex_short_details=ex_short_details,
                                                               short_details=short_details,
                                                               mid_details=mid_details,
                                                               stochastic_details=stochastic_details)

                velox_signal = self.math_obj.calculate_velox(recent[:3], None, ex_short_details, short_details,mid_details, long_details, pivot_details,
                                                             macd_details, stochastic_details)
                futuro_signal = self.math_obj.calculate_futuro(recent[:3], pivot_details, momentum_details, ex_short_details, short_details, mid_details, long_details, stochastic_details)

                macd_d_chng = self.math_obj.calculate_macd_d(macd_details=macd_details, short_details=short_details)
                # macd is not required now
                recent.insert(0, today)
                del(recent[limit+1:])
                #Here update tables
                self.data_db_obj.update_signals(table, velox=velox_signal, certus=certus_signal,futuro=futuro_signal, date=today['REC_DATE'])

                #self.data_db_obj.update_averages(table, macd_d_chng, date=today['REC_DATE'])
                #macd is not required for now to update

            done_count +=1
            if done_count % batch == 0:
                progress += 1
                self.update_progress.emit(progress-1)
        self.update_progress.emit(100)
        self.update_status.emit('Completed.Please Close The Window!!')
        message = 'Signals Reloaded successfully!!'
        self.show_message.emit(message)
        self.enable_disable_button.emit(1)


class DeleteThread(QtCore.QThread):

    update_delete_status = QtCore.Signal(basestring)
    show_message = QtCore.Signal(basestring)
    enable_disable_delete_button = QtCore.Signal(int)

    def __init__(self, setting_obj, parent=None):
        self.setting_obj = setting_obj
        super(DeleteThread, self).__init__(parent)
        self.data_db_obj = data_db_wrapper.DataDB()

    def run(self):
        self.update_delete_status.emit('Deleting the records. Please wait....')
        selected_date = self.setting_obj.dateEdit.date().toString('yyyy-MM-dd')
        if self.setting_obj.before_radio.isChecked():
            self.enable_disable_delete_button.emit(0)
            self.data_db_obj.delete_before(selected_date)
            self.update_delete_status.emit('Deleted successfully...!!!!')
            self.enable_disable_delete_button.emit(1)
        elif self.setting_obj.after_radio.isChecked():
            self.enable_disable_delete_button.emit(0)
            self.data_db_obj.delete_after(selected_date)
            self.update_delete_status.emit('Deleted successfully...!!!!')
            self.enable_disable_delete_button.emit(1)
        else:
            self.update_delete_status.emit('Error occurred!!')
            message = "Please select 'Before' or 'After' first.\nSelect the date carefully.Selection is not inclusive"
            self.show_message.emit(message)




