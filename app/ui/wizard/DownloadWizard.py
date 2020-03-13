

from PyQt5 import QtWidgets,QtGui
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

from app.utils.widgets.widgetanimation import FadeAnimation
import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPalette
from PyQt5.QtWidgets import QApplication, qApp

from qroundprogressbar import QRoundProgressBar

class DownloadWizardPage(FadeAnimation, QtWidgets.QWizardPage):

    fade_out_finished = pyqtSignal()

    def __init__(self, parent=None):
        super(DownloadWizardPage, self).__init__(parent, start_value=0)

        self.setObjectName(self.__class__.__name__)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.hlayout = QtWidgets.QHBoxLayout()
        self.main_layout.setSpacing(0)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        self.progress = QRoundProgressBar()
        self.progress.setBarStyle(QRoundProgressBar.BarStyle.LINE)


        self.progress.setStyleSheet("background-color: rgba(22, 31, 38, 1);color:gray;font-size:10pt;")

        #self.main_layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        #self.progress.setPalette(palette)
        #self.progress.show()
        self.hlayout.addWidget(self.progress)
        #self.hlayout.setAlignment(Qt.AlignCenter)
        self.main_layout.addLayout(self.hlayout)


        self._fade_in()
        self.timer = QTimer()



    def _fade_in(self):
        """
        Activate the fade in animation.

        :return:
        """
        self.fade_in(2000)
