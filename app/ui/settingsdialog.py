

import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QIcon, QColor, QStandardItem, QStandardItemModel, QFont
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from app.core.common import translate
from app.core.common.logapi import log
from app.core.common.registry import Registry
from app.core.common.registryproperties import RegistryProperties
from app.core.common.registrymixin import RegistryMixin
from app.core.common.resourceslocation import ResourcesLocation
from app.core.common.settings import Settings

from app.ui.abstract import Dialog, ListView, SideLabel, ListWidgetSelectorFrame



class SettingsFrameSelector(QtWidgets.QFrame):

    def __init__(self, parent=None):
        super(SettingsFrameSelector, self).__init__(parent)

        self.setFixedWidth(135)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName(self.__class__.__name__)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.h_layout = QtWidgets.QHBoxLayout()
        self.h_layout.setSpacing(0)

        # self.side_label = QtWidgets.QLabel('Settings - الاعدادات')
        # self.side_label.setObjectName("TopSideLabel")

        self.sl_1 = SideLabel(parent=self, label=translate('Application', "General"), icon=None, w_colorframe=3,
                              h_colorframe=45, alignment='left', color=QColor(255, 165, 0))


        self.listwidget_frame = ListWidgetSelectorFrame(self)

        _item = QtWidgets.QListWidgetItem(self.listwidget_frame)
        _item.setSizeHint(self.sl_1.sizeHint())
        self.listwidget_frame.setItemWidget(_item, self.sl_1)



        # Resize ListWidget to fit content
        self.listwidget_frame.setFixedSize(self.width(), self.listwidget_frame.sizeHintForRow(0) *
                                           self.listwidget_frame.count() + 2 * self.listwidget_frame.frameWidth())

        # self.layout.addWidget(self.side_label)
        self.layout.addWidget(self.listwidget_frame)
        self.layout.addStretch()

        # Set margin between frame and borders
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        # Set margin between elements of layout
        self.layout.setSpacing(0)

        self.layout.addLayout(self.h_layout)

        # # # # This whole code activate Toolbuttons inside the settings dialog # # # #
        # self.settings_dialog_tb = QtWidgets.QToolButton()
        # self.settings_dialog_tb.setObjectName("settings_button")
        # self.settings_dialog_tb.setFixedHeight(self.width() / 3)
        # self.info_dialog_tb = QtWidgets.QToolButton()
        # self.info_dialog_tb.setObjectName("info_button")
        # self.info_dialog_tb.setFixedHeight(self.width() / 3)
        # self.about_dialog_tb = QtWidgets.QToolButton()
        # self.about_dialog_tb.setObjectName("about_button")
        # self.about_dialog_tb.setFixedHeight(self.width() / 3)
        #
        # self.h_layout.addWidget(self.settings_dialog_tb)
        # self.h_layout.addWidget(self.info_dialog_tb)
        # self.h_layout.addWidget(self.about_dialog_tb)
        #
        # self.settings_dialog_tb.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # self.info_dialog_tb.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # self.about_dialog_tb.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        self.listwidget_frame.currentRowChanged[int].connect(self._modify_style_item)

    def _modify_style_item(self, idx):
        """
        Handle changing style whether a new item is selected.

        :param idx: index of the new item.
        :return:
        """
        self.parent().set_stack(idx)

        for idx_item in range(self.listwidget_frame.count()):
            item = self.listwidget_frame.item(idx_item)
            if item.isSelected():
                side_label_instance = self.listwidget_frame.itemWidget(item)
                side_label_instance.selected.emit()
            else:
                side_label_instance = self.listwidget_frame.itemWidget(item)
                side_label_instance.unselected.emit()


