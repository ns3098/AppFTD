
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import  time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from app.core.common import translate
from app.utils.widgets.widgetanimation import OpacityAnimation
from app.core.common.registrymixin import UniqueRegistryMixin, Registry
from app.core.common.registryproperties import RegistryProperties
from app.core.common.settings import Settings
from app.ui.PandasModel import PandasModel

from app.ui.exceptiondialog import CriticalExceptionDialog

from app.ui.controlframes import ControlOpacity
from app.ui.abstract import WelcomeNotification
from app.ui.Thread import Thread_for_Validate, Thread_for_Download
from app.ui.infodialog import InfoDialog
from app.ui.CustomCursor import ManagerCursor

from app.utils.widgets.floatingtext import PMXMessageOverlay

class MyProgressBar(QProgressBar):

    def __init__(self):
        super().__init__()
        self.setRange(0, 0)
        self.setAlignment(Qt.AlignCenter)
        self._text = None

    def setText(self, text):
        self._text = text

    def text(self):
        return self._text

class RoundedToolButton(QtWidgets.QToolButton):
    def __init__(self, obj_name, parent=None):
        super(RoundedToolButton, self).__init__(parent)

        self.setObjectName("{}TB".format(obj_name))
        self.setFixedSize(50, 50)

'''
This CustomQTableView class is needed to override the keyPressEvent because originally
if any cell is selected and we unintentionally press any key then value of that cell
changes ,so we overrided the keyPressEvent method to avoid that. So only after double
clicking on a cell will make it to go in editing mode.

'''
class CustomQTableView(QTableView):
    def __init__(self, *args, **kwargs):
        QTableView.__init__(self, *args, **kwargs) #Use QTableView constructor

    def keyPressEvent(self, event): #Reimplement the event here
        return

'''
Using a QItemDelegate. This will allow to manually create the editor widget and initialize it before it appears in the QTableView.
And it also override editor which helps to edit table data and reflect those changes in our original model.

'''
class MyDelegate(QtWidgets.QItemDelegate):

    def createEditor(self, parent, option, index):
        return super(MyDelegate, self).createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        text = index.data(QtCore.Qt.EditRole) or index.data(QtCore.Qt.DisplayRole)
        editor.setText(text)

    # Intentionally Commented the below function paint(will be uncommented when Search functionality will be added).
    # Search functionality Module is ready (Will be added Only when user needs it).

    '''def paint (self, painter, option, index):
        if (option.state & QStyle.State_Selected):
            value = index.data(QtCore.Qt.DisplayRole)
            currentQColor = QtCore.Qt.black
            painter.setPen(QColor(currentQColor))
            #painter.setFont(QFont("Bahnschrift SemiLight",10))
            painter.drawText(option.rect,QtCore.Qt.AlignCenter, value)
        else:
            QtWidgets.QItemDelegate.paint(self, painter, option, index)'''

