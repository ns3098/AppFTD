

import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap


class SplashScreen(QtWidgets.QSplashScreen):
    """
    Class implementing a splashscreen.
    """

    start_splashscreen = pyqtSignal()
    splash_time = 200

    def __init__(self, parent=None):
        super(SplashScreen, self).__init__(parent)

        self.setWindowModality(Qt.ApplicationModal)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setObjectName(self.__class__.__name__)
        self.setContextMenuPolicy(Qt.PreventContextMenu)

        pixmap = QPixmap(":/images/Pyqt.jpg")
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())

        self.start_splashscreen.connect(self.fade_opacity)

    def fade_opacity(self):
        """
        Fade splashscreen until it is visible.

        :return:
        """
        self.setWindowOpacity(0)
        t = 0
        while t <= self.splash_time:
            _opacity = self.windowOpacity() + 1 / self.splash_time
            if _opacity > 1:
                break
            self.setWindowOpacity(_opacity)
            self.show()
            t += 1
            time.sleep(0.5 * (1 / self.splash_time))

    def finish(self, widget):
        t = 0
        while t <= self.splash_time:
            _opacity = self.windowOpacity() - 1 / self.splash_time
            if _opacity < 0:
                self.close()
                break
            self.setWindowOpacity(_opacity)
            self.show()
            t += 1
            time.sleep(0.5 * (1 / self.splash_time))

        return QtWidgets.QSplashScreen().finish(widget)
