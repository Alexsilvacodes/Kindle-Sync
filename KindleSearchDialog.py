# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'KindleSearchDialog.ui'
#
# Created: Thu Apr  3 16:24:23 2014
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

class Ui_SearchDialog(QtGui.QDialog):
    closeSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None, flags=QtCore.Qt.Dialog):
        super(Ui_SearchDialog, self).__init__(parent, flags)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(280, 320)
        Dialog.setMinimumSize(QtCore.QSize(280, 320))
        Dialog.setMaximumSize(QtCore.QSize(280, 320))
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        flags = QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.CustomizeWindowHint
        Dialog.setWindowFlags(flags)
        self.image_label = QtGui.QLabel(Dialog)
        self.image_label.setGeometry(QtCore.QRect(0, 0, 280, 320))
        self.image_label.setText(_fromUtf8(""))
        self.image_label.setObjectName(_fromUtf8("image_label"))
        self.text_label = QtGui.QLabel(Dialog)
        self.text_label.setGeometry(QtCore.QRect(11, 270, 261, 41))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Futura"))
        font.setPointSize(24)
        self.text_label.setFont(font)
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)
        self.text_label.setObjectName(_fromUtf8("text_label"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(0, 300, 21, 21))
        self.pushButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("images/close-button.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(21, 21))
        self.pushButton.setStyleSheet("QPushButton, QPushButton:disabled, QPushButton:focus:pressed { border:transparent; background-color:white; }")
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.setVisible(False)
        self.pushButton.clicked.connect(self.closeSignal.emit)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def closeClicked(self):
        print "clicked"
        self.closeSignal.emit()

    def setStatus(self, status):
        self.pushButton.setVisible(True)
        if status:
            self.image_label.setPixmap(QtGui.QPixmap(_fromUtf8("images/unplug-usb.png")))
            self.text_label.setText(_fromUtf8("Desconecta el kindle"))
        else:
            self.image_label.setPixmap(QtGui.QPixmap(_fromUtf8("images/plugin-usb.png")))
            self.text_label.setText(_fromUtf8("Conecta el kindle"))

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Buscando Kindle...", None))
