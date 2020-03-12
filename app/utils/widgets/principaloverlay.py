
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QColor

from app.core.common.registrymixin import RegistryMixin
from app.core.common.registry import Registry


class PrincipalOverlay(RegistryMixin, QtWidgets.QFrame):
    """
    Principal overlay to show a transparent black widget.

    For the moment, apply only on window but need to be applied easily on different frame.
    """

    @classmethod
    def create_overlay(cls, parent):
        c = cls(parent=parent)
        c.show()
        return c

    def __init__(self, parent=None):
        super(PrincipalOverlay, self).__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self._parent = parent

    def __application_init__(self):
        self.hide()
        Registry().register_function("activate_overlay", self.show)
        Registry().register_function("desactivate_overlay", self.hide)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(0, 0, 0, 60)))
        self.resize(self._parent.width(), self._parent.height())

        # TODO - Make this overlay more generic and callable from every frame to every frame
        # def activate(self, parent):
        #     self._parent = parent
        #     self.show()
        #
        # def desactivate(self):
        #     self.hide()
        #
        # def showEvent(self, event):
        #     super(PrincipalOverlay, self).showEvent(event)
        #
        # def closeEvent(self, event):
        #     super(PrincipalOverlay, self).closeEvent(event)
