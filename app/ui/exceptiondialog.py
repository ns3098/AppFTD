

from PyQt5 import QtWidgets

from app.ui.abstract import Dialog


class CriticalExceptionDialog(Dialog):
    """
    About dialog.
    """

    def __init__(self, parent=None):
        super(CriticalExceptionDialog, self).__init__(width=670, height=380,
                                                      obj_name=self.__class__.__name__,
                                                      titlebar_name="Exception", titlebar_icon=None,
                                                      parent=parent)

        self.v_layout = QtWidgets.QVBoxLayout()

        self.dialog_frame.setLayout(self.v_layout)

        self.text_edit = QtWidgets.QTextEdit(self)
        self.text_edit.setObjectName("TextEditError")
        self.text_edit.setReadOnly(True)

        self.v_layout.addWidget(self.text_edit)
