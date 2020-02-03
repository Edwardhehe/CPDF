# coding=utf-8
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger


def merge_pdfs(pdfs_files, output):
    result_pdfs = PdfFileMerger()
    for pdf in pdfs_files:
        with open(pdf, 'rb') as fp:
            pdf_reader = PdfFileReader(fp)
            if pdf_reader.isEncrypted:
                continue
            result_pdfs .append(pdf_reader, import_bookmarks=True)
    result_pdfs .write(output)
    result_pdfs .close()


if __name__ == '__main__':
    paths = ['C:/Users/lihao/Desktop/pdfs/小米电子发票.pdf',
             'C:/Users/lihao/Desktop/pdfs/out1.pdf']
    merge_pdfs(paths, 'C:/Users/lihao/Desktop/pdfs/out2.pdf')
