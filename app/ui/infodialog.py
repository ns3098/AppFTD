

# import os
#
# from PyQt5 import QtWidgets
# from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import Qt

from app.ui.abstract import Dialog


class InfoDialog(Dialog):
    """
    About dialog.
    """

    def __init__(self, parent=None):
        super(InfoDialog, self).__init__(width=650, height=290, obj_name="AboutDialog",
                                         titlebar_name="Info", titlebar_icon=None, parent=parent)
