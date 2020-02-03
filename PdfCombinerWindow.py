# coding=utf-8

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

import combinePDF.GUI.PDFMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui=combinePDF.GUI.PDFMainWindow.Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.setWindowTitle("合并pdf")

    mainWindow.show()
    sys.exit(app.exec_())

