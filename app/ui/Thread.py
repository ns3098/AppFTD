import os.path
from PyQt5.QtCore import QThread, QObject, pyqtSignal
import pandas as pd
import numpy as np


class Thread_for_Validate(QObject):

    Not_unique = pyqtSignal()
    Not_numeric = pyqtSignal()
    No_error = pyqtSignal()
    data_frame_empty = pyqtSignal()
    is_exception = pyqtSignal(str)

    def __init__(self,df):
        QThread.__init__(self)
        self.df = df

    def Check_unique_value(self):
        try:
            self.df['year'].replace('', np.nan, inplace=True)
            self.df.dropna(subset=['year'], inplace=True)

            if not self.df.empty:
                boolean = self.df['year'].duplicated().any()

                if(boolean):

                    self.Not_unique.emit()
                else:

                    self.Check_numeric_value()
            else:
                self.data_frame_empty.emit()

        except Exception as e:
            self.is_exception.emit(str(e))


    def Check_numeric_value(self):

        self.df.replace('',0.0,inplace=True)
        Boolean = dict(self.df.apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all()))
        False_count = list(Boolean.values()).count(False)

        if False_count > 0:
            self.Not_numeric.emit()

        else:
            self.No_error.emit()

class Thread_for_Download(QObject):

    row_count = pyqtSignal('PyQt_PyObject','PyQt_PyObject','PyQt_PyObject')
    download_complete = pyqtSignal()
    data_frame_empty = pyqtSignal()
    is_exception = pyqtSignal(str)

    def __init__(self,df, filename):

        QThread.__init__(self)
        self.df = df
        self.filename = filename

    def start_download(self):
        try:
            self.df['year'].replace('', np.nan, inplace=True)
            self.df.dropna(subset=['year'], inplace=True)
            if not self.df.empty:
                values = self.df.to_dict(orient='records')
                length  = len(values)
                total = 100 / length

                for i in range(length):
                    name_of_file = str(i+1)
                    complete_name = os.path.join(self.filename,name_of_file+".txt")
                    file = open(complete_name,'w')
                    toFile = str(values[i])
                    file.write(toFile)
                    file.close()
                    self.row_count.emit(total*(i+1),i+1,length)

                self.download_complete.emit()

            else:
                self.data_frame_empty.emit()

        except Exception as e:
            self.is_exception.emit(str(e))
