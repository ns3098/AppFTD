
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime, QTimer


class TimeLabel(QtWidgets.QLabel):
    """
    Simple label that prints time.
    """

    def __init__(self, parent=None):
        super(TimeLabel, self).__init__(parent)

        self.setObjectName(self.__class__.__name__)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.__display_time)
        self.timer.start()

        self.__display_time()

    def __display_time(self):
        self.setText(QTime.currentTime().toString())
