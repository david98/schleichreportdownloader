from schleichore import TestManager

from PyQt5 import QtCore, QtGui, QtWidgets


class UiMainWindow(object):

    def __init__(self, test_manager: TestManager):
        self.test_manager = test_manager

        self.central_widget = None
        self.vertical_layout = None
        self.start_test_button = None
        self.text_box = None
        self.status_labels = None
        self.loading_icon = None
        self.connection_status = None
        self.action_start_test = None
        self.status_bar = None

        self.spinner = QtGui.QMovie('spinner.gif')

    def on_text_feedback_update(self, new_text: str):
        self.text_box.setText(new_text)

    def on_status_feedback_update(self, new_text: str):
        self.connection_status.setText(new_text)

    def on_set_loading_indicator_enable(self, enabled: bool):
        if enabled:
            self.loading_icon.setMovie(self.spinner)
            self.spinner.start()
        else:
            self.loading_icon.clear()

    def on_set_start_test_enable(self, enabled: bool):
        self.start_test_button.setEnabled(enabled)

    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.setMinimumSize(QtCore.QSize(400, 300))
        main_window.setAcceptDrops(False)
        main_window.setAutoFillBackground(False)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("centralwidget")
        self.vertical_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.vertical_layout.setObjectName("verticalLayout")
        self.start_test_button = QtWidgets.QPushButton(self.central_widget)
        self.start_test_button.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.start_test_button.setFont(font)
        self.start_test_button.setObjectName("startTestButton")
        self.vertical_layout.addWidget(self.start_test_button)

        self.test_manager.start_test_control.set_start_test_enable.connect(self.on_set_start_test_enable)

        self.text_box = QtWidgets.QTextEdit(self.central_widget)

        self.test_manager.text_feedback.text_feedback_update.connect(self.on_text_feedback_update)

        self.text_box.setReadOnly(True)
        self.text_box.setObjectName("statusInfo")
        self.vertical_layout.addWidget(self.text_box)
        self.status_labels = QtWidgets.QHBoxLayout()
        self.status_labels.setObjectName("status_labels")
        self.loading_icon = QtWidgets.QLabel(self.central_widget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.loading_icon.sizePolicy().hasHeightForWidth())
        self.loading_icon.setSizePolicy(size_policy)
        self.loading_icon.setMaximumSize(QtCore.QSize(16777215, 25))
        self.loading_icon.setScaledContents(False)
        self.loading_icon.setObjectName("loadingIcon")
        self.status_labels.addWidget(self.loading_icon)
        self.connection_status = QtWidgets.QLabel(self.central_widget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.connection_status.sizePolicy().hasHeightForWidth())
        self.connection_status.setSizePolicy(size_policy)
        self.connection_status.setMaximumSize(QtCore.QSize(16777215, 25))
        self.connection_status.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.connection_status.setObjectName("connectionStatus")
        self.status_labels.addWidget(self.connection_status)
        self.vertical_layout.addLayout(self.status_labels)

        self.test_manager.status_feedback.status_feedback_update.connect(self.on_status_feedback_update)
        self.test_manager.loading_indicator.set_loading_indicator_enable.connect(self.on_set_loading_indicator_enable)

        main_window.setCentralWidget(self.central_widget)
        self.status_bar = QtWidgets.QStatusBar(main_window)
        self.status_bar.setObjectName("statusbar")
        main_window.setStatusBar(self.status_bar)
        self.action_start_test = QtWidgets.QAction(main_window)
        self.action_start_test.setCheckable(False)
        self.action_start_test.setEnabled(True)
        self.action_start_test.setObjectName("actionstart_test")

        self.retranslate_ui(main_window)
        self.action_start_test.trigger = self.test_manager.start
        self.start_test_button.released.connect(self.action_start_test.trigger)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Schleich Report Downloader"))
        self.start_test_button.setText(_translate("MainWindow", "Start Test"))
        self.text_box.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.action_start_test.setText(_translate("MainWindow", "start_test"))
        self.action_start_test.setToolTip(_translate("MainWindow", "Starts a test using the currently selected test protocol and waits for its end"))
        self.test_manager.ready()
