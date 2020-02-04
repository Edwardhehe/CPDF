# -*- coding: utf-8 -*-

import os
import time
import traceback

from PyPDF2 import PdfFileMerger, PdfFileReader
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setWindowIcon(QIcon('../../images/favicon.ico'))
        MainWindow.resize(640, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 640, 378))
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pdf_listWidget = QtWidgets.QListWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pdf_listWidget.sizePolicy().hasHeightForWidth())
        self.pdf_listWidget.setSizePolicy(sizePolicy)
        self.pdf_listWidget.setObjectName("pdf_listWidget")
        self.horizontalLayout.addWidget(self.pdf_listWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(9, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.import_pushButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.import_pushButton.sizePolicy().hasHeightForWidth())
        self.import_pushButton.setSizePolicy(sizePolicy)
        self.import_pushButton.setObjectName("import_pushButton")
        self.verticalLayout.addWidget(self.import_pushButton)

        self.inputFileName_label = QtWidgets.QLabel(self.frame)
        self.inputFileName_label.setText("请输入合并后的文件名：")
        self.verticalLayout.addWidget(self.inputFileName_label)
        self.inputFileName_label.setSizePolicy(sizePolicy)

        self.filename_lineedit = QtWidgets.QLineEdit(self.frame)
        self.filename_lineedit.setObjectName("filename_lineedit")
        self.verticalLayout.addWidget(self.filename_lineedit)
        self.conbinepdf_pushButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.conbinepdf_pushButton.sizePolicy().hasHeightForWidth())
        self.conbinepdf_pushButton.setSizePolicy(sizePolicy)
        self.conbinepdf_pushButton.setObjectName("conbinepdf_pushButton")
        self.verticalLayout.addWidget(self.conbinepdf_pushButton)

        self.reset_pushbutton = QtWidgets.QPushButton(self.frame)
        self.reset_pushbutton.setText("重置pdf")
        self.verticalLayout.addWidget(self.reset_pushbutton)
        self.reset_pushbutton.setSizePolicy(sizePolicy)

        spacerItem = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.filename_lineedit.setText(time.strftime("%Y-%m-%d", time.localtime(time.time())) +
                                       '合并后的.pdf')
        self.filename_list = []  # 文件列表

        # 状态栏进度条
        self.progressBar_instatucBar = QtWidgets.QProgressBar()
        self.progressBar_instatucBar.setSizePolicy(sizePolicy)
        self.progressBar_instatucBar.setRange(0, 100)

        self.progressBar_instatucBar.setTextVisible(False)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.addPermanentWidget(self.progressBar_instatucBar, 0)

        self.regist_action()  # 注册按钮信息

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.import_pushButton.setText(_translate("MainWindow", "导入文件"))
        self.conbinepdf_pushButton.setText(_translate("MainWindow", "合并pdf"))

    def regist_action(self):
        """
        注册动作
        :return:
        """
        self.import_pushButton.clicked.connect(self.import_pdf_action)
        self.conbinepdf_pushButton.clicked.connect(self.combine_pdf_action)
        self.reset_pushbutton.clicked.connect(self.reset_pdf_action)

    def import_pdf_action(self):
        """
        获取文件名称数组
        """
        openfileNames = QFileDialog.getOpenFileNames(self.centralwidget, '请选择要合并的pdf文件', './', '("PDF (*.pdf *.PDF)")')
        self.filename_list = openfileNames[0]
        self.statusBar.showMessage("导入" + str(len(self.filename_list)) + "个pdf文件成功")
        self.pdf_listWidget.addItems(self.filename_list)

    def combine_pdf_action(self):
        """
        合并pdf动作
        :return:
        """
        if self.filename_list:
            parent_name = os.path.dirname(self.filename_list[0])
            output_filename = parent_name + '/' + self.filename_lineedit.text()
            print(output_filename)
            try:
                self.merge_pdfs(self.filename_list, output_filename)
                self.statusBar.showMessage("合并pdf文件成功文件位置：" + output_filename)
            except Exception as e:
                traceback.print_exc()
                print("合并失败！")
                print("Error: 文件名：" + output_filename + "被占用")
                self.statusBar.showMessage("合并失败！" + "Error: 文件名：" + output_filename + "被占用")
        else:
            # 如果未选择，强行点合并文件
            msgBox = QMessageBox()
            msgBox.setWindowTitle('错误')
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("未选择PDF文件")
            msgBox.exec()
            self.statusBar.showMessage("未选择pdf文件")

    def reset_pdf_action(self):
        """
        重置全部文件
        :return:
        """
        self.filename_list = []
        self.pdf_listWidget.clear()

    @staticmethod
    def merge_pdfs(pdfs_files, output):
        result_pdfs = PdfFileMerger()

        for pdf in pdfs_files:
            with open(pdf, 'rb') as fp:
                pdf_reader = PdfFileReader(fp)
                if pdf_reader.isEncrypted:
                    continue
                result_pdfs.append(pdf_reader, import_bookmarks=True)
        result_pdfs.write(output)
        result_pdfs.close()

    def update_processBar(self, i):
        self.progressBar_instatucBar.setValue(i)


class PdfMerger(QThread):
    progressBarValue = pyqtSignal(int)  # 更新进度条

    def __init__(self):
        super(PdfMerger, self).__init__()

    def merge_pdfs(self, pdfs_files, output):
        result_pdfs = PdfFileMerger()
        total = len(pdfs_files)
        progress_signal = 1
        self.progressBarValue.emit(progress_signal / total * 100)

        for pdf in pdfs_files:
            with open(pdf, 'rb') as fp:
                pdf_reader = PdfFileReader(fp)
                if pdf_reader.isEncrypted:
                    continue
                result_pdfs.append(pdf_reader, import_bookmarks=True)
                progress_signal += 1  # 更新进度条信号
                self.progressBarValue.emit(progress_signal / total * 100)  # 发信号
        result_pdfs.write(output)
        result_pdfs.close()
