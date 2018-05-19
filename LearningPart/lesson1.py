from PyQt4 import QtGui,QtCore
import sys
"""
def main():
    app = QtGui.QApplication(sys.argv)
    
    w = QtGui.QWidget()
    w.resize(250,150)
    w.move(300,300)
    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 

"""

class Example(QtGui.QWidget):
   
    def __init__(self):
        super(Example,self).__init__()
        self.initUI()

    def initUI(self):
        """
        self.setGeometry(300,300,250,150)
        self.setWindowTitle("Icon")
        self.setWindowIcon(QtGui.QIcon('./RE1Mu3b.png'))

        self.show()
        """
        """
        #QtGui.QToolTip.setFont(QtGui.QFont("SansSerif",10))
        #self.setToolTip("This is a <b>QWidget</b> widget")

        btn = QtGui.QPushButton("Quit",self)
        btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        btn.setToolTip("This is a <b>QPushButton</b> widget")
        btn.resize(btn.sizeHint())
        btn.move(50,50)
        """
        
        self.setGeometry(300,300,1200,750)
        self.setWindowTitle("Tooltips")
        self.show()

    def closeEvent(self,event):

        reply = QtGui.QMessageBox.question(self,"Message",
            "Are you sure to exit?",QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No,QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()   
