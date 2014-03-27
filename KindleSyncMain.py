# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'KindleSyncMain.ui'
#
# Created: Thu Mar 27 03:39:27 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(687, 535)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tableViewLibrary = QtGui.QTableView(self.centralwidget)
        self.tableViewLibrary.setGeometry(QtCore.QRect(10, 10, 661, 391))
        self.tableViewLibrary.setObjectName(_fromUtf8("tableViewLibrary"))
        self.btnEpMoAll = QtGui.QPushButton(self.centralwidget)
        self.btnEpMoAll.setGeometry(QtCore.QRect(10, 400, 151, 91))
        self.btnEpMoAll.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("images/epToMoAll.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnEpMoAll.setIcon(icon)
        self.btnEpMoAll.setIconSize(QtCore.QSize(128, 64))
        self.btnEpMoAll.setCheckable(False)
        self.btnEpMoAll.setAutoDefault(False)
        self.btnEpMoAll.setDefault(True)
        self.btnEpMoAll.setFlat(False)
        self.btnEpMoAll.setObjectName(_fromUtf8("btnEpMoAll"))
        self.btnEpMoSel = QtGui.QPushButton(self.centralwidget)
        self.btnEpMoSel.setGeometry(QtCore.QRect(160, 400, 151, 91))
        self.btnEpMoSel.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("images/epToMoSel.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnEpMoSel.setIcon(icon1)
        self.btnEpMoSel.setIconSize(QtCore.QSize(128, 64))
        self.btnEpMoSel.setCheckable(False)
        self.btnEpMoSel.setAutoDefault(False)
        self.btnEpMoSel.setDefault(True)
        self.btnEpMoSel.setFlat(False)
        self.btnEpMoSel.setObjectName(_fromUtf8("btnEpMoSel"))
        self.btnUploadSel = QtGui.QPushButton(self.centralwidget)
        self.btnUploadSel.setGeometry(QtCore.QRect(520, 400, 151, 91))
        self.btnUploadSel.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("images/upToKinSel.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnUploadSel.setIcon(icon2)
        self.btnUploadSel.setIconSize(QtCore.QSize(128, 64))
        self.btnUploadSel.setCheckable(False)
        self.btnUploadSel.setAutoDefault(False)
        self.btnUploadSel.setDefault(True)
        self.btnUploadSel.setFlat(False)
        self.btnUploadSel.setObjectName(_fromUtf8("btnUploadSel"))
        self.btnUploadAll = QtGui.QPushButton(self.centralwidget)
        self.btnUploadAll.setGeometry(QtCore.QRect(370, 400, 151, 91))
        self.btnUploadAll.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("images/upToKinAll.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnUploadAll.setIcon(icon3)
        self.btnUploadAll.setIconSize(QtCore.QSize(128, 64))
        self.btnUploadAll.setCheckable(False)
        self.btnUploadAll.setAutoDefault(False)
        self.btnUploadAll.setDefault(True)
        self.btnUploadAll.setFlat(False)
        self.btnUploadAll.setObjectName(_fromUtf8("btnUploadAll"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 687, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Kindle Sync", None))

import KindleConvert_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

