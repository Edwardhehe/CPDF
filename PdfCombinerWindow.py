# coding=utf-8

import sys

from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

import combinePDF.GUI.PDFMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = combinePDF.GUI.PDFMainWindow.Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.setWindowTitle("合并pdf")
    # 设置图标
    mainWindow.setWindowIcon(QIcon(QFileInfo(__file__).absolutePath()
                                   + '/images/favicon.ico'))
    mainWindow.setFixedSize(640, 400)

    mainWindow.show()
    sys.exit(app.exec_())
