__author__ = 'Ajay'

import logging
import nexusmont_logger
from PySide import QtGui, QtCore
import sys
import home_page


def start_nexusmont():
    nexusmont_logger.set_logging()
    logging.debug("logging from main file")
    app = QtGui.QApplication(sys.argv)
    home = home_page.HomePage()
    home.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    start_nexusmont()