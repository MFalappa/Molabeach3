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
from PyQt5.QtWidgets import QMainWindow,QApplication,QFileDialog
from PyQt5.QtCore import pyqtSignal,QObject
from ui_spike_gui import Ui_Form
import os, sys

classes_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'libraries')
phenopy_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'mainScripts')
import_dir = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")),'import')

sys.path.append(classes_dir)
sys.path.append(phenopy_dir)
sys.path.append(import_dir)

from importDataset import load_Spike_Data
        
class spk_gui(QMainWindow, Ui_Form, QObject):
    spkSig = pyqtSignal(str,name='spkSignal')
    closeSpike = pyqtSignal(str,name='closeSpike')
    def __init__(self,parent=None):
        super(spk_gui, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_done.clicked.connect(self.close)
        self.pushButton_save.clicked.connect(self.saveAct)
  
        self.pushButton_import.clicked.connect(self.importAction)
        self.pushButton_load.clicked.connect(self.loadAction)
        self.pushButton_save.clicked.connect(self.saveAction)
        
#        self.comboBox_cluster.setEnabled(True)
#        self.comboBox_cluster.addItem('ciao')
#        self.comboBox_cluster.addItem('bau')

        
    def saveAction(self):
        pass
#        item_selected = self.listWidget_file.selectedItems()
#        if not len(item_selected):
#            return
#        list_save = []
#        for item in item_selected:
#            list_save += [item.text()]
#        
#          
#        directory = os.path.dirname(os.path.abspath(os.path.join(__file__ ,"../..")))
#        Qfnames=QFileDialog.getOpenFileNames(self,
#                    "Spike GUI - Save Spike Data", directory)
                    
#        now = datetime.now()
#        time = now.year,now.month,now.day,now.hour,now.minute
#        savename = os.path.join(dirname,'workspace_%d-%d-%dT%d_%d'%time + '.phz')
#        try:
#            self.lock.lockForWrite()
#            for label in list_save:
#                self.Dataset.changePath(label,savename)
#            save_data_container(self.Dataset,list_save,dirname,fname=savename)
#        finally:
#            self.lock.unlock()
#        self.lastSaveDirectory = dirname
        
    def importAction(self):
        directory = os.path.dirname(os.path.abspath(os.path.join(__file__ ,"../..")))
        Qfnames=QFileDialog.getOpenFileNames(self,
                    "Spike GUI - Import Spike Data", directory)
        for name in Qfnames:
            load_Spike_Data(name)
            self.listWidget_file.addItem(os.path.basename(name))
            
    def loadAction(self):
        directory = os.path.dirname(os.path.abspath(os.path.join(__file__ ,"../..")))
        formats =([u'*.phz'])
        Qfnames=(QFileDialog.getOpenFileNames(self,
                    "Spike GUI - Load Spike Data", directory,
                    "Input files ({0})".format(" ".join(formats))))

        for name in Qfnames:
            load_Spike_Data(name)
            self.listWidget_file.addItem(os.path.basename(name))
           
       
    def saveAct(self):
        print('sono qui')        
        pass
    
    def closeTab(self):
        self.close()
        self.closeSpike.emit('spk_gui')
        
def main():
    import sys
    
    
    app = QApplication(sys.argv)
    dlg = spk_gui()
    dlg.show()
    app.exec_()
    return dlg
    
if __name__ == '__main__':
    dlg = main()