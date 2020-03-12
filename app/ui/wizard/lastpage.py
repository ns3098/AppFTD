
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class LastPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(LastPage, self).__init__(parent)

        self.setObjectName(self.__class__.__name__)

        self.layout = QtWidgets.QVBoxLayout()

        self.icon = QtWidgets.QLabel(self)
        self.icon.setPixmap(QPixmap(':/icons/wizard_set.png'))
        self.icon.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.title_label = QtWidgets.QLabel("You're all set !\n", self)
        self.title_label.setStyleSheet("QLabel {color: #6F8DA6; font: 60px 'capsuula';}")
        self.title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.layout.addStretch()
        self.layout.addWidget(self.icon)
        self.layout.addStretch()
        self.layout.addWidget(self.title_label)

        self.setLayout(self.layout)
