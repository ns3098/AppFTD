
import math

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QPainter, QBrush, QColor, QPen


class WaitingOverlay(QtWidgets.QFrame):

    def __init__(self, parent=None):
        super(WaitingOverlay, self).__init__(parent, Qt.FramelessWindowHint)

        self.counter = 0
        self.timer = QTimer()

        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Modify overlay frame color
        painter.fillRect(event.rect(), QBrush(QColor(0, 0, 0, 0)))
        painter.setPen(QPen(Qt.NoPen))
        self.resize(int(self.parent().width()), int(self.parent().height()))

        for i in range(6):
            if (self.counter / 1) % 6 == i:
                # Modify color of active bubbles
                painter.setBrush(QBrush(QColor(127 + (self.counter % 5) * 32, 187, 187)))
            else:
                # Modify color of inactive bubbles
                painter.setBrush(QBrush(QColor(127, 127, 127, 120)))
            painter.drawEllipse(self.width() / 2 + 8 * math.cos(2 * math.pi * i / 6.0) - 5,
                                self.height() / 2 + 8 * math.sin(2 * math.pi * i / 6.0) - 5,
                                6, 6)

        painter.end()

    def showEvent(self, event):
        self.adjustSize()
        self.timer = self.startTimer(50)
        self.counter = 0

    def hideEvent(self, *args, **kwargs):
        self.killTimer(self.timer)

    def timerEvent(self, event):
        self.counter += 1
        self.update()
        # if self.counter == 50:
        #     self.kill_timer()

    # def kill_timer(self):
    #     self.killTimer(self.timer)
        # self.hide()
