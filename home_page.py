__author__ = 'Ajay'

from PySide import QtGui, QtCore
from ui_files import home_ui
import import_page, chart_page, setting_page


class HomePage(home_ui.Ui_MainWindow):

    _ref_maintainer =[]
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.import_button.clicked.connect(self.open_importer)
        self.chart_button.clicked.connect(self.open_chart)
        self.close_button.clicked.connect(self.close_main_window)
        self.setting_button.clicked.connect(self.open_settings)

    def open_importer(self):
        """
        Open new dialog for downloading and importing file from NSE
        """
        import_obj = import_page.ImportPage()
        if len(HomePage._ref_maintainer) > 0:
            HomePage._ref_maintainer[:] = []
        HomePage._ref_maintainer.append(import_obj)
        import_obj.setModal(True)
        import_obj.show()

    def open_chart(self):
        """
        Open new window for showing the charts and graphs
        """
        chart_obj = chart_page.ChartPage()
        if len(HomePage._ref_maintainer) > 0:
            HomePage._ref_maintainer[:] = []
        HomePage._ref_maintainer.append(chart_obj)
        chart_obj.setModal(True)
        chart_obj.show()

    def open_settings(self):
        """
        Opens the new window for setting page
        """
        setting_obj = setting_page.SettingPage()
        if len(HomePage._ref_maintainer) > 0:
            HomePage._ref_maintainer[:] = []
        HomePage._ref_maintainer.append(setting_obj)
        setting_obj.setModal(True)
        setting_obj.show()


    def closeEvent(self, event):
        """
        Action to taken when Main window is closed.
        Clear all the memory to avoid memory leaks
        """
        if len(HomePage._ref_maintainer) > 0:
            HomePage._ref_maintainer[:] = []

    def close_main_window(self):
        """
        Close the whole application
        """
        self.close()
