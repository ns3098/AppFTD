import os.path
from PyQt5.QtCore import QThread, QObject, pyqtSignal
import pandas as pd
import numpy as np

## This a thread class used for threading so that UI should not freeze.

class Thread_for_Validate(QObject):  # thread for data validation

    Not_unique = pyqtSignal()
    Not_numeric = pyqtSignal()
    No_error = pyqtSignal()   ## differnet type of signals
    data_frame_empty = pyqtSignal()
    is_exception = pyqtSignal(str)

    def __init__(self,df):
        QThread.__init__(self)
        self.df = df

    def Check_unique_value(self):
        columns = list(self.df.columns)
        lower_columns = list(map(lambda x:x.lower().strip(),columns))
        if 'id' in lower_columns and lower_columns.count('id')==1:  ## Specifically checks for coulmn id and it's uniqueness
            idx = lower_columns.index('id')
            text = columns[idx]
            self.df[text].replace('', np.nan, inplace=True)
            self.df.dropna(subset=[text], inplace=True)  ## drop all rows having no value in column id.
            if not self.df.empty:  ## check if data frame is empty
                boolean = self.df[text].duplicated().any()  ## Check for duplicates in column id.

                if(boolean):  ## If there is duplicate emit the signal

                    self.Not_unique.emit()
                else:  ## Else check if all the values are numeric or not.

                    self.Check_numeric_value()
            else:
                self.data_frame_empty.emit()
        else:
            self.is_exception.emit('No Unique Column ID in the uploaded file.')

    def Check_numeric_value(self):   ## TO check if values are numeric only.

        self.df.replace('','x',inplace=True)
        Boolean = dict(self.df.apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all()))
        False_count = list(Boolean.values()).count(False)

        if False_count > 0:  ## If not Numeric
            self.Not_numeric.emit()

        else:
            self.No_error.emit()

class Thread_for_Download(QObject):   ## thread for downloading.

    row_count = pyqtSignal('PyQt_PyObject','PyQt_PyObject','PyQt_PyObject')
    download_complete = pyqtSignal()
    data_frame_empty = pyqtSignal()
    is_exception = pyqtSignal(str)

    def __init__(self,df, filename, module_name):

        QThread.__init__(self)
        self.df = df
        self.filename = filename
        self.ModuleName = module_name

    def start_download(self):
        columns = list(self.df.columns)
        lower_columns = list(map(lambda x:x.lower().strip(),columns))
        if 'id' in lower_columns and lower_columns.count('id')==1: ## Same as validation thread.
            idx = lower_columns.index('id')
            text = columns[idx]
            self.df[text].replace('', np.nan, inplace=True)
            self.df.dropna(subset=[text], inplace=True)
            if not self.df.empty:

                values = self.df.to_dict(orient='records')  ## get all the data in dictionary form.
                length  = len(values)
                total = 100 / length
                for i in range(length):
                    name_of_file = self.ModuleName+'_'+str(values[i][text])  ## Give file name
                    complete_name = os.path.join(self.filename,name_of_file+".txt")
                    file = open(complete_name,'w')
                    toFile = str(values[i])
                    file.write(toFile)
                    file.close()
                    self.row_count.emit(total*(i+1),i+1,length)  ## Send data to update progress bar.

                self.download_complete.emit()

            else:
                self.data_frame_empty.emit()

        else:
            self.is_exception.emit('No Column ID in the uploaded file.')
