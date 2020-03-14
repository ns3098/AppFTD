from PyQt5 import QtCore
from PyQt5.QtCore import *
import pandas as pd

'''
This is a custom Model used to show Pandas DataFrame.
Making a QAbstractTableModel is beneficial in many ways
It can handle large amount of datas without being laggy unlike QTableWidget
We can use many different functions to modify our data because pandas is full
of such magical functions.
'''
class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, df = pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df
        self._df = self._df.applymap(str)
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.TextAlignmentRole:
            return Qt.AlignCenter

        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        #return QtCore.QVariant(str(self._df.ix[index.row(), index.column()]))
        return QtCore.QVariant(str(self._df.iloc[index.row() ,index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        print(row,col)
        if hasattr(value, 'toPyObject'):
            value = value.toPyObject()
        else:
            self._df.at[row,col]=value
            return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):  ## used for sorting columns

        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

    def flags(self, index):

        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def insertRows(self, position, count=1, parent=QtCore.QModelIndex()):  ## To insrt rows

        self.layoutAboutToBeChanged.emit()
        cols=list(self._df.columns)
        line = pd.DataFrame({x:'' for x in cols},index=list(range(count)))
        self._df = pd.concat([self._df.iloc[:position], line, self._df.iloc[position:]])
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

    def removeRows(self, position,parent=QtCore.QModelIndex()):  ## To remove rows.

        self.layoutAboutToBeChanged.emit()
        self._df = self._df.drop(position)
        self._df.reset_index(inplace=True,drop=True)
        self.layoutChanged.emit()

    def set_values(self, Columns, parent=QtCore.QModelIndex()):  ## Reset Dtaaframe values

        self.layoutAboutToBeChanged.emit()
        self._df = pd.DataFrame(columns=Columns,index=range(1000))
        self._df = self._df.fillna('')
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

    def clearRows(self, indexes, parent=QtCore.QModelIndex()):   ## Clear content of selected rows.

        self.layoutAboutToBeChanged.emit()
        self._df.iloc[indexes] = ''
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()
