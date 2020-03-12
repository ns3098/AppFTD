

from PyQt5 import QtWidgets
# from PyQt5.QtGui import QPixmap

from app.ui.abstract import Dialog


class AboutDialog(Dialog):
    """
    About dialog.
    """

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(width=650, height=250, obj_name=self.__class__.__name__,
                                          titlebar_name="About", titlebar_icon=None, parent=parent)

        grid_layout = QtWidgets.QGridLayout()

        self.name_prog = QtWidgets.QLabel("AppFTD", self)

        self.label_version = QtWidgets.QLabel("v0.0.1", self)
        self.label_copyright = QtWidgets.QLabel("Copyright 2020 AppForTabularData", self)
        self.label_contribution = QtWidgets.QLabel("Special thanks to FOSSEE for giving me this opportunity.", self)

        grid_layout.addWidget(self.name_prog, 0, 0)
        grid_layout.addWidget(self.label_version, 1, 0)
        grid_layout.addWidget(self.label_copyright, 2, 0)
        grid_layout.addWidget(self.label_contribution, 0, 1, 3, 1)

        self.dialog_frame.setLayout(grid_layout)
