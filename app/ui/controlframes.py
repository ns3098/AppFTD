

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap

from app.core.common import translate
from app.core.common.logapi import log

from app.ui.abstract import ControlOption


class ControlOpacity(ControlOption):
    def __init__(self, parent=None):
        super(ControlOpacity, self).__init__(obj_name=self.__class__.__name__,
                                             icon=":/icons/controloption_opacity.png",
                                             parent=parent)

        self.sld.setRange(0, 100)
        self.sld.setMaximum(30)
        self.sld.valueChanged[int].connect(self._ctrl_opacity)

    def showEvent(self, *args, **kwargs):
        self.move(self.parent().opacity_tb.x(), self.parent().opacity_tb.y() - 60)
        super(ControlOpacity, self).showEvent(*args)

    def _ctrl_opacity(self, value):
        """
        Change opacity of the program.

        :return:
        """
        _opacity = 1 - value / 100
        self.window().setWindowOpacity(_opacity)
