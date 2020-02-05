# -*- coding: utf-8 -*-
"""
主界面及合并pdf方法
"""

import os
import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QMenu, QAction

from combinePDF.GUI.MergePDFs import PdfMergerThread


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

        # 给listWidget加右键菜单
        self.pdf_listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.pdf_listWidget.customContextMenuRequested[QtCore.QPoint].connect(self.contextmenu_listWidget)
        # 注册按钮信息
        self.regist_action()

    def contextmenu_listWidget(self):
        rightMenu = QMenu(self.pdf_listWidget)

        self.action_delete = QAction(u'删除')
        self.action_sort = QAction(u'正向排序')
        self.action_sort_reverse = QAction(u'反向排序')

        rightMenu.addAction(self.action_delete)
        rightMenu.addAction(self.action_sort)
        rightMenu.addAction(self.action_sort_reverse)

        # 链接方法：
        self.action_sort_reverse.triggered.connect(self.sort_reverse_list_widget)
        self.action_sort.triggered.connect(self.sort_list_widget)
        self.action_delete.triggered.connect(self.delete_list_widget)

        rightMenu.exec_(QCursor.pos())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "合并pdf"))
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
        self.filename_list = self.filename_list + openfileNames[0]
        self.statusBar.showMessage("导入" + str(len(self.filename_list)) + "个pdf文件成功")
        self.pdf_listWidget.addItems(openfileNames[0])

    def combine_pdf_action(self):
        """
        合并pdf按钮动作
        :return:
        """
        if self.filename_list:
            parent_name = os.path.dirname(self.filename_list[0])
            output_filename = parent_name + '/' + self.filename_lineedit.text()
            print(output_filename)
            # 启动pdf合并线程及线程通讯
            self.pdfMerge_thread = PdfMergerThread(self.filename_list, output_filename)
            self.pdfMerge_thread.progressBarValue.connect(self.update_processBar)
            self.pdfMerge_thread.work_status.connect(self.update_statusBar)
            self.pdfMerge_thread.start()

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

    def update_processBar(self, i):
        self.progressBar_instatucBar.setValue(i)

    def update_statusBar(self, message):
        self.statusBar.showMessage(message)

    def delete_list_widget(self):
        """
        :param pos:
        :param x: x坐标
        :param y: y坐标
        :return:
        """
        items = self.pdf_listWidget.selectedItems()
        if len(items) > 0:
            index = self.pdf_listWidget.selectedIndexes()[0].row()
            self.filename_list.pop(index)
            print(index)
            self.pdf_listWidget.takeItem(index)
        else:
            self.statusBar.showMessage("未选中对象！")

    def sort_list_widget(self):
        """
        正向排序
        :return:
        """
        self.pdf_listWidget.sortItems(Qt.AscendingOrder)
        self.filename_list.sort(reverse=False)

    def sort_reverse_list_widget(self):
        """
        反向排序
        :return:
        """
        self.pdf_listWidget.sortItems(Qt.DescendingOrder)
        self.filename_list.sort(reverse=True)