class FinPlate(UniqueRegistryMixin, RegistryProperties, QtWidgets.QFrame):
    """
    Main Class
    Other classes will inherit it.

    """

    def __init__(self, parent=None):
        super(FinPlate, self).__init__(parent)



        self.setObjectName(self.__class__.__name__)

        self.layout = QtWidgets.QVBoxLayout()
        self.settings_layout = QtWidgets.QHBoxLayout()


        self.opacity_tb = RoundedToolButton(obj_name='Opacity', parent=self)
        self.opacity_tb.clicked.connect(self._control_opacity)
        self.control_op = ControlOpacity(self)
        self.control_op.hide()


        self.style_tb = RoundedToolButton(obj_name='Style', parent=self)
        #self.style_tb.setIcon(QIcon("C:/Users/nitin/Desktop/fsf_2020_screening_task/resources/icons/Upload_.png"))
        self.style_tb.setEnabled(False)

        self.file_upload_tb = RoundedToolButton(obj_name='File_upload', parent=self)
        self.file_upload_tb.clicked.connect(self.loadFile)

        self.validate_tb = RoundedToolButton(obj_name='Validate', parent=self)
        self.validate_tb.clicked.connect(self.Validate_Data)

        self.download_tb = RoundedToolButton(obj_name = 'Download', parent = self)
        self.download_tb.clicked.connect(self.Download_data)

        self.progress_bar = MyProgressBar()
        #self.progress_bar.setObjectName("Progress_Bar")
        self.progress_bar.setRange(0,100)
        self.progress_bar.setText('')
        self.progress_bar.setMinimumHeight(30)
        self.progress_bar.setValue(0)

        self.progress_bar.hide()

        self.count = 0 # to increase thread count
        self.pandasTv = QTableView()

        self.__Downloadthreads = []
        self.__Validatethreads = []


        self.setup_ui()

    def setup_ui(self):
        """
        Setup the UI layout.

        :return:
        """
        self.settings_layout.setContentsMargins(0,0,15,0)
        self.settings_layout.addWidget(self.style_tb)
        self.settings_layout.addWidget(self.opacity_tb)
        self.settings_layout.addStretch(0)

        self.settings_layout.addWidget(self.file_upload_tb)
        self.settings_layout.addWidget(self.validate_tb)
        self.settings_layout.addWidget(self.download_tb)
        self.settings_layout.addWidget(self.progress_bar)

        '''self.layout.addWidget(self.top_label)
        self.layout.addStretch()
        self.layout.addWidget(self.prayer_frame)
        self.layout.addLayout(self.buttons_layout)
        self.layout.addStretch()
        self.layout.addWidget(self.dua_after_athan_cb)
        self.layout.addStretch()
        self.layout.addLayout(self.settings_layout)'''
        self.layout.addWidget(self.pandasTv)

        #self.settings_layout.setContentsMargins(0,50,0,0)
        self.layout.addLayout(self.settings_layout)
        delegate = MyDelegate()
        #self.pandasTv.setStyleSheet(Style)
        self.pandasTv.setItemDelegate(delegate)
        self.pandasTv.horizontalHeader().setStretchLastSection(True)
        self.pandasTv.setAlternatingRowColors(True)
        #self.pandasTv.setStyleSheet("QTableView {font-family:Georgia;}" "QTableCornerButton:section { background-color:orange; }"   "QHeaderView { qproperty-defaultAlignment: AlignCenter; font:bold;font-family:consolas;font-size:17px; }")

        # Using ResizeToContents instead of Stretch makes the Application Laggy while switching Windows size and Tab.
        self.pandasTv.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.pandasTv.verticalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.pandasTv.verticalHeader().customContextMenuRequested.connect(self.getObjectHeaderContextMenu)
        self.notification = None

        self.setLayout(self.layout)
        self.set_values()

        self._manager = ManagerCursor(self)
        movie = QtGui.QMovie(":/icons/giphy.gif")
        movie.setScaledSize(QtCore.QSize(100,90))
        #self._manager.setScaledContents(True)
        self._manager.setMovie(movie)
        self._manager.setWidget(self)


    def set_values(self):
        Columns = ['ID','Connection type','Axial load','Shear load','Bolt diameter','Bolt grade','Plate thickness']
        self.df = pd.DataFrame(columns=Columns,index=range(1000))
        self.df = self.df.fillna('')
        model = PandasModel(self.df)
        self.pandasTv.setModel(model)

    def reset_table(self):
        Columns = ['ID','Connection type','Axial load','Shear load','Bolt diameter','Bolt grade','Plate thickness']
        self.pandasTv.model().set_values(Columns, QtCore.QModelIndex())

    def show_df(self):
        Model = self.pandasTv.model()
        dtf = Model._df.copy()
        print(dtf)

    def loadFile(self):
        fileName, ok = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv)")
        if ok:
            df = pd.read_csv(fileName)
            model = PandasModel(df)
            self.pandasTv.setModel(model)



    def _control_opacity(self):
        """
        Control the opacity frame display.

        :return:
        """
        if self.control_op.isHidden():
            self.settings_layout.setContentsMargins(0,60,15,0)
            self.control_op.show()
            self.control_op.setFocus(True)
        else:
            self.settings_layout.setContentsMargins(0,0,15,0)
            self.control_op.hide()

    @staticmethod
    def change_style():
        """
        Change application stylesheet.

        :return:
        """
        Registry().emit_signal("change_style")


    def getObjectHeaderContextMenu(self, pos):
        self.menu = QtWidgets.QMenu(self)

        self.menu.addAction('Add Rows Above Selected', self.insertObjectsBeforeSelectedObjects)
        self.menu.addAction('Add Rows Below Selected', self.insertObjectsAfterSelectedObjects)
        self.menu.addSeparator()
        self.menu.addAction('Add Row Above Selected',self.insertObjectBeforeSelectedObjects)
        self.menu.addAction('Add Row Below Selected',self.insertObjectAfterSelectedObjects)
        self.menu.addSeparator()
        self.menu.addAction('Delete Selected Rows', self.deleteRows)
        self.menu.addSeparator()
        self.menu.addAction('Clear Selected Rows', self.deleteSelectedRows)
        self.menu.addAction('Clear Table', self.Clear_Table)
        self.menu.exec_(self.pandasTv.verticalHeader().viewport().mapToGlobal(pos))

    def deleteSelectedRows(self):
        self.pandasTv.model().clearRows(self.selectedRows())

    def selectedRows(self):
        selectedIndexes = self.pandasTv.selectedIndexes()
        rows = set()
        for index in selectedIndexes:
            rows.add(index.row())
        return sorted(list(rows))

    def insertObjectBeforeSelectedObjects(self):
        selectedObjectIndices = self.selectedRows()
        self.pandasTv.model().insertRows(selectedObjectIndices[0], 1)

    def insertObjectAfterSelectedObjects(self):
        selectedObjectIndices = self.selectedRows()
        self.pandasTv.model().insertRows(selectedObjectIndices[-1]+1, 1)

    def insertObjectsBeforeSelectedObjects(self):
        num, ok = QInputDialog.getInt(self, "Insert", '<html style="font-size:10pt;font-family:georgia;color:white;">Number of rows to insert</html>', 1, 1)
        if ok:
            selectedObjectIndices = self.selectedRows()
            self.pandasTv.model().insertRows(selectedObjectIndices[0], num)

    def insertObjectsAfterSelectedObjects(self):
        num, ok = QInputDialog.getInt(self, "Insert", '<html style="font-size:10pt;font-family:georgia;color:white;">Number of rows to insert</html>', 1, 1)
        if ok:
            selectedObjectIndices = self.selectedRows()
            self.pandasTv.model().insertRows(selectedObjectIndices[-1]+1, num)

    def deleteRows(self):
        selectedObjectIndices = self.selectedRows()
        self.pandasTv.model().removeRows(selectedObjectIndices)

    def Clear_Table(self):
        welcome_title = 'Confirmation'
        message = "All the data will be deleted. Do you wish to clear the whole table?\n\n"
        x = WelcomeNotification(self)
        x.notify(WelcomeNotification.QUESTION, message,welcome_title, button_text='NO',flag=1,text="YES")
        x.close_button.clicked.connect(self.confirmation)
        x.close_button_1.clicked.connect(self.confirmation)


    def confirmation(self):
        if self.sender().objectName() == 'close_button_notification':
            return
        if self.sender().objectName() == 'close_button_notification_1':
            self.reset_table()

    def enable_btn(self):
        self.file_upload_tb.setEnabled(1)
        self.download_tb.setEnabled(1)
        self.validate_tb.setEnabled(1)

    def disable_btn(self):
        self.file_upload_tb.setEnabled(0)
        self.download_tb.setEnabled(0)
        self.validate_tb.setEnabled(0)

    def data_empty(self):
        welcome_title = 'Alert'
        message = 'Seems like there is no data to Validate or Download.\n\n' \
        'NOTE : For any row to be considered as a valid data row there \n'\
        'must be some value in the column ID. Only Valid data row(s) will\n'\
        'be considered for Validation and Downloading.\n'
        WelcomeNotification(self).notify(WelcomeNotification.WARNING, message,welcome_title, button_text='OK')
        self.destroy_thread()
        self.destroy_download_thread()

    def Validate_Data(self):
        self.destroy_thread()
        self.disable_btn()

        Model = self.pandasTv.model()
        df = Model._df.copy()

        self.count+=1
        Worker = Thread_for_Validate(df)
        thread = QThread()
        thread.setObjectName('main'+str(self.count))
        self.__Validatethreads.append((thread,Worker))
        Worker.moveToThread(thread)

        thread.started.connect(Worker.Check_unique_value)
        Worker.Not_unique.connect(self.no_unique)
        Worker.Not_numeric.connect(self.no_numeric)
        Worker.No_error.connect(self.no_error)
        Worker.is_exception.connect(self.show_error)
        Worker.data_frame_empty.connect(self.data_empty)
        self._manager.start()
        thread.start()

    def show_error(self,msg):
        error_box = CriticalExceptionDialog()
        error_box.text_edit.setText('Data Table has no attribute : '+msg)
        error_box.show()
        self.destroy_thread()
        self.destroy_download_thread()

    def no_unique(self):
        self.destroy_thread()
        welcome_title = 'Alert'
        message = "All the values in the column ID is not unique. Please Check all the values once again.\n\n"
        WelcomeNotification(self).notify(WelcomeNotification.ERROR, message,welcome_title, button_text='OK')


    def no_numeric(self):
        self.destroy_thread()
        welcome_title = 'Alert'
        message = 'All the values in the table is not Numeric. Please Check all the values once again.\n\n'
        WelcomeNotification(self).notify(WelcomeNotification.ERROR, message,welcome_title, button_text='OK')


    def no_error(self):
        self.destroy_thread()
        welcome_title = 'Congratulations'
        message = 'All the data validated successfully. No error has been found. You can now download the data\n\n'
        WelcomeNotification(self).notify(WelcomeNotification.OK, message,welcome_title, button_text='OK')


    def destroy_thread(self):

        if self.__Validatethreads:
            for thread,worker in self.__Validatethreads:
                thread.quit()
                thread.wait()

        self.enable_btn()
        self._manager.stop()


    def Download_data(self):
        filename = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if filename:
            self.destroy_download_thread()
            self.progress_bar.show()
            self.progress_bar.setValue(0)
            self.disable_btn()
            Model = self.pandasTv.model()
            df = Model._df.copy()
            print(df.empty)
            self.count+=1
            Worker = Thread_for_Download(df,filename)
            thread = QThread()
            thread.setObjectName('main'+str(self.count))
            self.__Downloadthreads.append((thread,Worker))
            Worker.moveToThread(thread)

            thread.started.connect(Worker.start_download)
            Worker.row_count.connect(self.show_counter)
            Worker.download_complete.connect(self.download_completed)
            Worker.data_frame_empty.connect(self.data_empty)
            Worker.is_exception.connect(self.show_error)
            self._manager.start()
            thread.start()

    def show_counter(self,count, current, length):
        self.progress_bar.setValue(count)
        self.progress_bar.setText(f'{current} out of {length} file(s) downloaded.')

    def download_completed(self):
        self.progress_bar.setValue(100)
        self.progress_bar.hide()
        self.destroy_download_thread()
        welcome_title = 'Congratulations'
        message = 'All the data has been downloaded in the chosen directory.\n\n'
        WelcomeNotification(self).notify(WelcomeNotification.OK, message,welcome_title, button_text='OK')

    def destroy_download_thread(self):
        if self.__Downloadthreads:
            for thread,worker in self.__Downloadthreads:
                thread.quit()
                thread.wait()
        self.enable_btn()
        self._manager.stop()

