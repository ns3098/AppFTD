
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, Qt, QPoint


class OpacityAnimation(object):
    """
    This class handles fade in/fade out animation on appearing widget only.
    """

    FULL_THRESHOLD = 0.9
    DEFAULT_FADE_SPEED = 0.10

    fade_out_finished = pyqtSignal()
    fade_in_finished = pyqtSignal()

    def __init__(self, parent):
        try:
            super(OpacityAnimation, self).__init__(parent)
        except TypeError:
            super(OpacityAnimation, self).__init__()

        self.timer_transition = QTimer()
        self.timer_transition.setInterval(32)
        self.timer_transition.timeout.connect(self.update_opacity)

        # Get the caller widget to apply fade effect
        self.widget = vars()['self']

        self.speed = 0
        self.opacity = 0

    def fade_in(self):
        """
        Start fade in animation.

        :return:
        """
        self.opacity = 0
        self.speed = self.DEFAULT_FADE_SPEED
        self.timer_transition.start()

    def fade_out(self):
        """
        Start fade out animation.

        :return:
        """
        self.opacity = self.FULL_THRESHOLD
        self.speed = -self.DEFAULT_FADE_SPEED
        self.timer_transition.start()

    def fade_out_over(self):
        """
        Function called when fade out animation is over.

        :return:
        """
        pass

    def fade_in_over(self):
        """
        Function called when fade in animation is over.

        :return:
        """
        pass

    @property
    def opacity(self):
        return self.__opacity

    @opacity.setter
    def opacity(self, value):
        if value < 0:
            value = 0
        elif value > 1:
            value = 1
        self.__opacity = value
        self.widget.setWindowOpacity(self.__opacity)

    def update_opacity(self):
        if self.speed > 0:
            if self.widget.isHidden():
                self.widget.show()
            if self.opacity <= self.FULL_THRESHOLD:
                self.opacity += self.speed
            else:
                self.timer_transition.stop()
                self.fade_in_finished.emit()

        elif self.speed < 0:
            if self.opacity > 0:
                self.opacity += self.speed
            else:
                self.timer_transition.stop()
                self.fade_out_finished.emit()
                self.widget.hide()


class FadeAnimation(object):
    """
    This class handles fade in/fade out animation on every widget.
    However it consumes ~2Mb of memory per use.
    """

    def __init__(self, parent, start_value=0.3):
        try:
            super(FadeAnimation, self).__init__(parent)
        except TypeError:
            super(FadeAnimation, self).__init__()

        # Get the caller widget to apply fade effect
        self.widget = vars()['self']
        self.start_value = start_value

        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(self)
        self.widget.setGraphicsEffect(self.opacityEffect)
        self.opacityEffect.setOpacity(start_value)

        self.fadeInAnimation = QPropertyAnimation(self.opacityEffect, b'opacity')
        self.fadeInAnimation.setStartValue(start_value)
        self.fadeInAnimation.setEndValue(1.0)
        self.fadeInAnimation.finished.connect(self.on_finished_fadein_animation)

        self.fadeOutAnimation = QPropertyAnimation(self.opacityEffect, b'opacity')
        self.fadeOutAnimation.setStartValue(1.0)
        self.fadeOutAnimation.setEndValue(start_value)
        self.fadeOutAnimation.finished.connect(self.on_finished_fadeout_animation)

    def on_finished_fadein_animation(self):
        """ Override """
        pass

    def on_finished_fadeout_animation(self):
        """ Override """
        pass

    def fade_in(self, duration):
        """
        Function called when fade in animation is over.

        :return:
        """
        if type(duration) != int:
            raise TypeError("duration should be an integer")
        self.fadeInAnimation.setDuration(duration)
        self.fadeInAnimation.start()

    def fade_out(self, duration):
        """
        Function called when fade out animation is over.

        :return:
        """
        self.fadeOutAnimation.setDuration(duration)
        self.fadeOutAnimation.start()


class AlternatePositionAnimation(object):
    """
    This class handles alternate position animation on widgets.
    It permits to move from a position to another and vice versa.
    """

    def __init__(self, parent):
        try:
            super(AlternatePositionAnimation, self).__init__(parent)
        except TypeError:
            super(AlternatePositionAnimation, self).__init__()

        # Get the caller widget to apply fade effect
        self.widget = vars()['self']

        self.show_animation = QPropertyAnimation(self.widget, b'pos')
        self.hide_animation = QPropertyAnimation(self.widget, b'pos')

        self.show_animation.setDuration(200)
        self.show_animation.setEasingCurve(QEasingCurve.Linear)

        self.hide_animation.setDuration(200)
        self.hide_animation.setEasingCurve(QEasingCurve.Linear)

        self.show_animation.finished.connect(self.show_finished_animation)
        self.hide_animation.finished.connect(self.hide_finished_animation)

    def set_animation_start_values(self):
        """
        Set different animation values.

        :param start: position when starting animation.
        :param end: position when finishing animation.
        :return:
        """
        beg_pos = self.window().width() - self.width() - 2
        end_pos = self.window().width() + self.width()
        print(beg_pos,end_pos, self.window(),self.width())
        start = QPoint(end_pos, 0)
        end = QPoint(beg_pos, 0)
        if not start or not end:
            return

        self.show_animation.setStartValue(QPoint(end_pos, 0))
        self.show_animation.setEndValue(QPoint(beg_pos, 0))

    def start_show(self):
        """
        Start the showing animation.

        :return:
        """

        self.set_animation_start_values()
        self.show_animation.start()

    def set_animation_hide_values(self):
        """
        Set different animation values.

        :param start: position when starting animation.
        :param end: position when finishing animation.
        :return:
        """
        beg_pos = self.window().width() - self.width() - 2
        end_pos = self.window().width() + self.width()
        print('hide',beg_pos,end_pos, self.window(),self.width())
        start = QPoint(end_pos, 0)
        end = QPoint(beg_pos, 0)
        if not start or not end:
            return

        self.hide_animation.setStartValue(QPoint(beg_pos, 0))
        self.hide_animation.setEndValue(QPoint(end_pos, 0))

    def start_hide(self):
        """
        Start the hiding animation.

        :return:
        """
        self.set_animation_hide_values()
        self.hide_animation.start()

    def show_finished_animation(self):
        """
        Function called when show animation is over.

        :return:
        """
        pass

    def hide_finished_animation(self):
        """
        Function called when hide animation is over.

        :return:
        """
        pass
