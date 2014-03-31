# -*- coding: utf-8 -*-
#
# 2014 Alex Silva <alexsilvaf28 at gmail.com>

from PyQt4 import QtCore, QtGui
import webbrowser

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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(281, 298)
        flags = QtCore.Qt.Tool | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.CustomizeWindowHint 
        Dialog.setWindowFlags(flags)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 265, 141, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.btnLicense = QtGui.QPushButton(Dialog)
        self.btnLicense.setGeometry(QtCore.QRect(160, 260, 114, 32))
        self.btnLicense.setObjectName(_fromUtf8("btnLicense"))

        self.btnLicense.clicked.connect(lambda: webbrowser.open("http://www.gnu.org/licenses/old-licenses/gpl-2.0-standalone.html"))

        self.textEdit = QtGui.QTextBrowser(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(0, 110, 281, 131))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.textEdit.setReadOnly(True)
        self.textEdit.setOpenExternalLinks(True)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(110, 30, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(23)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(160, 70, 31, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.labelIcon = QtGui.QLabel(Dialog)
        self.labelIcon.setGeometry(QtCore.QRect(20, 10, 71, 91))
        self.labelIcon.setText(_fromUtf8(""))
        self.labelIcon.setObjectName(_fromUtf8("labelIcon"))
        self.appIcon = QtGui.QImage(_fromUtf8("images/icon.png"))
        self.appIcon = self.appIcon.scaledToHeight(90)
        self.labelIcon.setPixmap(QtGui.QPixmap.fromImage(self.appIcon))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        self.label.setText(_translate("Dialog", "GPLv2 2014 - Alex Silva", None))
        self.btnLicense.setText(_translate("Dialog", "Licencia", None))
        self.textEdit.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.Lucida Grande UI\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:600;\">Autor</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Alex Silva &lt;<a href=\"mailto:alexsilvaf28@gmail.com\"><span style=\" text-decoration: underline; color:#0000ff;\">alexsilvaf28@gmail.com</span></a>&gt;</p>\n"
"<p style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:600;\">Web</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://alexsays.github.io/Kindle-Sync/\"><span style=\" text-decoration: underline; color:#0000ff;\">http://alexsays.github.io/Kindle-Sync/</span></a></p></body></html>", None))
        self.label_2.setText(_translate("Dialog", "Kindle Sync", None))
        self.label_3.setText(_translate("Dialog", "1.0a", None))

