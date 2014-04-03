# -*- coding: utf-8 -*-
#
# 2014 Alex Silva <alexsilvaf28 at gmail.com>

from PyQt4 import QtCore, QtGui
from KindleSync import *
from AboutDialog import *
from KindleSearchDialog import *
from time import sleep
from subprocess import call
from shutil import copy2
import os, subprocess, glob

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class ConversorThread(QtCore.QThread):
    """
    Thread to do the conversion to mobi files
    Methods:
    - execTimeoutTimer(): called on timer timeout to kill long time processes
    - run(): runnable method that convert and move files
    """
    finishBookNum = QtCore.pyqtSignal(int)
    finishBookName = QtCore.pyqtSignal(QtCore.QString)
    finishWithError = QtCore.pyqtSignal(list)

    def __init__(self, indexes, books, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.indexes = indexes
        self.books = books
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.execTimeoutTimer)
        self.conv_proc = ""
        self.file_error = []
        self.flag_error = False

    def execTimeoutTimer(self):
        try:
            self.conv_proc.kill()
            self.flag_error = True
        except Exception, e:
            print e

    def run(self):
        for i in self.indexes:
            if not self.books[i]['converted']:
                self.flag_error = False
                self.timer.start(50000)
                cmd = "./kindlegen " + ibooks_folder + self.books[i]['book_file'] + " -o " + self.books[i]['book_file'].split(".")[0] + ".mobi"
                if debug: print cmd
                self.finishBookName.emit(_fromUtf8("Convirtiendo libro " + str(i+1)))
                self.conv_proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
                (stdout, stdin) = self.conv_proc.communicate()
                if "error" in stdout or self.flag_error is True:
                    self.file_error.append(str(i+1))

                try:
                    os.rename(ibooks_folder + self.books[i]['book_file'].split(".")[0] + ".mobi", ks_folder + "/ConvertedKindle/" + self.books[i]['book_file'].split(".")[0] + ".mobi")
                except Exception, e:
                    if debug: print e

                self.finishBookNum.emit(i+1)
        self.finishWithError.emit(self.file_error)


class KindleDetectorThread(QtCore.QThread):
    """
    Thread to detect Kindle connected (Mac OS)
    """
    disconnectSignal = QtCore.pyqtSignal(int)
    connectSignal = QtCore.pyqtSignal(int)
    finishSignal = QtCore.pyqtSignal(str)
    STATUS_CONNECT = 0
    STATUS_DISCONNECT = 1

    def run(self):
        disk = glob.glob("/dev/rdisk?")
        volume = glob.glob("/Volumes/*")
        update_disk = []
        update_volume = []
        connect_step = False

        while True:
            df = ""

            try:
                df = subprocess.check_output("system_profiler SPUSBDataType | grep 0x1949", shell=True)
            except subprocess.CalledProcessError, e:
                pass

            if len(df) > 0:
                update_disk = glob.glob("/dev/rdisk?")
                update_volume = glob.glob("/Volumes/*")
                diff_disk = [i for i in update_disk if not i in disk]
                diff_volume = [i for i in update_volume if not i in volume]
                # print diff
                # print disk, "", update_disk
                if len(disk) > len(update_disk):
                    disk = update_disk
                    volume = update_volume
                if len(diff_disk) > 0:
                    self.finishSignal.emit(diff_volume[0])
                    if debug: print "Kindle connected"
                    break
                if not connect_step:
                    self.disconnectSignal.emit(self.STATUS_DISCONNECT)
                    if debug: print "Disconnect kindle"
            else:
                connect_step = True
                self.connectSignal.emit(self.STATUS_CONNECT)
                if debug: print "Connect kindle"
            sleep(1)


