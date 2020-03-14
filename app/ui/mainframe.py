
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
import  time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *   ## using * is a bad practice but i was irritated :(

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

## Custom Progree bar to show Download Progress
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

 ## Custm ROund Button
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

Currently we are not using this . If you want to use this You can Make pandasTv an instance
of this class instead of QTableView.

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
        self.opacity_tb.setToolTip("Control Opacity")
        self.control_op.hide()


        self.style_tb = RoundedToolButton(obj_name='Style', parent=self)
        #self.style_tb.setIcon(QIcon("C:/Users/nitin/Desktop/fsf_2020_screening_task/resources/icons/Upload_.png"))
        self.style_tb.setEnabled(False)

        self.file_upload_tb = RoundedToolButton(obj_name='File_upload', parent=self)
        self.file_upload_tb.clicked.connect(self.loadFile)
        self.file_upload_tb.setToolTip("Load Input")

        self.validate_tb = RoundedToolButton(obj_name='Validate', parent=self)
        self.validate_tb.clicked.connect(self.Validate_Data)
        self.validate_tb.setToolTip("Validate Data")

        self.download_tb = RoundedToolButton(obj_name = 'Download', parent = self)
        self.download_tb.clicked.connect(self.Download_data)
        self.download_tb.setToolTip("Download Data")

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
        self.module_name = "FinPlate"
        self.ModuleColumns = ['ID','Connection type','Axial load','Shear load','Bolt diameter','Bolt grade','Plate thickness']


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

        self.layout.addWidget(self.pandasTv)

        #self.settings_layout.setContentsMargins(0,50,0,0)
        self.layout.addLayout(self.settings_layout)
        delegate = MyDelegate()
        self.pandasTv.setItemDelegate(delegate)  ## Set Custom Delegate to Model.
        self.pandasTv.horizontalHeader().setStretchLastSection(True)
        self.pandasTv.setAlternatingRowColors(True)  ## Enable colouring alternate rows

        self.pandasTv.setSortingEnabled(0)  ## Set value to 1 if you want to Enable sorting(Not recommended for large data set)

        # Using ResizeToContents instead of Stretch makes the Application Laggy while switching Windows size and Tab.
        self.pandasTv.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.pandasTv.verticalHeader().setContextMenuPolicy(Qt.CustomContextMenu) ## Setting right click menu.
        self.pandasTv.verticalHeader().customContextMenuRequested.connect(self.getObjectHeaderContextMenu)


        self.setLayout(self.layout)
        self.set_values()  ## Set values in table for the first time.

        self._manager = ManagerCursor(self)  ## this is a Custom Cursor which is better looking than Normal Cursor
        movie = QtGui.QMovie(":/icons/giphy.gif")  ## You can change the animation of cursor by changing this file name with your own.
        movie.setScaledSize(QtCore.QSize(100,90))
        self._manager.setMovie(movie)
        self._manager.setWidget(self)


    def set_values(self): ##Set Values for the given Module when it's opened for first time.

        self.df = pd.DataFrame(columns=self.ModuleColumns,index=range(1000))
        self.df = self.df.fillna('')
        model = PandasModel(self.df)
        self.pandasTv.setModel(model)

    def reset_table(self):  ## Reset Table
        self.pandasTv.model().set_values(self.ModuleColumns, QtCore.QModelIndex())


    def loadFile(self):  ## Load files

        filter = "XLSX (*.xlsx);;CSV (*.csv)"  ## choose only xlsx and csv
        file_name = QtWidgets.QFileDialog()
        fileName, ok = file_name.getOpenFileName(self, "Open File", "", filter)
        if ok:
            try:
                df = pd.read_csv(fileName)
            except:
                df = pd.read_excel(fileName)
            if self.validate_uploaded_file(df):  ##verify it before showing to user.

                model = PandasModel(df)
                self.pandasTv.setModel(model)

            else:  ## show message if file is not valid.
                welcome_title = 'Alert'
                message = "Uploaded file does not belong to the selected module.\n\n"
                WelcomeNotification(self).notify(WelcomeNotification.ERROR, message,welcome_title, button_text='OK')

    def validate_uploaded_file(self,df): ## To validate the Uploaded Files and verfies whether the uploaded file belongs to same module.

        Columns = list(df.columns)
        original_columns = list(self.ModuleColumns)
        for i in range(len(Columns)):
            Columns[i] = Columns[i].lower()
        for i in range(len(original_columns)):
            original_columns[i] = original_columns[i].lower()
        if set(Columns)!=set(original_columns):
            return 0
        return 1

    def _control_opacity(self):  ## To control Opacity
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


    def getObjectHeaderContextMenu(self, pos):  ## Right Click menu. It appears when we click on header of selected rows.
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

    def deleteSelectedRows(self): ## Delete all selected Rows

        self.pandasTv.model().clearRows(self.selectedRows())

    def selectedRows(self): ## Get all the selected rows.

        selectedIndexes = self.pandasTv.selectedIndexes()
        rows = set()
        for index in selectedIndexes:
            rows.add(index.row())
        return sorted(list(rows))

    def insertObjectBeforeSelectedObjects(self):  ## insert single row before selected row.

        selectedObjectIndices = self.selectedRows()
        self.pandasTv.model().insertRows(selectedObjectIndices[0], 1)

    def insertObjectAfterSelectedObjects(self):  ## Insert a single row after selected row

        selectedObjectIndices = self.selectedRows()
        self.pandasTv.model().insertRows(selectedObjectIndices[-1]+1, 1)

    def insertObjectsBeforeSelectedObjects(self):  ## insert rows before selected rows

        num, ok = QInputDialog.getInt(self, "Insert", '<html style="font-size:10pt;font-family:georgia;color:white;">Number of rows to insert</html>', 1, 1)
        if ok:
            selectedObjectIndices = self.selectedRows()
            self.pandasTv.model().insertRows(selectedObjectIndices[0], num)

    def insertObjectsAfterSelectedObjects(self): ##Insert rows after selected rows.

        num, ok = QInputDialog.getInt(self, "Insert", '<html style="font-size:10pt;font-family:georgia;color:white;">Number of rows to insert</html>', 1, 1)
        if ok:
            selectedObjectIndices = self.selectedRows()
            self.pandasTv.model().insertRows(selectedObjectIndices[-1]+1, num)

    def deleteRows(self): ## Function to delete selected rows.

        selectedObjectIndices = self.selectedRows()
        self.pandasTv.model().removeRows(selectedObjectIndices)

    def Clear_Table(self): ## Ask for confirmation to  clear the table

        welcome_title = 'Confirmation'
        message = "All the data will be deleted. Do you wish to clear the whole table?\n\n"
        x = WelcomeNotification(self)
        x.notify(WelcomeNotification.QUESTION, message,welcome_title, button_text='NO',flag=1,text="YES")
        x.close_button.clicked.connect(self.confirmation)
        x.close_button_1.clicked.connect(self.confirmation)


    def confirmation(self):  ## Take confirmation from user to clear the table

        if self.sender().objectName() == 'close_button_notification':
            return
        if self.sender().objectName() == 'close_button_notification_1':
            self.reset_table()

    def enable_btn(self):  ## Enable All buttons.
        self.file_upload_tb.setEnabled(1)
        self.download_tb.setEnabled(1)
        self.validate_tb.setEnabled(1)

    def disable_btn(self):  ## Disable all buttons
        self.file_upload_tb.setEnabled(0)
        self.download_tb.setEnabled(0)
        self.validate_tb.setEnabled(0)

    def data_empty(self):  #To Notify the user that Data is empty

        welcome_title = 'Alert'
        message = 'Seems like there is no data to Validate or Download.\n\n' \
        'NOTE : For any row to be considered as a valid data row there \n'\
        'must be some value in the column ID. Only Valid data row(s) will\n'\
        'be considered for Validation and Downloading.\n'
        WelcomeNotification(self).notify(WelcomeNotification.WARNING, message,welcome_title, button_text='OK')
        self.destroy_validate_thread()  ## Drstroy both the threads.
        self.destroy_download_thread()

    def Validate_Data(self):

        self.destroy_validate_thread()  ## Destroy already Validation threads
        self.disable_btn() ## Disable all buttons.

        Model = self.pandasTv.model()  ## Get Modified data from Model.
        df = Model._df.copy()

        self.count+=1   ## Count is used to give each thread a unique name
        Worker = Thread_for_Validate(df)
        thread = QThread()
        thread.setObjectName('main'+str(self.count))
        self.__Validatethreads.append((thread,Worker))
        Worker.moveToThread(thread)

        thread.started.connect(Worker.Check_unique_value)  ## connecting all thrad functions to Main UI functions
        Worker.Not_unique.connect(self.no_unique)
        Worker.Not_numeric.connect(self.no_numeric)
        Worker.No_error.connect(self.no_error)
        Worker.is_exception.connect(self.show_error)
        Worker.data_frame_empty.connect(self.data_empty)

        self._manager.start()  ## Set the busy Cursor
        thread.start()  ## start the thread.

    def show_error(self,msg):  ## Function to show error if any.

        self.destroy_validate_thread()
        welcome_title = 'Alert'
        message = "Cannot Validate data.There is no Column ID in the uploaded file.\n\n"
        WelcomeNotification(self).notify(WelcomeNotification.ERROR, message,welcome_title, button_text='OK')

    def no_unique(self):  ## To show that values in column ID are not unique.

        self.destroy_validate_thread()
        welcome_title = 'Alert'
        message = "All the values in the column ID is not unique. Please Check all the values once again.\n\n"
        WelcomeNotification(self).notify(WelcomeNotification.ERROR, message,welcome_title, button_text='OK')


    def no_numeric(self):  ## TO show that all the values are not unique

        self.destroy_validate_thread()
        welcome_title = 'Alert'
        message = 'Either all the values in the table is not Numeric or some of them are empty. \n Please Check all the values once again.\n\n'
        WelcomeNotification(self).notify(WelcomeNotification.ERROR, message,welcome_title, button_text='OK')


    def no_error(self):  ## Function to show messgae to user that their is no error in data Validation.

        self.destroy_validate_thread()  # destroy all threads
        welcome_title = 'Congratulations'
        message = 'All the data validated successfully. No error has been found. You can now download the data\n\n'
        WelcomeNotification(self).notify(WelcomeNotification.OK, message,welcome_title, button_text='OK')


    def destroy_validate_thread(self):  ## Destroys all Validating threads

        if self.__Validatethreads:   ## destroy all threads one by one.
            for thread,worker in self.__Validatethreads:
                thread.quit()
                thread.wait()

        self.enable_btn()  ## Enable all buttons
        self._manager.stop()  ## Stop busy cursor and return to normal


    def Download_data(self):
        filename = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if filename:

            self.destroy_download_thread()  ## Destroy already running threads(if any)

            self.progress_bar.show()
            self.progress_bar.setValue(0)  ## show progress bar and set value to zero
            self.disable_btn()    ## disable all buttons


            Model = self.pandasTv.model()
            df = Model._df.copy()           ## get the updated model or data
            self.count+=1
            Worker = Thread_for_Download(df,filename,self.module_name)
            thread = QThread()
            thread.setObjectName('main'+str(self.count))  ## unique name for each thread
            self.__Downloadthreads.append((thread,Worker))
            Worker.moveToThread(thread)

            thread.started.connect(Worker.start_download)  ## connect thread to various Main functions
            Worker.row_count.connect(self.show_counter)
            Worker.download_complete.connect(self.download_completed)
            Worker.data_frame_empty.connect(self.data_empty)
            Worker.is_exception.connect(self.show_error)

            self._manager.start()  ## set the busy cursor
            thread.start() ## start the thread

    def show_counter(self,count, current, length):  # this function updates progress bar from thread.So that UI don't freeze

        self.progress_bar.setValue(count)
        self.progress_bar.setText(f'{current} out of {length} file(s) downloaded.')

    def download_completed(self):  # Notifies user that download has been completed

        self.progress_bar.setValue(100)  ## reset progress bar
        self.progress_bar.hide()
        self.destroy_download_thread()  ## destroy all threads
        welcome_title = 'Congratulations'
        message = 'All the data has been downloaded in the chosen directory.\n\n'
        WelcomeNotification(self).notify(WelcomeNotification.OK, message,welcome_title, button_text='OK')  ## show the notification

    def destroy_download_thread(self):  ## Function to destroy all downloading threads.
        if self.__Downloadthreads:
            for thread,worker in self.__Downloadthreads:
                thread.quit()
                thread.wait()
        self.enable_btn()   ## enable all buttons
        self._manager.stop()  ## stop the busy cursor.
        self.progress_bar.hide()  ## hide progree bar

class TensionMember(FinPlate):
    """
    TensionMember Frame inherited from FinPlate
    """

    def __init__(self, parent=None):
        super(TensionMember, self).__init__(parent)

        self.setObjectName(self.__class__.__name__)
        self.ModuleColumns = ['ID','Member length','Tensile load','Support condition at End 1','Support condition at End 2']
        self.module_name = "TensionMember"
        self.set_values()

class BCEndPlate(FinPlate):


    def __init__(self,parent=None):
        super(BCEndPlate, self).__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.module_name = "BCEndPlate"
        self.ModuleColumns = ['ID','End plate type','Shear load','Axial Load','Moment Load','Bolt diameter','Bolt grade','Plate thickness']
        self.set_values()


class CleatAngle(FinPlate):


    def __init__(self,parent=None):
        super(CleatAngle, self).__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.module_name = "CleatAngle"
        self.ModuleColumns = ['ID','Angle leg 1','Angle leg 2','Angle thickness','Shear load','Bolt diameter','Bolt grade']
        self.set_values()
