#skelton code from http://pythonforengineers.com/your-first-gui-app-with-python-and-pyqt/

import sys
from PyQt4 import QtCore, QtGui, uic

qtCreatorFile = "tiltshift.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):

    def cmdHBar_clicked(self):
        print "HBarClicked"

    def cmdVBar_clicked(self):
        print "VBarClicked"

    def cmdCircle_clicked(self):
        print "Circle"

    def chkSaturate_clicked(self):
        print "Saturate"

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.cmdHBar.clicked.connect(self.cmdHBar_clicked)
        self.cmdVBar.clicked.connect(self.cmdVBar_clicked)
        self.cmdCircle.clicked.connect(self.cmdCircle_clicked)
        self.chkSaturate.clicked.connect(self.chkSaturate_clicked)

        self.graphicsView.scene = QtGui.QGraphicsScene(self)
        self.item = QtGui.QGraphicsEllipseItem(50, 50, 40, 20)
        self.graphicsView.scene.addItem(self.item)
        self.graphicsView.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())