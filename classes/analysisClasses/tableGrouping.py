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

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    def startDrag(self, dropActions):
        list_items = self.selectedItems()
        data = QtCore.QByteArray()
        stream = QtCore.QDataStream(data, QtCore.QIODevice.WriteOnly)
        stream.writeInt(len(list_items))
        if len(list_items) != 1:
            raise IndexError
        item = list_items[0]

        rowDrag = item.row()
        for col in range(self.columnCount()):
            itemCol = self.item(rowDrag,col)
            icon = itemCol.icon()
            stream.writeQString(itemCol.text())
            stream << icon
        mimeData = QtCore.QMimeData()
        mimeData.setData("%s/x-icon-and-text"%self.tableID, data)
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = icon.pixmap(24, 24)
        drag.setHotSpot(QtCore.QPoint(12, 12))
        drag.setPixmap(pixmap)
        # if drag.exec_(QtCore.Qt.CopyAction) == QtCore.Qt.MoveAction:
        #     for item in list_items:
        #         self.takeItem(self.row(item),self.column(item))
        #     self.dragged.emit(list_items)

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):

        if event.mimeData().hasFormat("%s/x-icon-and-text"%self.tableID):
            lstDrop = []
            data = event.mimeData().data("%s/x-icon-and-text"%self.tableID)
            stream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
            num_drag = stream.readInt()
            # mouse prosition
            qpoint = self.mapFromGlobal(QtGui.QCursor.pos())
            # take the corresponding item
            itemIndex = self.indexAt(qpoint)
            drop_row = itemIndex.row()
            dictInfo = {}

            for col in self.columnCount():
                text = stream.readQString()
                icon = QtGui.QIcon()
                stream >> icon
                dictInfo[col] = {'text':text,'icon':icon}

            items = self.findItems(dictInfo[self.dragAndDropCol]['text'], QtCore.Qt.MatchExactly)
            matchInCol = False

            for item in items:
                if item.column() == self.dragAndDropCol:
                    matchInCol = True
                    break
            # if item present switch the dropped with the old item
            if matchInCol:
                # crea un altro dizionatio con testo e icona della riga che va sostituita
                # e switcha tutti gli elementi
                # change content of the matched item and set the content of the current
                itemMv = self.item(itemIndex.row()-1,itemIndex.column())
                # print('match',items[0].row())
                # print(text,icon)
                print(itemMv.text(),itemIndex.row())

                item.setText(itemMv.text())
                item.setIcon(itemMv.icon())

                itemMv.setText(text)
                itemMv.setIcon(icon)
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