class TensionMember(FinPlate):
    """
    TensionMember Frame inherited from FinPlate
    """

    def __init__(self, parent=None):
        super(TensionMember, self).__init__(parent)

        self.setObjectName(self.__class__.__name__)

        self.set_values()

    def set_values(self):
        Columns = ['ID','Member length','Tensile load','Support condition at End 1','Support condition at End 2']
        self.df = pd.DataFrame(columns=Columns,index=range(1000))
        self.df = self.df.fillna('')
        model = PandasModel(self.df)
        self.pandasTv.setModel(model)

    def reset_table(self):
        Columns = ['ID','Member length','Tensile load','Support condition at End 1','Support condition at End 2']
        self.pandasTv.model().set_values(Columns, QtCore.QModelIndex())

class BCEndPlate(FinPlate):


    def __init__(self,parent=None):
        super(BCEndPlate, self).__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.set_values()

    def set_values(self):
        Columns = ['ID','End plate type','Shear load','Axial Load','Moment Load','Bolt diameter','Bolt grade','Plate thickness']
        self.df = pd.DataFrame(columns=Columns,index=range(1000))
        self.df = self.df.fillna('')
        model = PandasModel(self.df)
        self.pandasTv.setModel(model)

    def reset_table(self):
        Columns = ['ID','End plate type','Shear load','Axial Load','Moment Load','Bolt diameter','Bolt grade','Plate thickness']
        self.pandasTv.model().set_values(Columns, QtCore.QModelIndex())


class CleatAngle(FinPlate):


    def __init__(self,parent=None):
        super(CleatAngle, self).__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.set_values()

    def set_values(self):
        Columns = ['ID','Angle leg 1','Angle leg 2','Angle thickness','Shear load','Bolt diameter','Bolt grade']
        self.df = pd.DataFrame(columns=Columns,index=range(1000))
        self.df = self.df.fillna('')
        model = PandasModel(self.df)
        self.pandasTv.setModel(model)

    def reset_table(self):
        Columns = ['ID','Angle leg 1','Angle leg 2','Angle thickness','Shear load','Bolt diameter','Bolt grade']
        self.pandasTv.model().set_values(Columns, QtCore.QModelIndex())
