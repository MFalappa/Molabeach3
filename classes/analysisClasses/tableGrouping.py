import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QListWidget,QListWidgetItem,QPushButton,QTableWidget,QWidget,QApplication,QVBoxLayout,QTableWidgetItem,QInputDialog




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
        ##
        ## Modifica il comportamento di drop
        # 1. controlla l'indice che corrisponde al puntatore del mouse quando sposti in su
        # e quando sposti in giu' una casella
        # 2. crea un dizionario unico che ricopia gli stessi elementi della tabella fino alla riga
        # del drop schippando l'elemento/elementi selezionati
        # 3. aggiungi gli elementi selezionati nel dizionario
        # 4. aggiungi gli elementi successivi
        # 5. canccella la tabella (self.clearTable)
        # 6. ricompila in base al dizionario
        # fix bug di cancellazione

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
                    if item is None:
                        dictMove[row][col] = {
                            'text': None,
                            'icon': None
                        }

                    else:
                        dictMove[row][col] = {
                            'text': item.text(),
                            'icon': item.icon()
                        }

                    self.takeItem(row,col)
            dictShift = {}
            for row in range(drop_row-1,self.rowCount()):

                item = self.item(row, 0)
                if not item is None:
                    dictShift[row] = {}
                    for col in range(self.columnCount()):
                        item = self.item(row,col)
                        if item is None:
                            dictShift[row][col] = {
                                'text': None,
                                'icon': None
                            }

                        else:
                            dictShift[row][col] = {
                                'text': item.text(),
                                'icon': item.icon()
                            }
                        self.takeItem(row, col)

            ii = drop_row - 1
            for row in dictMove.keys():
                for col in dictMove[row].keys():
                    text = dictMove[row][col]['text']
                    icon = dictMove[row][col]['icon']
                    if text is None:
                        continue
                    item = QTableWidgetItem(text)
                    item.setIcon(icon)
                    self.setItem(ii,col,item)
                ii += 1

            for row in dictShift.keys():
                for col in dictShift[row].keys():
                    text = dictShift[row][col]['text']
                    icon = dictShift[row][col]['icon']
                    if text is None:
                        continue
                    item = QTableWidgetItem(text)
                    item.setIcon(icon)
                    self.setItem(ii,col,item)
                ii += 1

            for row in range(self.rowCount()):
                delRow = True
                for col in range(self.columnCount()):
                    if not self.item(row,col) is None:
                        delRow = False
                        break
                if delRow:
                    self.removeRow(row)
            print('took all items')


        elif event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text" )
            stream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
            # quanti elementi ho selezionatp
            num_drag = stream.readInt()
            oldRowNum = self.rowCount()

            self.setRowCount(oldRowNum+num_drag)
            group, okPressed  = QInputDialog.getText(self,'Insert Group Name','Group name:')

            for row in range(oldRowNum,oldRowNum+num_drag):

                item = QTableWidgetItem(group)
                self.setItem(row,0,item)
                dataName = stream.readQString()
                dataIcon = QtGui.QIcon()
                stream >> dataIcon

                item = QTableWidgetItem(dataName)
                item.setIcon(dataIcon)
                self.setItem(row,1,item)

            # item = QTableWidgetItem(text)
            # item.setIcon(icon)
            # drop_row = self.rowCount() + 1
            # self.setItem(drop_row,drop_col, item)
            # # event.setDropAction(QtCore.Qt.CopyAction)
            # event.accept()
            # self.dropped.emit(drop_row)
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
        dndListWidget = MyDnDListWidget()
        for column in range(columns):
            for row in range(rows):
                item = QTableWidgetItem('Text%d' % row)
                self.table.setItem(row, column, item)
        layout = QVBoxLayout(self)

        path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        #        path = '/Users/Matte/Python_script/Phenopy3/'
        i = 0
        for image in sorted(os.listdir(os.path.join(path, "images"))):
            if image.endswith(".png") or image.endswith(".ico"):
                item = QListWidgetItem(image.split(".")[0].capitalize())
                if i in [0, 2, 3]:
                    item.setIcon(QtGui.QIcon(os.path.join(path,
                                                    "images/{0}".format(image))))
                i += 1
                dndListWidget.addItem(item)


        layout.addWidget(self.table)
        layout.addWidget(dndListWidget)

        self.table.setMouseTracking(True)
        self.table.itemEntered.connect(self.handleItemEntered)
        self.table.itemExited.connect(self.handleItemExited)

    def handleItemEntered(self, item):
        item.setBackground(QtGui.QColor('moccasin'))

    def handleItemExited(self, item):
        item.setBackground(QTableWidgetItem().background())

if __name__ == '__main__':

    import sys,os
    sys.path.append('/Users/edoardo/Work/Code/phenopy/dialogsAndWidget/analysisDlg')
    from MyDnDDialog import MyDnDListWidget
    app = QApplication(sys.argv)
    window = Window(6, 3)
    window.setGeometry(500, 300, 350, 250)
    window.show()
    sys.exit(app.exec_())