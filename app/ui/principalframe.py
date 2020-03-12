

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from app.core.common.registry import Registry
from app.core.common.registrymixin import UniqueRegistryMixin

from app.ui.mainframe import FinPlate, TensionMember, BCEndPlate, CleatAngle
from app.ui.mainframeselector import MainFrameSelector


class PrincipalFrame(UniqueRegistryMixin, QtWidgets.QFrame):
    """
    Principal Frame that contains all widgets and the frame that selects between widgets.
    """

    def __init__(self, parent=None):
        super(PrincipalFrame, self).__init__(parent)

        self.layout = QtWidgets.QHBoxLayout(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName(self.__class__.__name__)

        self.container_stack = QtWidgets.QStackedWidget(self)

        self.main_frame_selector = MainFrameSelector(self)

        self.finplate_frame = FinPlate(self)
        self.tensionmember_frame = TensionMember(self)
        self.bcEnd_plate = BCEndPlate(self)
        self.cleat_angle = CleatAngle(self)

        self.container_stack.addWidget(self.finplate_frame)
        self.container_stack.addWidget(self.tensionmember_frame)
        self.container_stack.addWidget(self.bcEnd_plate)
        self.container_stack.addWidget(self.cleat_angle)
        # Set margin between frame and borders
        self.layout.setContentsMargins(0, 0, 0, 0)
        # Set margin between elements of layout
        self.layout.setSpacing(0)

        self.setLayout(self.layout)

        self.layout.addWidget(self.container_stack)
        self.layout.addWidget(self.main_frame_selector)

        Registry().register_function("set_main_stack", self.set_stack)

    def __application_init__(self):
        # Set first time to main frame
        self.set_stack(0)
        pass

    def __application_clean__(self):
        pass

    def set_stack(self, idx):
        """
        Set the visible widget to widget at index <idx>

        :param idx: index of the widget to be visible.
        :return:
        """
        self.container_stack.setCurrentIndex(idx)
        self.main_frame_selector.listwidget_frame.setCurrentRow(idx)

        self.change_margin()

    def change_margin(self):
        self.finplate_frame.control_op.hide()
        self.tensionmember_frame.control_op.hide()
        self.finplate_frame.settings_layout.setContentsMargins(0,0,15,0)
        self.tensionmember_frame.settings_layout.setContentsMargins(0,0,15,0)
