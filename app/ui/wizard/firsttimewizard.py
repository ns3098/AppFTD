
import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from app.ui.wizard.lastpage import LastPage

from app.ui.wizard.InsFeat1 import InstrFeat1
from app.ui.wizard.welcomepage import WelcomeWizardPage
from app.ui.wizard.InsFeat2 import InstrFeat2


from app.core.common.logapi import log
from app.core.common.settings import Settings

Instruction_for_page1 = '''

1. There are 4 tabs one for each module. On selecting a particular module an empty table with 1000 rows
   (by default) along with corresponding header row will be displayed. User can fill data manually in each row.

2. User can also perform operations like adding row(s), deleting row(s), Clearing values of row(s),
   Clearing Table. Right clicking on the header of selected row(s) will show above options.

3. From all the rows of data table, only those rows will be considered for data validation and downloading
   which contains some value in the column ID except these row(s) all other row(s) will be ignored. It is also
   advised to validate the data before downloading it to get the error free result.

'''

Instruction_for_page2 = '''

4. User can upload *.csv or *.xlsx data file. Uploaded file will populate the table with file contents and
   overwrite the table. Always make sure to finish working with current file before uploading new data file.

5. To edit the value in any cell double click on the cell and start editing. To overwrite whole data of the
    cell simply select the cell by single left click and type the new value. Just like Google Spreadsheet.

6. In case of any critical error while running, app will show an error message and then automatically closes.
   To get more details check log file.

'''
class Wizard(QtWidgets.QWizard):
    """
    Generic AppFTD wizard to provide generic functionality and a unified look
    and feel.
    """

    def __init__(self, parent):
        super(Wizard, self).__init__(parent)

        self.setObjectName(self.__class__.__name__)

        # Need to be added, if not, moving frame from a button crash
        self.pressed = 0
        self.offset = self.pos()

        self.finish_button = self.button(QtWidgets.QWizard.FinishButton)
        self.cancel_button = self.button(QtWidgets.QWizard.CancelButton)
        self.next_button = self.button(QtWidgets.QWizard.NextButton)
        self.back_button = self.button(QtWidgets.QWizard.BackButton)


        self.setup_ui()

        self.welcome_page = WelcomeWizardPage(parent=self)
        self.insFeat1 = InstrFeat1(parent=self)
        self.insFeat2 = InstrFeat2(parent=self)
        self.last_page = LastPage(parent=self)

        self.welcome_page_id = self.addPage(self.welcome_page)
        self.insFeat1_id = self.addPage(self.insFeat1(Instruction_for_page1))
        self.insFeat2_id = self.addPage(self.insFeat2(Instruction_for_page2))
        self.last_page_id = self.addPage(self.last_page)

        #self.currentIdChanged.connect(self.on_current_id_changed)

    def setup_ui(self):
        """
        Set up the wizard UI.

        :return:
        """
        self.setObjectName(self.__class__.__name__)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        self.finish_button.setFixedWidth(100)
        self.cancel_button.setFixedWidth(100)
        self.next_button.setFixedWidth(100)
        self.back_button.setFixedWidth(100)


        button_layout = [QtWidgets.QWizard.Stretch, QtWidgets.QWizard.BackButton,
                         QtWidgets.QWizard.NextButton, QtWidgets.QWizard.FinishButton, QtWidgets.QWizard.CancelButton]
        self.setButtonLayout(button_layout)
        self.setModal(True)
        self.setFixedSize(820, 565)

        self.setOptions(QtWidgets.QWizard.IndependentPages | QtWidgets.QWizard.NoBackButtonOnStartPage)

        self.setWizardStyle(QtWidgets.QWizard.ModernStyle)

    def mousePressEvent(self, event):
        self.offset = event.pos()
        self.pressed = 1

    def mouseMoveEvent(self, event):
        if self.pressed:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)

    def mouseReleaseEvent(self, event):
        self.pressed = 0

    def showEvent(self, event):
        """
        Center the wizard dialog when appears.

        :param event:
        :return:
        """
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())
        return super(Wizard, self).showEvent(event)

    def exec(self):
        """
        Run the wizard.
        """
        return QtWidgets.QWizard.exec(self)

    def reject(self):
        """
        Stop the wizard on cancel button, close button or ESC key.
        Remove settings file if wizard is not completed.
        """
        log.debug('Wizard cancelled by user.')
        self.was_cancelled = True
        if os.path.exists(Settings().fileName()):
            try:
                os.remove(Settings().fileName())
            except (OSError, FileNotFoundError):
                log.error("File {} not found...".format(Settings().fileName()))
        return super(Wizard, self).reject()

    def accept(self):
        """
        The wizard finished correctly.
        Extend settings defined by user by default settings.
        """
        log.debug('Wizard finished. Saving settings ...')
        Settings().extend_current_settings()
        return super(Wizard, self).accept()