class GeneralSettingsFrame(RegistryProperties, QtWidgets.QFrame):

    def __init__(self, parent=None):
        super(GeneralSettingsFrame, self).__init__(parent)

        self.setObjectName(self.__class__.__name__)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.close_prog_cb = QtWidgets.QCheckBox(translate('Application',
                                                           "Minimize to system tray when program is closed"), self)
        self.splashscreen_cb = QtWidgets.QCheckBox(translate('Application', "Show splashscreen"), self)

        self.layout.addWidget(self._groupbox_close_setting())
        self.layout.addStretch()

    def _groupbox_close_setting(self):
        """
        Generate groupbox for general settings.

        :return:
        """
        group_close = QtWidgets.QGroupBox("", self)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.close_prog_cb)
        vbox.addWidget(self.splashscreen_cb)
        group_close.setLayout(vbox)

        return group_close

    def save_settings(self):
        """
        Save current configuration.

        :return:
        """
        if self.close_prog_cb.isChecked():
            Settings().setValue("general_settings/close", 0)
        else:
            Settings().setValue("general_settings/close", 1)

        if self.splashscreen_cb.isChecked():
            Settings().setValue("general_settings/splashscreen", 1)
        else:
            Settings().setValue("general_settings/splashscreen", 0)


    def load_settings(self):
        """
        Load settings to read settings each time dialog is opened and set the correct state for settings.

        :return:
        """
        if Settings().contains("general_settings/splashscreen"):
            if Settings().value("general_settings/splashscreen") == 0:
                self.splashscreen_cb.setChecked(False)
            elif Settings().value("general_settings/splashscreen") == 1:
                self.splashscreen_cb.setChecked(True)
            else:
                log.debug("value for splashscreen in "
                          "settings.ini: {}".format(Settings().value("general_settings/splashscreen")))
        else:
            self.splashscreen_cb.setChecked(True)
            Settings().setValue("general_settings/splashscreen", 1)


        if Settings().contains("general_settings/close"):
            if Settings().value("general_settings/close") == 0:
                self.close_prog_cb.setChecked(True)
            elif Settings().value("general_settings/close") == 1:
                self.close_prog_cb.setChecked(False)
            else:
                log.debug("value for close in settings.ini: {}".format(Settings().value("general_settings/close")))
        else:
            self.close_prog_cb.setChecked(True)
            Settings().setValue("general_settings/close", 0)


class SettingsDialog(Dialog):
    """
    Settings dialog.
    """

    APPLY = QtWidgets.QDialogButtonBox.Apply
    CANCEL = QtWidgets.QDialogButtonBox.Cancel
    OK = QtWidgets.QDialogButtonBox.Ok

    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(width=780, height=480, obj_name=self.__class__.__name__,
                                             titlebar_name="Settings", titlebar_icon=None, parent=parent)

        self.dialog_buttons = QtWidgets.QDialogButtonBox(self.CANCEL | self.OK | self.APPLY, Qt.Horizontal, self)

        self.apply_button = self.dialog_buttons.button(self.APPLY)
        self.cancel_button = self.dialog_buttons.button(self.CANCEL)
        self.ok_button = self.dialog_buttons.button(self.OK)

        self.apply_button.setFixedWidth(100)
        self.cancel_button.setFixedWidth(100)
        self.ok_button.setFixedWidth(100)

        # Cancel button signal
        self.dialog_buttons.rejected.connect(self.reject)
        # OK button signal
        self.dialog_buttons.accepted.connect(self.handle_ok)
        # Apply button signal
        self.apply_button.clicked.connect(self.handle_apply)

        self.status_layout = QtWidgets.QHBoxLayout()
        self.status_layout.setContentsMargins(9, 9, 9, 9)

        contact_label = QtWidgets.QLabel(translate('Application', "For any problem, please contact me."), self)
        font = QFont('ubuntu', 10)
        contact_label.setFont(font)

        self.status_layout.addWidget(contact_label)
        self.status_layout.addWidget(self.dialog_buttons)

        self.h_layout = QtWidgets.QHBoxLayout()

        self.right_side_panel = SettingsFrameSelector(self)
        self.stack = QtWidgets.QStackedWidget(self)

        self.general_settings_frame = GeneralSettingsFrame(self)


        self.stack.addWidget(self.general_settings_frame)


        self.layout.addLayout(self.h_layout)
        self.h_layout.addWidget(self.right_side_panel)
        self.h_layout.addWidget(self.stack)
        self.layout.addLayout(self.status_layout)

    def __application_init__(self):
        self.set_stack(0)

    def __application_post_init__(self):
        pass

    def __application_clean__(self):
        pass

    def showEvent(self, event):
        """
        Overring showEvent to update settings values from each frame each time the dialog is opened.

        :param event:
        :return:
        """
        self.general_settings_frame.load_settings()
        return super(SettingsDialog, self).showEvent(event)

    def set_stack(self, idx):
        """
        Set the visible widget to widget at index <idx>

        :param idx: index of the widget to be visible.
        :return:
        """
        self.stack.setCurrentIndex(idx)
        self.right_side_panel.listwidget_frame.setCurrentRow(idx)

    def handle_ok(self):
        """
        Ok button behaves exactly like apply buttons except it closes the dialog.

        :return:
        """
        self.handle_apply()
        self.accept()

    def handle_apply(self):
        """
        Save all configuration present in frames contained in settings dialog.

        :return:
        """
        self.general_settings_frame.save_settings()
