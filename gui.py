# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(515, 458)
        MainWindow.setMinimumSize(QtCore.QSize(400, 300))
        MainWindow.setAcceptDrops(False)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.startTestButton = QtWidgets.QPushButton(self.centralwidget)
        self.startTestButton.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.startTestButton.setFont(font)
        self.startTestButton.setObjectName("startTestButton")
        self.verticalLayout.addWidget(self.startTestButton)
        self.statusInfo = QtWidgets.QTextEdit(self.centralwidget)
        self.statusInfo.setReadOnly(True)
        self.statusInfo.setPlaceholderText("")
        self.statusInfo.setObjectName("statusInfo")
        self.verticalLayout.addWidget(self.statusInfo)
        self.status_labels = QtWidgets.QHBoxLayout()
        self.status_labels.setObjectName("status_labels")
        self.loadingIcon = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadingIcon.sizePolicy().hasHeightForWidth())
        self.loadingIcon.setSizePolicy(sizePolicy)
        self.loadingIcon.setMaximumSize(QtCore.QSize(16777215, 20))
        self.loadingIcon.setScaledContents(False)
        self.loadingIcon.setObjectName("loadingIcon")
        self.status_labels.addWidget(self.loadingIcon)
        self.connectionStatus = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connectionStatus.sizePolicy().hasHeightForWidth())
        self.connectionStatus.setSizePolicy(sizePolicy)
        self.connectionStatus.setMaximumSize(QtCore.QSize(16777215, 20))
        self.connectionStatus.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.connectionStatus.setObjectName("connectionStatus")
        self.status_labels.addWidget(self.connectionStatus)
        self.verticalLayout.addLayout(self.status_labels)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionstart_test = QtWidgets.QAction(MainWindow)
        self.actionstart_test.setCheckable(False)
        self.actionstart_test.setEnabled(True)
        self.actionstart_test.setObjectName("actionstart_test")

        self.retranslateUi(MainWindow)
        self.startTestButton.released.connect(self.actionstart_test.trigger)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Schleich Report Downloader"))
        self.startTestButton.setText(_translate("MainWindow", "Start Test"))
        self.statusInfo.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.loadingIcon.setText(_translate("MainWindow", "TextLabel"))
        self.connectionStatus.setText(_translate("MainWindow", "TextLabel"))
        self.actionstart_test.setText(_translate("MainWindow", "start_test"))
        self.actionstart_test.setToolTip(_translate("MainWindow", "Starts a test using the currently selected test protocol and waits for its end"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
