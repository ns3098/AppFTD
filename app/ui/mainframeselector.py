

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor

from app.core.common import translate
from app.core.common.registry import Registry
from app.core.common.registrymixin import UniqueRegistryMixin

from app.ui.abstract import SideLabel, ListWidgetSelectorFrame
from app.ui.aboutdialog import AboutDialog
from app.ui.infodialog import InfoDialog
from app.ui.settingsdialog import SettingsDialog

from app.utils.widgets.timelabel import TimeLabel
from app.utils.widgets.widgetanimation import AlternatePositionAnimation


class ToolButton(QtWidgets.QToolButton):

    def __init__(self, obj_name, parent=None):
        super(ToolButton, self).__init__(parent)

        self.setObjectName(obj_name)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)


class MainFrameSelector(UniqueRegistryMixin, AlternatePositionAnimation, QtWidgets.QFrame):

    def __init__(self, parent=None):
        super(MainFrameSelector, self).__init__(parent)

        self.setFixedWidth(135)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName(self.__class__.__name__)

        # TODO - Fix when resizing
        beg_pos = self.window().width() - self.width() - 2
        end_pos = self.window().width() + self.width()


        self.settings_dialog = SettingsDialog(self)
        self.info_dialog = InfoDialog(self)
        self.about_dialog = AboutDialog(self)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.h_layout = QtWidgets.QHBoxLayout()
        self.h_layout.setSpacing(0)

        #self.side_label = QtWidgets.QLabel(translate('Application', 'Settings'), self)
        #self.side_label.setObjectName("TopSideLabel")

        self.time_label = TimeLabel(self)

        self.sizegrip = QtWidgets.QSizeGrip(self)

        self.sl_1 = SideLabel(parent=self, label=translate('Application', "<h3> FinPlate </h3>"),  icon=None,
                              w_colorframe=3, h_colorframe=60, alignment='right', color=QColor(0, 152, 206))
        self.sl_2 = SideLabel(parent=self, label=translate('Application', "<h3> TensionMember </h3>"),  icon=None,
                              w_colorframe=3, h_colorframe=60, alignment='right', color=QColor(0, 152, 206))
        self.sl_3 = SideLabel(parent=self, label=translate('Application', "<h3> BCEndPlate </h3>"),  icon=None,
                              w_colorframe=3, h_colorframe=60, alignment='right', color=QColor(0, 152, 206))
        self.sl_4 = SideLabel(parent=self, label=translate('Application', "<h3> CleatAngle </h3>"),  icon=None,
                              w_colorframe=3, h_colorframe=60, alignment='right', color=QColor(0, 152, 206))
        self.listwidget_frame = ListWidgetSelectorFrame(self)

        item_salat = QtWidgets.QListWidgetItem(self.listwidget_frame)
        item_salat.setSizeHint(self.sl_1.sizeHint())
        item_salat1 = QtWidgets.QListWidgetItem(self.listwidget_frame)
        item_salat1.setSizeHint(self.sl_2.sizeHint())
        item_salat2 = QtWidgets.QListWidgetItem(self.listwidget_frame)
        item_salat2.setSizeHint(self.sl_3.sizeHint())
        item_salat3 = QtWidgets.QListWidgetItem(self.listwidget_frame)
        item_salat3.setSizeHint(self.sl_4.sizeHint())
        self.listwidget_frame.setItemWidget(item_salat, self.sl_1)
        self.listwidget_frame.setItemWidget(item_salat1, self.sl_2)
        self.listwidget_frame.setItemWidget(item_salat2, self.sl_3)
        self.listwidget_frame.setItemWidget(item_salat3, self.sl_4)

        self.settings_dialog_tb = ToolButton(obj_name="settings_button", parent=self)
        self.settings_dialog_tb.setFixedHeight(self.width() / 3)

        self.info_dialog_tb = ToolButton(obj_name="info_button", parent=self)
        self.info_dialog_tb.setFixedHeight(self.width() / 3)

        self.about_dialog_tb = ToolButton(obj_name="about_button", parent=self)
        self.about_dialog_tb.setFixedHeight(self.width() / 3)

        for b in [self.settings_dialog_tb, self.info_dialog_tb, self.about_dialog_tb]:
            b.clicked.connect(self._call_dialog)

        self.listwidget_frame.currentRowChanged.connect(self._modify_style_item)

        self.setup_ui()

    def __application_init__(self):
        Registry().register_function('expand_main_frame_selector', self.set_expand_animation)
        Registry().register_function('hide_main_frame_selector', self.set_hide_animation)

    def __application_post_init__(self):
        pass

    def __application_clean__(self):
        pass

    def setup_ui(self):
        """
        Setup the UI layout.

        :return:
        """
        # Resize ListWidget to fit content
        self.listwidget_frame.setFixedSize(self.width(), self.listwidget_frame.sizeHintForRow(0) *
                                           self.listwidget_frame.count() + 2 * self.listwidget_frame.frameWidth())

        #self.layout.addWidget(self.side_label)
        self.layout.addWidget(self.listwidget_frame)
        self.layout.addStretch()

        self.layout.addWidget(self.time_label)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.layout.addLayout(self.h_layout)

        self.layout.addWidget(self.sizegrip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.h_layout.addWidget(self.settings_dialog_tb)
        self.h_layout.addWidget(self.info_dialog_tb)
        self.h_layout.addWidget(self.about_dialog_tb)

    def set_expand_animation(self):
        """
        Show the MainFrameSelector frame.

        :return:
        """
        self.start_show()
        self.show()

    def set_hide_animation(self):
        """
        Hide the MainFrameSelector frame.

        :return:
        """
        self.start_hide()

    def hide_finished_animation(self):
        self.hide()

    def _modify_style_item(self, idx):
        """
        Handle changing style whether a new item is selected.

        :param idx: index of the new item.
        :return:
        """
        Registry().execute("set_main_stack", idx)

        for idx_item in range(self.listwidget_frame.count()):
            item = self.listwidget_frame.item(idx_item)
            if item.isSelected():
                side_label_instance = self.listwidget_frame.itemWidget(item)
                side_label_instance.selected.emit()
            else:
                side_label_instance = self.listwidget_frame.itemWidget(item)
                side_label_instance.unselected.emit()

    def _call_dialog(self):
        """
        Execute the matching dialog according to button clicked.

        :return:
        """
        if self.sender().objectName() == "settings_button":
            self.settings_dialog.exec_()
        elif self.sender().objectName() == "info_button":
            self.info_dialog.exec_()
        elif self.sender().objectName() == "about_button":
            self.about_dialog.exec_()
