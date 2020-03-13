

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

from app.utils.widgets.widgetanimation import FadeAnimation


class WelcomeWizardPage(FadeAnimation, QtWidgets.QWizardPage):

    fade_out_finished = pyqtSignal()

    def __init__(self, parent=None):
        super(WelcomeWizardPage, self).__init__(parent, start_value=0)

        self.setObjectName(self.__class__.__name__)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.principal_label = QtWidgets.QLabel("Hi There,", self)
        self.principal_label.setStyleSheet("QLabel {color: #6F8DA6; font: 70px 'capsuula';margin : -50px}")
        self.principal_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.title_label = QtWidgets.QLabel("Welcome to the Application\n", self)
        self.title_label.setStyleSheet("QLabel {color: #6F8DA6; font: 50px 'capsuula';}")
        self.title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.under_label = QtWidgets.QLabel("This wizard helps you to get familiar with the program for the first time. \n"
                                            "Read all the instructions and features carefully.", self)
        self.under_label.setStyleSheet("color: #6F8DA6; font: 30px 'capsuula';")
        self.under_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.main_layout.addWidget(self.principal_label)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.under_label)
        self.timer = QTimer()

        self._fade_in()

    def _fade_in(self):
        """
        Activate the fade in animation.

        :return:
        """
        self.fade_in(2000)
