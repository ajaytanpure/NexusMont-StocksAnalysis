import sys
from PySide.QtCore import QObject, Slot
from PySide.QtGui import QApplication
from PySide.QtWebKit import QWebView


html = """
<html>
<body>

<h1>JavaScript Can Validate Input</h1>
<script language="javascript" type="text/javascript">
    function AmIcalled(){
        alert("Yes, I am called")
    }
</script>
</body>
</html>

"""

class ConsolePrinter(QObject):
    def __init__(self, parent=None):
        super(ConsolePrinter, self).__init__(parent)

    @Slot(str)
    def text(self, message):
        print message

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = QWebView()
    frame = view.page().mainFrame()
    printer = ConsolePrinter()
    view.setHtml(html)
    #frame.addToJavaScriptWindowObject('printer', printer)
    frame.evaluateJavaScript("AmICalled()")
    #frame.evaluateJavaScript("printer.text('Goooooooooo!');")
    view.show()
    app.exec_()
