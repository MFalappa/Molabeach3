# -*- coding: utf-8 -*-
"""
Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

Copyright (C) 2017 FONDAZIONE ISTITUTO ITALIANO DI TECNOLOGIA
                   E. Balzani, M. Falappa - All rights reserved

@author: edoardo.balzani87@gmail.com; mfalappa@outlook.it

                                Publication:
         An approach to monitoring home-cage behavior in mice that
                          facilitates data sharing

        DOI: 10.1038/nprot.2018.031

"""

import sys
import os
from PyQt5.QtCore import (QByteArray, QDataStream, QIODevice, QMimeData,
                          QPoint, pyqtSignal, Qt)

from PyQt5.QtWidgets import (QAbstractItemView, QGridLayout, QDialog,
                             QApplication, QListWidgetItem, QListWidget)

from PyQt5.QtGui import (QCursor, QDrag, QIcon)


class dNdModeList(QListWidget):
    dropped = pyqtSignal(int)
    dragged = pyqtSignal(int)

    def __init__(self, acceptDrop, acceptDrag, dropAction=Qt.CopyAction, parent=None):
        super(dNdModeList, self).__init__(parent)
#        super(dNdModeDlg, self).__init__(parent)
        self.setAcceptDrops(acceptDrop)
        self.setDragEnabled(acceptDrag)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.dropAction = dropAction

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):

        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QDataStream(data, QIODevice.ReadOnly)
            num_drag = stream.readInt()
            for k in range(num_drag):
                text = stream.readQString()
                icon = QIcon()
                stream >> icon
                item = QListWidgetItem(text)
                item.setIcon(icon)
                items = self.findItems(text, Qt.MatchExactly)
                if len(items) > 1:
                    event.setDropAction(Qt.CopyAction)
                    event.ignore()
                    print('Ignora')
                else:
                    qpoint = self.mapFromGlobal(QCursor.pos())
                    itemIndex = self.indexAt(qpoint)
                    drop_row = itemIndex.row()
                    if drop_row is -1:
                        drop_row = self.count()
                    else:
                        drop_row += 1
                    self.insertItem(drop_row, item)
                    event.setDropAction(Qt.MoveAction)
                    event.accept()
                    self.dropped.emit(drop_row)
        else:
            event.ignore()

    def startDrag(self, dropActions):
        list_items = self.selectedItems()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeInt(len(list_items))
        for item in list_items:
            icon = item.icon()
            stream.writeQString(item.text())
            stream << icon
        mimeData = QMimeData()
        mimeData.setData("application/x-icon-and-text", data)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = icon.pixmap(24, 24)
        drag.setHotSpot(QPoint(12, 12))
        drag.setPixmap(pixmap)
        if drag.exec_(self.dropAction) == Qt.MoveAction:
            for item in list_items:
                self.takeItem(self.row(item))
            self.dragged.emit(list_items)


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        dndListWidget = dNdModeList(acceptDrag=True,acceptDrop=False)
        path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        #        path = '/Users/Matte/Python_script/Phenopy3/'
        i = 0
        for image in sorted(os.listdir(os.path.join(path, "images"))):
            if image.endswith(".png") or image.endswith(".ico"):
                item = QListWidgetItem(image.split(".")[0].capitalize())
                if i in [0, 2, 3]:
                    item.setIcon(QIcon(os.path.join(path,
                                                    "images/{0}".format(image))))
                i += 1
                dndListWidget.addItem(item)
        dndIconListWidget = dNdModeList(acceptDrag=False,acceptDrop=True)
        dndIconListWidget.setViewMode(QListWidget.IconMode)

        layout = QGridLayout()
        layout.addWidget(dndListWidget, 0, 0)
        layout.addWidget(dndIconListWidget, 0, 1)

        self.setLayout(layout)

        self.setWindowTitle("Custom Drag and Drop")


def main():
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
