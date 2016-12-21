# -*- coding: utf-8 -*-

from PySide import  QtGui, QtCore
from PySide.QtWebKit import QWebView
from ui_files import chart_ui
import data_db_wrapper


class ChartPage(chart_ui.Ui_Dialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.long_label.setText('EX_SHORT :')
        self.table_data.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table_data.setStyleSheet('selection-background-color: DodgerBlue')
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.db_obj = data_db_wrapper.DataDB()
        self.load_filters()
        self.filter_selector.currentIndexChanged.connect(self.load_companies)
        self.viewer.clicked.connect(self.load_company_data)

    def load_filters(self):
        """
        Loads the following selectors in the first combo box to select the company
        """
        self.filter_selector.clear()
        filters_list = ['Select', 'ALL COMPANIES', 'CNX NIFTY 50', 'CNX NIFTY 200', 'CERTUS BUY', 'CERTUS SELL',
                        'VELOX BUY', 'VELOX SELL', 'FUTURO BUY', 'FUTURO SELL', 'SHORT BUY', 'SHORT SELL', 'MID BUY', 'MID SELL', 'LONG BUY', 'LONG SELL',
                        'XSHORT BUY', 'XSHORT SELL', 'XLONG BUY', 'XLONG SELL', 'CERTUS-VELOX BUY',
                        'CERTUS-VELOX SELL', 'FUTURO-VELOX BUY','FUTURO-VELOX SELL', 'CERTUS-FUTURO BUY', 'CERTUS-FUTURO SELL']
        self.filter_selector.addItems(filters_list)

    def load_companies(self):
        company_filter = self.filter_selector.currentText()
        self.company_selector.clear()
        if company_filter != 'Select':
            filtered_companies = self.db_obj.get_companies_from_filter(company_filter)
            self.company_selector.addItems(filtered_companies)

    def load_company_data(self):
        selected_company = self.company_selector.currentText()
        if not selected_company:
            return
        self.all_data = self.db_obj.get_company_data(selected_company)
        self.render_graph()
        self.company_val.setText(selected_company)
        self.company_val.setStyleSheet('color: blue')
        self.table_data.setRowCount(len(self.all_data))
        self.table_data.setColumnCount(len(self.all_data[0]))
        self.table_data.verticalScrollBar().setValue(self.table_data.verticalScrollBar().maximum())
        self.table_data.setHorizontalHeaderLabels(['DATE',' OPEN    ',u' HIGH    ',u' LOW     ',u' CLOSE   ','SHRT_SIG','SHRT_AVG','SHRT %','MID_SIG','MID_AVG','MID %',
                                                   'LONG_SIG','LONG_AVG','LONG %','CERTUS','VELOX','FUTURO','PIVOT','PIVOT %','STOCH','MACD','MACD %','MACD_D %',
                                                   'EX_SHRT_SIG','EX_SHRT_AVG','EX_SHRT %','QUANTITY','TRADERS','EX_LONG_SIG','EX_LONG_AVG','MNTM','MNTM %'])

        self.table_data.resizeColumnsToContents()
        self.table_data.resizeRowsToContents()
        self.table_data.setColumnWidth(0, 80)

        for i, row in enumerate(self.all_data):
            for j, col in enumerate(row):
                if col is None:
                    col = ''
                if j in (5,8,11, 14,15,16,23,28):
                    col = self.get_signal(col)
                item = QtGui.QTableWidgetItem(str(col))
                self.table_data.setItem(i,j,item)
                if col == 'BUY':
                        self.table_data.item(i,j).setBackground(QtGui.QColor(51,255,51))
                elif col == 'SELL':
                    self.table_data.item(i,j).setBackground(QtGui.QColor(255,127,80))
                elif col == 'IGNIS':
                    self.table_data.item(i,j).setBackground(QtGui.QColor(70,130,180))

        highlight_list = self.all_data[len(self.all_data)-1]
        self.set_front_details(highlight_list)

    def set_front_details(self, highlight_list):
        self.open_val.setText(str(highlight_list[1]))
        self.high_val.setText(str(highlight_list[2]))
        self.low_val.setText(str(highlight_list[3]))
        self.close_val.setText(str(highlight_list[4]))

        #futuro
        signal, custom_style = self.get_signal_and_color(highlight_list[16])
        self.futuro_val.setText(signal)
        self.futuro_val.setStyleSheet(custom_style)

        #velox
        signal, custom_style = self.get_signal_and_color(highlight_list[15])
        self.velox_val.setText(signal)
        self.velox_val.setStyleSheet(custom_style)

        #certus
        signal, custom_style = self.get_signal_and_color(highlight_list[14])
        self.certus_val.setText(signal)
        self.certus_val.setStyleSheet(custom_style)

        #short term
        signal, custom_style = self.get_signal_and_color(highlight_list[5])
        self.short_val.setText(signal)
        self.short_val.setStyleSheet(custom_style)

        #mid term
        signal, custom_style = self.get_signal_and_color(highlight_list[8])
        self.mid_val.setText(signal)
        self.mid_val.setStyleSheet(custom_style)

        #long term
        signal, custom_style = self.get_signal_and_color(highlight_list[23])
        self.long_val.setText(signal)
        self.long_val.setStyleSheet(custom_style)

        self.pivot_change_val.setText(str(highlight_list[18]))
        self.momentum_change_val.setText(str(highlight_list[31]))
        self.stochastic_val.setText(str(highlight_list[19]))

        self.macd_change_val.setText(str(highlight_list[21]))
        self.short_term_change_val.setText(str(highlight_list[7]))


    def get_signal_and_color(self, signal_id):
        red = 'color: red'
        green = 'color: green'
        yellow = 'color: yellow'
        blue = 'color: RoyalBlue'
        if signal_id == 1:
            return 'BUY', green
        elif signal_id == 2:
            return 'UP', green
        elif signal_id == 3:
            return 'SELL', red
        elif signal_id == 4:
            return 'DOWN', red
        elif signal_id == 5:
            return 'IGNIS',blue
        else:
            return '--', yellow

    def get_signal(self, signal_id):
        if signal_id == 1:
            return 'BUY'
        elif signal_id == 2:
            return 'UP'
        elif signal_id == 3:
            return 'SELL'
        elif signal_id == 4:
            return 'DOWN'
        elif signal_id == 5:
            return 'IGNIS'
        else:
            return '---'

    def render_graph(self):
        self.web_view.loadFinished.connect(self.render_on_load)
        self.web_view.load('index.html')
        self.web_view.show()

    def render_on_load(self):
        plot_data = ""
        for item in self.all_data:
            plot_data += item[0] + "," + str(item[4]) + "," + str(item[6]) + "," + str(item[9]) + "," + str(item[12]) + \
                         "," + str(item[19]) + "|"
        plot_data = plot_data.replace("-","/")
        print plot_data
        self.my_page = self.web_view.page()
        self.my_frame = self.my_page.mainFrame()
        #self.my_frame.addToJavaScriptWindowObject("python_obj", self)
        self.my_frame.evaluateJavaScript("plot_avg('"+plot_data+"');")
        self.my_frame.evaluateJavaScript("plot_stoch('"+plot_data+"')")
