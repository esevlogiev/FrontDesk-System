import sys
from PyQt5.QtCore import QAbstractItemModel, Qt, QVariant, QModelIndex
from PyQt5.QtWidgets import QTableView, QAbstractScrollArea, QApplication

MAID_CHARACTERISTICS = 2

class MaidModel(QAbstractItemModel):
    def __init__(self):
        super(MaidModel, self).__init__()
        self.maids = []

    def set_maids(self, maids):
        self.beginResetModel()
        self.maids = maids
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self.maids)

    def columnCount(self, parent=QModelIndex()):
        return MAID_CHARACTERISTICS

    def data(self, index, role):
        if (not self.hasIndex(index.row(), index.column()) or
           role != Qt.DisplayRole):
            return QVariant()

        maid = self.maids[index.row()]
        if index.column() in (0, 1):
            return maid[index.column()]

        return QVariant()

    def index(self, row, column, parent=QModelIndex()):
        if self.is_valid_row_index(row) and self.is_valid_column_index(column):
            return self.createIndex(row, column)
        else:
            return QModelIndex()

    def is_valid_row_index(self, row_index):
        return 0 <= row_index and row_index < self.rowCount()

    def is_valid_column_index(self, column_index):
        return 0 <= column_index and column_index < self.columnCount()


    def parent(self, child):
        return QModelIndex()

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Vertical:
            if not self.is_valid_row_index(section):
                return QVariant()
            else:
                return section + 1
        if orientation == Qt.Horizontal:
            if not self.is_valid_column_index(section):
                return QVariant()
            else:
                return ('First Name', 'Last Name')[section]
        return QVariant()
