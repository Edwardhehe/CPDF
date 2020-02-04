# -*- coding: utf-8 -*-
"""
合并pdf多线程类
"""
from PyQt5.QtCore import QThread, pyqtSignal
from pdfrw import PdfWriter, PdfReader


class PdfMergerThread(QThread):
    """
    pdf合并累，采用多线程模式，可以更新进度条
    """
    progressBarValue = pyqtSignal(int)  # 更新进度条
    work_status = pyqtSignal(object)  # 任务状态信号

    def __init__(self, pdfs_files, output):
        super(PdfMergerThread, self).__init__()
        self.pdfs_files = pdfs_files
        self.output = output

    def run(self):
        """
        重写线程run方法
        :return:
        """
        self.merge_pdfs(self.pdfs_files, self.output)

    def merge_pdfs(self, pdfs_files, output):
        """
        合并pdf函数
        :param pdfs_files: 输入待合并的文件名数组
        :param output: 输出文件名
        :return:
        """
        total = len(pdfs_files)
        progress_signal = 1
        self.progressBarValue.emit(progress_signal / total * 100)

        writer = PdfWriter()
        for input_filename in pdfs_files:
            try:
                writer.addpages(PdfReader(input_filename).pages)
                progress_signal += 1  # 更新进度条信号
                self.progressBarValue.emit(progress_signal / total * 100)  # 发信号
            except Exception as e:
                self.work_status.emit("导入文件" + input_filename + "失败")

        try:
            writer.write(output)
            self.work_status.emit("合并pdf文件成功! 文件位置：" + output)
        except Exception as e:
            self.work_status.emit("合并失败！" + "原因可能是: 文件名：" + output + "被占用")
