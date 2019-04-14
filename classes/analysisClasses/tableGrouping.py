import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton,QTableWidget,QWidget,QApplication,QVBoxLayout,QTableWidgetItem




class TableWidget(QTableWidget):
    dropped = QtCore.pyqtSignal(int)
    dragged = QtCore.pyqtSignal(int)
    cellExited = QtCore.pyqtSignal(int, int)
    itemExited = QtCore.pyqtSignal(QTableWidgetItem)

    def __init__(self, rows, columns,dragAndDropCol=2,tableID='input_table', parent=None):
        QTableWidget.__init__(self, rows, columns, parent)
        self._last_index = QtCore.QPersistentModelIndex()
        self.viewport().installEventFilter(self)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.tableID = tableID
        # use this to mark which col use for dropping
        self.dragAndDropCol = dragAndDropCol
        self.lastDrop = []
        # self.dragged.connect(self.dropEvent)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text")\
                or event.mimeData().hasFormat("%s/x-icon-and-text"%self.tableID):
            event.accept()
        else:
            event.ignore()

    def startDrag(self, dropActions):
        list_items = self.selectedItems()
        data = QtCore.QByteArray()
        stream = QtCore.QDataStream(data, QtCore.QIODevice.WriteOnly)
        stream.writeInt(len(list_items))
        # if len(list_items) != 1:
        #     raise IndexError
        for item in list_items:

            rowDrag = item.row()
            stream.writeInt(rowDrag)
            # stream.writeQString(itemCol.text())
            # stream << icon
        mimeData = QtCore.QMimeData()
        mimeData.setData("%s/x-icon-and-text"%self.tableID, data)
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = item.icon().pixmap(24, 24)
        drag.setHotSpot(QtCore.QPoint(12, 12))
        drag.setPixmap(pixmap)
        drag.exec_(QtCore.Qt.CopyAction) #== QtCore.Qt.CopyAction:
        # for item in list_items:
        #     self.takeItem(self.row(item),self.column(item))
        self.dragged.emit(len(list_items))

    def dragMoveEvent(self, event):
        # print('drag move')
        if event.mimeData().hasFormat("application/x-icon-and-text")\
                or event.mimeData().hasFormat("%s/x-icon-and-text"%self.tableID):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()


        else:
            event.ignore()

    def dropEvent(self, event):
        print('drop enter')
        if event.mimeData().hasFormat("%s/x-icon-and-text"%self.tableID):
            lstDrop = []
            data = event.mimeData().data("%s/x-icon-and-text"%self.tableID)
            stream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
            # quanti elementi ho selezionatp
            num_drag = stream.readInt()
            # mouse prosition
            qpoint = self.mapFromGlobal(QtGui.QCursor.pos())
            # take the corresponding item
            itemIndex = self.indexAt(qpoint)
            drop_row = itemIndex.row()
            # creare num_drag colonne nuove
            print(self.rowCount())
            self.setRowCount(self.rowCount()+num_drag)
            dictMove = {}
            for kk in range(num_drag):
                row = stream.readInt()
                dictMove[row] = {}
                for col in range(self.columnCount()):
                    item = self.item(row,col)
                    dictMove[row][col] = {
                        'text':item.text(),
                        'icon':item.icon()
                    }
                    self.takeItem(row,col)
            dictShift = {}
            for row in range(drop_row-1,self.rowCount()):

                item = self.item(row, 0)
                if not item is None:
                    dictShift[row] = {}
                    for col in range(self.columnCount()):
                        dictShift[row][col] = {
                            'text':item.text(),
                            'icon':item.icon()
                        }
                        self.takeItem(row, col)

            ii = drop_row - 1
            for row in dictMove.keys():
                for col in dictMove[row].keys():
                    text = dictMove[row][col]['text']
                    icon = dictMove[row][col]['icon']
                    item = QTableWidgetItem(text)
                    item.setIcon(icon)
                    self.setItem(ii,col,item)
                ii += 1

            for row in dictShift.keys():
                for col in dictShift[row].keys():
                    text = dictShift[row][col]['text']
                    icon = dictShift[row][col]['icon']
                    item = QTableWidgetItem(text)
                    item.setIcon(icon)
                    self.setItem(ii,col,item)
                ii += 1

            self.setRowCount(ii)
            print('took all items')


        elif event.mimeData().hasFormat("application/x-icon-and-text"):
            ####
            item = QTableWidgetItem(text)
            item.setIcon(icon)
            drop_row = self.rowCount() + 1
            self.setItem(drop_row,drop_col, item)
            # event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            self.dropped.emit(drop_row)
        else:
            event.ignore()


    def eventFilter(self, widget, event):
        if widget is self.viewport():
            index = self._last_index
            if event.type() == QtCore.QEvent.MouseMove:
                index = self.indexAt(event.pos())
            elif event.type() == QtCore.QEvent.Leave:
                index = QtCore.QModelIndex()
            if index != self._last_index:
                row = self._last_index.row()
                column = self._last_index.column()
                item = self.item(row, column)
                if item is not None:
                    self.itemExited.emit(item)
                self.cellExited.emit(row, column)
                self._last_index = QtCore.QPersistentModelIndex(index)
        return QTableWidget.eventFilter(self, widget, event)

class Window(QWidget):
    def __init__(self, rows, columns):
        QWidget.__init__(self)
        self.table = TableWidget(rows, columns,2,'input_table', self)
        for column in range(columns):
            for row in range(rows):
                item = QTableWidgetItem('Text%d' % row)
                self.table.setItem(row, column, item)
        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        self.table.setMouseTracking(True)
        self.table.itemEntered.connect(self.handleItemEntered)
        self.table.itemExited.connect(self.handleItemExited)

    def handleItemEntered(self, item):
        item.setBackground(QtGui.QColor('moccasin'))

    def handleItemExited(self, item):
        item.setBackground(QTableWidgetItem().background())

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = Window(6, 3)
    window.setGeometry(500, 300, 350, 250)
    window.show()
    sys.exit(app.exec_())