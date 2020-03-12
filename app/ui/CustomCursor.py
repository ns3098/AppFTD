
from PyQt5 import QtCore,QtGui

class ManagerCursor(QtCore.QObject):
    def __init__(self, parent=None):
        super(ManagerCursor, self).__init__(parent)
        self._movie = None
        self._widget = None
        self._last_cursor = None

    def setMovie(self, movie):
        if isinstance(self._movie, QtGui.QMovie):
            if not self._movie != QtGui.QMovie.NotRunning:
                self._movie.stop()
            del self._movie
        self._movie = movie
        self._movie.frameChanged.connect(self.on_frameChanged)
        self._movie.started.connect(self.on_started)
        self._movie.finished.connect(self.restore_cursor)

    def setWidget(self, widget):
        self._widget = widget

    @QtCore.pyqtSlot()
    def on_started(self):
        if self._widget is not None:
            self._last_cursor = self._widget.cursor()

    @QtCore.pyqtSlot()
    def restore_cursor(self):
        if self._widget is not None:
            if self._last_cursor is not None:
                self._widget.setCursor(self._last_cursor)
        self._last_cursor = None

    @QtCore.pyqtSlot()
    def start(self):
        if self._movie is not None:
            self._movie.start()

    @QtCore.pyqtSlot()
    def stop(self):
        if self._movie is not None:
            self._movie.stop()
            self.restore_cursor()

    @QtCore.pyqtSlot()
    def on_frameChanged(self):
        pixmap = self._movie.currentPixmap()
        cursor = QtGui.QCursor(pixmap)
        if self._widget is not None:
            if self._last_cursor is None:
                self._last_cursor = self._widget.cursor()
            self._widget.setCursor(cursor)
