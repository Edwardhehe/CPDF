import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QProgressBar, QMainWindow


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(800, 600)

#        self.lb=QLabel('finding resource   ')

        self.pb = QProgressBar()
        self.pb.setRange(0, 0)
#        self.pb.setTextVisible(False)

#        self.statusBar().addPermanentWidget(self.lb)
        self.statusBar().setSizeGripEnabled(False)
#        print(self.statusBar().layout() )
        self.statusBar().setStyleSheet("QStatusBar::item {border: none;}")
        self.statusBar().addPermanentWidget(self.pb, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())