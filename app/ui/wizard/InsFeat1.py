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

        1. There are 4 tabs one for each module. On selecting a particular module an empty table with 1000 rows
           (by default) along with corresponding header row will be displayed. User can fill data manually in each row.

        2. User can also perform operations like adding row(s), deleting row(s), Clearing values of row(s),
           Clearing Table. Right clicking on the header of selected row(s) will show above options.

        3. From all the rows of data table, only those rows will be considered for data validation and downloading
           which contains some value in the column ID except these row(s) all other row(s) will be ignored. It is also
           advised to validate the data before downloading it to get the error free result.

        ''')


        self.question_label.setStyleSheet("color: #6F8DA6; font: 20px 'capsuula';")
        self.question_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)



        self.layout.addWidget(self.question_label)

        self.setLayout(self.layout)


class InstrFeat1(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(InstrFeat1, self).__init__(parent)

        self.setObjectName(self.__class__.__name__)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        self.frame = Frame(parent=self)

        self.setTitle("Features and Instructions")
        self.setSubTitle("\nUser is advised to read all the points carefully.\n\n"
                        "Since this is a one time wizard all these points will not be displayed again when you open the application.")
        self.setPixmap(QtWidgets.QWizard.BannerPixmap, QPixmap(":/icons/wizard_.png"))

        self.layout.addWidget(self.frame)

        self.setLayout(self.layout)

    def initializePage(self):
        """
        Init page with default methods.
        :return:
        """
        return super(InstrFeat1, self).initializePage()
