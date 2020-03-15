from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
from app.core.common.settings import Settings
from app.ui.abstract import CheckableButton


class SimplestLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(SimplestLabel, self).__init__(parent)

        self.setObjectName(self.__class__.__name__)

        self.setWordWrap(True)


class Frame(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(Frame, self).__init__(parent)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setObjectName(self.__class__.__name__)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(10)
        self.question_label = QtWidgets.QLabel('''
        4. User can upload *.csv or *.xlsx data file. Uploaded file will populate the table with file contents and
           overwrite the table. Always make sure to finish working with current file before uploading new data file.
        5. To edit the value in any cell double click on the cell and start editing. To overwrite whole data of the
            cell simply select the cell by single left click and type the new value. Just like Google Spreadsheet.
        6. In case of any critical error while running, app will show an error message and then automatically closes.
           To get more details check log file.
        ''')


        self.question_label.setStyleSheet("color: #6F8DA6; font: 20px 'capsuula';")
        self.question_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)



        self.layout.addWidget(self.question_label)

        self.setLayout(self.layout)


class InstrFeat2(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(InstrFeat2, self).__init__(parent)

        self.setObjectName(self.__class__.__name__)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        self.frame = Frame(parent=self)

        self.setTitle("Features and Instructions")
        self.setSubTitle("\nUser is advised to read all the points carefully.\n\n"
                        "Since this is a one time wizard all these points will not be displayed again when you open the application.")
        self.setPixmap(QtWidgets.QWizard.BannerPixmap, QPixmap(":/icons/wizard_prayer.png"))

        self.layout.addWidget(self.frame)

        self.setLayout(self.layout)

    def initializePage(self):
        """
        Init page with default methods.
        :return:
        """
        return super(InstrFeat2, self).initializePage()