class KindleSendThread(QtCore.QThread):
    """
    Thread to send files to Kindle
    """
    finishBook = QtCore.pyqtSignal(int)
    finishAll = QtCore.pyqtSignal(list, list)

    def __init__(self, indexes, books, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.indexes = indexes
        self.books = books

    def setKindlePath(self, path):
        self.path = path

    def run(self):
        file_error = []
        file_sent = []
        for i in self.indexes:
            if self.books[i]['converted']:
                try:
                    src = ks_folder + "/ConvertedKindle/" + self.books[i]['book_file'].split(".")[0] + ".mobi"
                    copy2(src, self.path + "/documents/" + self.books[i]['book_file'].split(".")[0] + ".mobi")
                    file_sent.append(str(i+1))
                except IOError, e:
                    file_error.append(str(i+1))
                
                self.finishBook.emit(i+1)
                sleep(0.5)
            else:
                file_error.append(str(i+1))
        self.finishAll.emit(file_sent, file_error)


class Ui_MainWindow(object):
    """
    Main Window class
    Methods:
    - setupUi: setup the MainWindow GUI
    - redrawTable: put values on QTableView
    - onClickConvertSel: slot called with button btnEpMoSel. Convert only selected books
    - onClickConvertAll: slot called with button btnEpMoAll. Convert all library books
    - onClickSendSel: slot called with button btnUploadSel. Send to kindle only selected library books
    - onClickSendAll: slot called with button btnUploadAll. Send to kindle all library books
    - showErrors: show a dialog if there's any file with conversion errors
    """

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(684, 520)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(684, 520))
        MainWindow.setMaximumSize(QtCore.QSize(684, 520))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tableViewLibrary = QtGui.QTableView(self.centralwidget)
        self.tableViewLibrary.setGeometry(QtCore.QRect(0, 0, 684, 401))
        self.tableViewLibrary.setShowGrid(False)
        self.tableViewLibrary.setCornerButtonEnabled(False)
        self.tableViewLibrary.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableViewLibrary.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableViewLibrary.setObjectName(_fromUtf8("tableViewLibrary"))
        self.tableViewLibrary.horizontalHeader().setVisible(False)
        self.tableViewLibrary.verticalHeader().setVisible(True)
        self.tableViewLibrary.verticalHeader().setMinimumSectionSize(30)
        self.tableViewLibrary.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)

        ## Changes ##
        self.model = QtGui.QStandardItemModel()
        
        self.blue_color = QtGui.QBrush(QtGui.QColor(240, 243, 249))
        self.epub_icon = QtGui.QImage(_fromUtf8("images/epub_tag.png"))
        self.mobi_icon = QtGui.QImage(_fromUtf8("images/mobi_tag.png"))
        self.mobi_icon_g = QtGui.QImage(_fromUtf8("images/mobi_tag_g.png"))
        self.redrawTable()
        #############

        self.btnEpMoAll = QtGui.QPushButton(self.centralwidget)
        self.btnEpMoAll.setGeometry(QtCore.QRect(10, 400, 151, 91))
        self.btnEpMoAll.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("images/epToMoAll.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnEpMoAll.setIcon(icon)
        self.btnEpMoAll.setIconSize(QtCore.QSize(128, 64))
        self.btnEpMoAll.setCheckable(False)
        self.btnEpMoAll.setFlat(True)
        self.btnEpMoAll.setObjectName(_fromUtf8("btnEpMoAll"))
        self.btnEpMoSel = QtGui.QPushButton(self.centralwidget)
        self.btnEpMoSel.setGeometry(QtCore.QRect(160, 400, 151, 91))
        self.btnEpMoSel.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("images/epToMoSel.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnEpMoSel.setIcon(icon1)
        self.btnEpMoSel.setIconSize(QtCore.QSize(128, 64))
        self.btnEpMoSel.setCheckable(False)
        self.btnEpMoSel.setFlat(True)
        self.btnEpMoSel.setObjectName(_fromUtf8("btnEpMoSel"))
        self.btnUploadSel = QtGui.QPushButton(self.centralwidget)
        self.btnUploadSel.setGeometry(QtCore.QRect(520, 400, 151, 91))
        self.btnUploadSel.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("images/upToKinSel.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnUploadSel.setIcon(icon2)
        self.btnUploadSel.setIconSize(QtCore.QSize(128, 64))
        self.btnUploadSel.setCheckable(False)
        self.btnUploadSel.setFlat(True)
        self.btnUploadSel.setObjectName(_fromUtf8("btnUploadSel"))
        self.btnUploadAll = QtGui.QPushButton(self.centralwidget)
        self.btnUploadAll.setGeometry(QtCore.QRect(370, 400, 151, 91))
        self.btnUploadAll.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("images/upToKinAll.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnUploadAll.setIcon(icon3)
        self.btnUploadAll.setIconSize(QtCore.QSize(128, 64))
        self.btnUploadAll.setCheckable(False)
        self.btnUploadAll.setFlat(True)
        self.btnUploadAll.setObjectName(_fromUtf8("btnUploadAll"))

        self.btnEpMoAll.clicked.connect(self.onClickConvertAll)
        self.btnEpMoSel.clicked.connect(self.onClickConvertSel)
        self.btnUploadAll.clicked.connect(self.onClickSendAll)
        self.btnUploadSel.clicked.connect(self.onClickSendSel)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 684, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        menu = self.menubar.addMenu("Kindle Sync")
        aboutAction = menu.addAction("Acerca de")
        aboutAction.setMenuRole(QtGui.QAction.AboutRole)
        aboutDialog = QtGui.QDialog(MainWindow)
        ui_about_dialog = Ui_AboutDialog()
        ui_about_dialog.setupUi(aboutDialog)
        aboutAction.triggered.connect(aboutDialog.show)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        self.statusbar.showMessage(str(len(self.books)) + " libros en tu biblioteca", 0)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Kindle Sync", None))

    def redrawTable(self):
        kindle_sync.initFolderConf()
        self.books = kindle_sync.collectiBooks()
        kindle_sync.createLibrary(self.books)
        self.model.setColumnCount(3)
        self.model.setRowCount(len(self.books))

        self.tableViewLibrary.setModel(self.model)

        if debug: self.books = [{'book_name': "1"},{'book_name': "2"},{'book_name': "3"}]

        for i,book in enumerate(self.books):
            itemCol1 = QtGui.QStandardItem(_fromUtf8(book['book_name']))
            itemCol2 = QtGui.QStandardItem()
            itemCol3 = QtGui.QStandardItem()
            itemCol1.setToolTip(_fromUtf8(book['book_name']))
            itemCol2.setToolTip(_fromUtf8(book['book_name']))
            itemCol3.setToolTip(_fromUtf8(book['book_name']))
            itemCol1.setEditable(False)
            itemCol2.setEditable(False)
            itemCol3.setEditable(False)

            itemCol2.setData(QtCore.QVariant(self.epub_icon), QtCore.Qt.DecorationRole)
            if book['converted']:
                itemCol3.setData(QtCore.QVariant(self.mobi_icon), QtCore.Qt.DecorationRole)
            else:
                itemCol3.setData(QtCore.QVariant(self.mobi_icon_g), QtCore.Qt.DecorationRole)

            if not i%2: 
                itemCol1.setBackground(self.blue_color)
                itemCol2.setBackground(self.blue_color)
                itemCol3.setBackground(self.blue_color)
            self.model.setItem(i, 0, itemCol1)
            self.model.setItem(i, 1, itemCol2)
            self.model.setItem(i, 2, itemCol3)
        if len(self.books) < 1:
            itemCol1 = QtGui.QStandardItem(_fromUtf8("La librería de iBooks está vacía..."))
            itemCol2 = QtGui.QStandardItem()
            itemCol3 = QtGui.QStandardItem()
            itemCol1.setEditable(False)
            itemCol2.setEditable(False)
            itemCol3.setEditable(False)
            itemCol1.setSelectable(False)
            itemCol2.setSelectable(False)
            itemCol3.setSelectable(False)
            self.model.setItem(i, 0, itemCol1)
            self.model.setItem(i, 1, itemCol2)
            self.model.setItem(i, 2, itemCol3)

        if len(self.books) > 13:
            tableViewWidth = self.tableViewLibrary.geometry().width()-21-17
        else:
            tableViewWidth = self.tableViewLibrary.geometry().width()-21-2
        self.tableViewLibrary.setColumnWidth(0, tableViewWidth * 0.80)
        self.tableViewLibrary.setColumnWidth(1, tableViewWidth * 0.10)
        self.tableViewLibrary.setColumnWidth(2, tableViewWidth * 0.10)

    def onClickConvertSel(self):
        index_list = self.tableViewLibrary.selectionModel().selectedRows()
        index_list_aux = []

        for index in index_list:
            index_list_aux.append(index.row())

        if len(index_list) > 0:
            progress = QtGui.QProgressDialog(MainWindow)
            progress.setRange(0, len(index_list_aux))
            progress.setWindowModality(QtCore.Qt.WindowModal)
            progress.setAutoClose(False)
            progress.setAutoReset(False)
            progress.setCancelButton(None)

            conv = ConversorThread(index_list_aux, self.books)
            conv.finished.connect(progress.close)
            conv.finished.connect(self.redrawTable)

            conv.finishBookName.connect(progress.setLabelText)
            conv.finishBookNum.connect(progress.setValue)
            conv.finishWithError.connect(self.showConversionErrors)

            conv.start()
            progress.show()

    def onClickConvertAll(self):
        index_list = range(len(self.books))

        if len(index_list) > 0:
            progress = QtGui.QProgressDialog(MainWindow)
            progress.setRange(0, len(index_list))
            progress.setWindowModality(QtCore.Qt.WindowModal)
            progress.setAutoClose(False)
            progress.setAutoReset(False)
            progress.setCancelButton(None)

            conv = ConversorThread(index_list, self.books)
            conv.finished.connect(progress.close)
            conv.finished.connect(self.redrawTable)

            conv.finishBookName.connect(progress.setLabelText)
            conv.finishBookNum.connect(progress.setValue)
            conv.finishWithError.connect(self.showConversionErrors)

            conv.start()
            progress.show()

    def onClickSendAll(self):
        # Get item list
        index_list = range(len(self.books))

        if len(index_list) > 0:
            # Prepare send and detector threads
            search_dialog = Ui_SearchDialog(MainWindow)
            progress = QtGui.QProgressDialog(MainWindow)
            progress.setRange(0, len(index_list))
            progress.setWindowModality(QtCore.Qt.WindowModal)
            progress.setAutoClose(False)
            progress.setAutoReset(False)
            progress.setCancelButton(None)
            progress.setLabelText(_fromUtf8("Enviando libros al Kindle"))

            kindle_send = KindleSendThread(index_list, self.books)
            kindle_send.finishBook.connect(progress.setValue)
            kindle_send.finishAll.connect(self.showSent)
            kindle_send.finished.connect(progress.close)

            kindle_detector = KindleDetectorThread()
            kindle_detector.finished.connect(search_dialog.close)
            kindle_detector.finishSignal.connect(lambda: self.callSend(kindle_send))
            kindle_detector.connectSignal.connect(search_dialog.setStatus)
            kindle_detector.disconnectSignal.connect(search_dialog.setStatus)
            kindle_detector.finishSignal.connect(kindle_send.setKindlePath)

            search_dialog.finished.connect(kindle_detector.terminate)
            search_dialog.closeSignal.connect(kindle_detector.terminate)

            # Show send progress
            kindle_detector.finishSignal.connect(progress.show)

            kindle_detector.start()
            search_dialog.show()

    def onClickSendSel(self):
        # Get item list
        index_list = self.tableViewLibrary.selectionModel().selectedRows()
        index_list_aux = []

        for index in index_list:
            index_list_aux.append(index.row())

        if len(index_list) > 0:
            # Prepare send and detector threads
            search_dialog = Ui_SearchDialog(MainWindow)
            progress = QtGui.QProgressDialog(MainWindow)
            progress.setRange(0, len(index_list_aux))
            progress.setWindowModality(QtCore.Qt.WindowModal)
            progress.setAutoClose(False)
            progress.setAutoReset(False)
            progress.setCancelButton(None)
            progress.setLabelText(_fromUtf8("Enviando libros al Kindle"))

            kindle_send = KindleSendThread(index_list_aux, self.books)
            kindle_send.finishBook.connect(progress.setValue)
            kindle_send.finishAll.connect(self.showSent)
            kindle_send.finished.connect(progress.close)

            kindle_detector = KindleDetectorThread()
            kindle_detector.finished.connect(search_dialog.close)
            kindle_detector.finishSignal.connect(lambda: self.callSend(kindle_send))
            kindle_detector.connectSignal.connect(search_dialog.setStatus)
            kindle_detector.disconnectSignal.connect(search_dialog.setStatus)
            kindle_detector.finishSignal.connect(kindle_send.setKindlePath)

            search_dialog.finished.connect(kindle_detector.terminate)
            search_dialog.closeSignal.connect(kindle_detector.terminate)

            # Show send progress
            kindle_detector.finishSignal.connect(progress.show)

            kindle_detector.start()
            search_dialog.show()

    def showSent(self, file_sent, file_error):
        box_errors = QtGui.QMessageBox(MainWindow)
        
        if len(file_sent) > 0 and len(file_error) < 1 :
            box_errors.setIcon(QtGui.QMessageBox.Information)
            box_errors.setText("Todos los libros se han enviado correctamente al kindle.")
        elif len(file_sent) < 1 and len(file_error) > 0 :
            box_errors.setIcon(QtGui.QMessageBox.Warning)
            box_errors.setText("No se ha podido enviar ningún libro al kindle.")
        elif len(file_sent) > 0 and len(file_error) > 0 :
            box_errors.setIcon(QtGui.QMessageBox.Warning)
            box_errors.setText("Los libros " + ", ".join(file_sent) + " se han enviado correctamente." +
                " Los libros " + ", ".join(file_error) + " no se han podido enviar.")

        box_errors.exec_()

    def callSend(self, kindle_send):
        print "calling send"
        kindle_send.start()

    def showConversionErrors(self, file_errors):
        if len(file_errors) is not 0:
            box_errors = QtGui.QMessageBox(MainWindow)
            box_errors.setIcon(QtGui.QMessageBox.Warning)
            box_errors.setText("Los libros: " + '%s' % ', '.join(map(str, file_errors)) + " no se han podido convertir.")
            box_errors.exec_()


if __name__ == "__main__":
    import sys
    kindle_sync = KindleSync()
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    app.setActiveWindow(MainWindow)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())