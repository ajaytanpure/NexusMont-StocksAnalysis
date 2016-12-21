__author__ = 'Ajay'

from PySide import  QtGui, QtCore
from ui_files import import_ui
import file_downloader
import time
import data_calculations


class ImportPage(import_ui.Ui_Dialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.import_progressbar.setValue(0)
        self.data_worker = DataThread(import_obj=self)
        self.data_worker.updateProgress.connect(self.update_progressbar)
        self.data_worker.updateStatus.connect(self.update_status)
        self.data_worker.showMessage.connect(self.show_message)
        self.data_worker.enable_disable_button.connect(self.enable_disable_import_button)
        self.start_import_button.clicked.connect(self.download_file)
        self.status_lable.setText("")

    def download_file(self):
        download_success = self.data_worker.start()

    def update_progressbar(self, progress):
        self.import_progressbar.setValue(progress)

    def update_status(self, text):
        self.status_lable.setText(text)

    def show_message(self, text):
        QtGui.QMessageBox.critical(self, "Error", text)

    def enable_disable_import_button(self, state):
        if state:
            self.start_import_button.setEnabled(True)
        else:
            self.start_import_button.setEnabled(False)


class DataThread(QtCore.QThread):

    updateProgress = QtCore.Signal(int)
    updateStatus = QtCore.Signal(basestring)
    showMessage = QtCore.Signal(basestring)
    enable_disable_button = QtCore.Signal(int)

    def __init__(self,import_obj,parent=None):
        self.import_obj = import_obj
        super(DataThread, self).__init__(parent)

    def run(self):
        nse_file_name = None
        cnx_nifty_file_name = None
        cnx_bank_file_name = None
        self.updateProgress.emit(0)
        self.enable_disable_button.emit(0)
        self.updateStatus.emit('Downloading Data from NSE')
        file_names = file_downloader.download_wrapper(self.import_obj)
        if file_names.has_key('Error'):
            self.showMessage.emit(str(file_names['Error']))
            self.updateStatus.emit("Error while downloading file. Check logs")
            return
        else:
            self.updateStatus.emit("Download Completed Successfully")
            self.updateProgress.emit(100)
            self.enable_disable_button.emit(1)
            time.sleep(1)
            self.updateProgress.emit(0)
            self.updateStatus.emit('Calculating....')
        nse_file_name = file_names['nse_file_name']

        #TODO: nifty file name and bank file name are needed now. May in future this might be needed. Also file_name consists
        #TODO: name of the list of cnx 50 and 200. Which is not needed as of now

        cnx_nifty_file_name = file_names['cnx_nifty_file_name']
        cnx_bank_file_name = file_names['cnx_bank_file_name']
        cnx_50_file_name = file_names['cnx_50_file_name']
        cnx_200_file_name = file_names['cnx_200_file_name']

        data_cal_obj = data_calculations.DataCalc()
        self.enable_disable_button.emit(0)
        inserter = data_cal_obj.handle_nse(nse_file_name)
        while True:
            progress = inserter.next()
            if progress == 101:
                self.updateStatus.emit('Import Successful..!!!!')
                self.enable_disable_button.emit(1)
                break
            self.updateProgress.emit(progress)





