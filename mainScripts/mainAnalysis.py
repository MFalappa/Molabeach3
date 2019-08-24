# -*- coding: utf-8 -*-
""""
Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

Copyright (C) 2017 FONDAZIONE ISTITUTO ITALIANO DI TECNOLOGIA
                   E. Balzani, M. Falappa - All rights reserved

@author: edoardo.balzani87@gmail.com; mfalappa@outlook.it

                                Publication:
         An approach to monitoring home-cage behavior in mice that 
                          facilitates data sharing
        
        DOI: 10.1038/nprot.2018.031      
"""

import sys,os
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
phenopy_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
file_dir = os.path.dirname(phenopy_dir)
import_dir = os.path.join(file_dir,'import')

image_dir = os.path.join(file_dir,'images')
sys.path.append(os.path.join(file_dir,'libraries'))
sys.path.append(os.path.join(file_dir,'dialogsAndWidget','analysisDlg'))
sys.path.append(os.path.join(file_dir,'classes','analysisClasses'))
sys.path.append(os.path.join(file_dir,'export'))
sys.path.append(os.path.join(file_dir,'future'))
sys.path.append(import_dir)

from PyQt5.QtCore import (QSettings,QTimer, Qt, QReadWriteLock)
from PyQt5.QtWidgets import (QAction, QApplication, QDockWidget, QFileDialog,
                             QFrame, QInputDialog, QLabel, QListWidget, 
                             QListWidgetItem,QMainWindow, QMessageBox,
                             QLineEdit, QAbstractItemView,QTabWidget)

from PyQt5.QtGui import (QIcon,QImage,QKeySequence,QPixmap)

from get_folder_and_format_dlg_export import get_export_info_dlg
from Wizard_New_Analysis import new_Analysis_Wizard
from datainfodlg import datainfodlg
from protocol_save_files import load_npz,save_data_container


from Input_Dlg_std import inputDialog
from copy import copy

from plot_Launcher_all import select_Function_GUI_all

import datetime as dt
import numpy as np
import pandas as pd

#import matplotlib.pylab as plt


from importDatasetDlg import importDlg

from Class_Analisi import (Analysis_Single_GUI, Analysis_Group_GUI)

from export_files import select_export
from editDatasetDlg import editDlg
from Modify_Dataset_GUI import (DatasetContainer_GUI,Dataset_GUI)

from AnalysisThread import analysis_thread
from analysis_data_type_class import refreshTypeList

#from spikeGUI import spk_gui
from sleepWidget import sleepDlg
from behavWidget import behavDlg
from integrativeWidget import integrativeDlg
from dragAndDropModes import dNdModeList

__version__ = "2.0.0"


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
#       Recording Original TimeStamps:        
        self.TimeStamps={}
        self.TimeStampsKey=['Start Month','Start Day','Start Year','Start Hour',
                            'Start Minute','Start Second','ACT_MILLI','End Month',
                            'End Day','End Year','ACT_SUBJECT','ACT_EXPID','ACT_PHASE',
                            'ACT_BOXID','ACT_TRIAL',
                            
                            'House Light On','House Light Off','Left Light On',
                            'Left Light Off','Center Light On','Center Light Off',
                            'Right Light On','Right Light Off','Left NP In','Left NP Out',
                            'Center NP In','Center NP Out','Right NP In','Right NP Out',
                            'Give Pellet Left','Give Pellet Right','ACT_TTL_HIGH',
                            'ACT_TTL_LOW','Start Intertrial Interval','End Intertrial Interval',
                            'ACT_TIMEOUT_REACHED','Probe Trial','ACT_LEFT_NOISE_ON',
                            'ACT_LEFT_NOISE_OFF','ACT_MID_NOISE_ON','ACT_MID_NOISE_OFF',
                            'ACT_RIGHT_NOISE_ON','ACT_RIGHT_NOISE_OFF','ACT_ABORT_ACTION',
                            'ACT_END_GLOBAL_TRIAL','ACT_BATTERY_LOW','ACT_START_TEST',
                            
                            'ACT_MARK_1','ACT_MARK_2','ACT_MARK_3','ACT_MARK_4',
                            'ACT_MARK_5','ACT_MARK_6','ACT_MARK_7','ACT_MARK_8',
                            'ACT_MARK_9','ACT_MARK_10']
                            
        TimeStampsCode = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
                          20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,
                          38,39,40,41,42,43,44,45,46,47,48,49,50,51,
                          60,61,62,63,64,65,66,67,68,69]
        
        refreshTypeList(import_dir)
        # dictionary with keys group or single, contains a dict with
        # keys function names and values a list of the accepted types
        self.AnalysisAndLabels = np.load(os.path.join(os.path.dirname(__file__),'Analysis.npy'),allow_pickle=True).all()

        
        ind=0
        for key in self.TimeStampsKey:
            self.TimeStamps[key] = TimeStampsCode[ind]  
            ind+=1
            
#       Keeping Track of original timestamps
        self.OriginalTimeStamps = self.TimeStamps.copy()
        self.OriginalTimeStampsKey = copy(self.TimeStampsKey)


#       Input will contain the input used as well as the dataset name
#        self.Input = OrderedDict()

        self.filename = None
        self.currentDatasetLabel = None
        self.currentInput = None
        self.currentInputName = None
        self.lastOpenFileDirectory=None
        self.flagData=False
        self.flagInput = False
        self.lastSaveDirectory = None
        self.sleepAction_option = False

#       self.InputOrData is a flag to specify if you are saving an input or a 
#       dataset, if you press save when an input is the last selected you will 
#       save this input, if a dataset is the last selected you will save this 
#       dataset

        self.InputOrData = None

#       Usual Time Scale in which the dataset are rescaled
        self.scale=1000

#       Image in the middle
        self.imageLabel = QLabel()
        self.imageLabel.setMinimumSize(200, 200)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        Logo=QImage(os.path.join(image_dir,'phenopyLogo.png'))
        self.imageLabel.setPixmap(QPixmap.fromImage(Logo))
        self.setCentralWidget(self.imageLabel)        
 
#       Dock widgets: 1 for the input, 1 for the dataset,1 for the log        
        logDockWidgetRight = QDockWidget("Log", self)
        logDockWidgetRight.setObjectName("LogDockWidgetRight")
        logDockWidgetRight.setAllowedAreas(Qt.RightDockWidgetArea)
        logDockWidgetRight.setMaximumWidth(300)
        self.listWidgetRight = QListWidget()
        
        logDockWidgetRight.setWidget(self.listWidgetRight)
        self.addDockWidget(Qt.RightDockWidgetArea, logDockWidgetRight)
        
        logDockWidgetLeft = QDockWidget("Loaded Datasets", self)
        logDockWidgetLeft.setObjectName("LoadedDockWidgetLeft")
        logDockWidgetLeft.setAllowedAreas(Qt.LeftDockWidgetArea)                                      
        logDockWidgetLeft.setMaximumWidth(300)
        
        self.listWidgetLeft = dNdModeList(acceptDrag=True,acceptDrop=False)
        
        logDockWidgetLeft.setWidget(self.listWidgetLeft)
        self.addDockWidget(Qt.LeftDockWidgetArea, logDockWidgetLeft)
        self.listWidgetLeft.setSelectionMode(QAbstractItemView.ExtendedSelection)
                                     
#       Size label, left lower corner.
        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        self.setWindowState(Qt.WindowMaximized)
        self.status = self.statusBar()
        self.status.setSizeGripEnabled(False)
        self.status.addPermanentWidget(self.sizeLabel)
        self.status.showMessage("Ready", 5000)
        
#       Creating all the actions... open,save, quit, Option...        
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                QKeySequence.Open, "fileopen", "Open an existing dataset")
        
        fileImportAction = self.createAction("&Import...", self.importExternalData,
                None, "fileImport", "Import an external dataset")
        
        self.fileExportAction = self.createAction("&Export...", self.exportData,
                None, "fileExport", "Import an external dataset")
        
        self.fileExportAction.setEnabled(False)
        
        self.fileSaveAsAction = self.createAction("Save &As...",
                self.fileSaveAs, icon="filesaveas", tip="Save the selected dataset")
        self.fileSaveAsAction.setEnabled(False)
        
        fileQuitAction = self.createAction("&Quit", self.close,
                "Ctrl+Q", "filequit", "Close the application")
                
        self.dataInfoAction = self.createAction("&Dataset Info",self.DataInfo,
                                           None,None,"Information about the dataset")
        
        self.imageLabel.addAction(fileQuitAction)
        
        startWizardAction = self.createAction('&Upload Analysis',self.startWizard,None,
                                              None,'Upload a new function for data analysis')
        
                                                      
        self.spikeAction = self.createAction('&Spike Analysis',self.startSpikeAnalysis,
                                             None,'wave_spike','Perform spike analysis')
        
        self.sleepAction = self.createAction('&Sleep Analysis',self.startSleepAnalysis,
                                             None,None,'Perform sleep analysis, EEG and EMG data')    
        
        self.behaviourAction = self.createAction('&Behaviour Analysis',self.startBehaviourAnalysis,
                                                 None,None,'Perform behavioural analysis, code action data')
        
        self.integrativenAction = self.createAction('&Integrative Analysis',self.startIntegrativeAnalysis,
                                                 None,None,'Perform analysis from different recordings')                      
                                              
                                   
        clearLogAction = self.createAction('Clear Log',self.listWidgetRight.clear,None,'rubber','Clear Log')
                                        
        self.removeDatasetAction = self.createAction('Remove selected dataset',self.RemoveDataset,
                                                     None,None,'Remove Dataset')
        self.removeAllDatasetAction = self.createAction('Remove all',self.RemoveAllDataset,
                                                        None,None,'Remove all')
        
        self.renameDatasetAction = self.createAction('Rename Dataset',self.renameData,
                                                     'F2',None,'Rename selected dataset')
        
        self.editFunctDlgAction = self.createAction('&Edit Dataset...',self.startEditDlg,
                                                    "CTRL+E",None)
    
#       Creating the Menu file, edit and analyzing, using the created action,
#       if an action is related to an icon, the icon will be displayed in the menu
        self.fileMenu = self.menuBar().addMenu("&File")
        
        fileMenuActions_Before = (fileOpenAction,fileImportAction,
                                  self.fileExportAction,self.fileSaveAsAction)
        self.addActions(self.fileMenu,fileMenuActions_Before)
                                            
        fileMenuActions_After = ( None,fileQuitAction)
        self.addActions(self.fileMenu,fileMenuActions_After)
        
        self.editMenu = self.menuBar().addMenu('&Edit')
        self.addActions(self.editMenu,(self.editFunctDlgAction,))
        analysisMenu=self.menuBar().addMenu("&Analysis")
        
        self.integrativenAction.setEnabled(False)
        self.spikeAction.setEnabled(False)
        self.sleepAction.setEnabled(False)
        self.behaviourAction.setEnabled(False)
        
        self.addActions(analysisMenu,(self.sleepAction,
                                      self.behaviourAction,
                                      self.integrativenAction,
                                      self.spikeAction,
                                      startWizardAction))
                                      
#       Creating a toolbar menu, as in the menus we use the action created that
#       are already associated with icon and connected
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, ( fileOpenAction,self.fileSaveAsAction))
                                      
        logToolbar = self.addToolBar("Log")
        logToolbar.setObjectName("LogToolBar")
        
        
        self.addActions(logToolbar,(clearLogAction,
                                    self.sleepAction,
                                    self.behaviourAction,
                                    self.integrativenAction,
                                    self.spikeAction))
                                      
        self.imageLabel.addAction(fileQuitAction)
        
        self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        self.addActions(self.listWidgetLeft,(self.fileSaveAsAction,
                                             self.renameDatasetAction,
                                             self.dataInfoAction,
                                             self.removeDatasetAction,
                                             self.removeAllDatasetAction))
        
        
        self.listWidgetLeft.setContextMenuPolicy(Qt.ActionsContextMenu)

#       Restoring previous settings like the geometry of the window, the movements
#       of the dock widgets, the last imported dataset, the time stamp list,
#       the last directory we used to open datasets

        fname=[]
        try:    
            settings = QSettings()
            settingsKeys = settings.childKeys()

            # Restoring TimeStamps Code or Use the normal one
#            if 'TimeStampsKey 0' in settingsKeys:
#                
#                self.TimeStampsKey = []
#                self.TimeStamps={}
#                KeyNum=0
#                while 'TimeStampsKey %d'%KeyNum in settingsKeys:
#                    self.TimeStampsKey = self.TimeStampsKey + [settings.value('TimeStampsKey %d'%KeyNum)]
#                    self.TimeStamps[self.TimeStampsKey[-1]]=settings.value('TimeStampsCode %d'%KeyNum)
#                    KeyNum+=1
                    
            
            self.restoreGeometry(
                    settings.value("MainWindow/Geometry"))
            self.restoreState(settings.value("MainWindow/State"))
            
            self.lastOpenFileDirectory = settings.value('LastOpenFileDirectory')
            if 'ScaleFactor' in settingsKeys:
                self.scale=settings.value('ScaleFactor')
            if not len(self.lastOpenFileDirectory):
                self.lastOpenFileDirectory=None
            
            
            for key in settingsKeys:
                key=str(key)
                first_word_key = key.split(' ')[0]
                
                if (key!='MainWindow/Geometry' and key!='MainWindow/State' 
                            and key!='LastOpenFileDirectory'
                            and first_word_key!='Group' and first_word_key!='Single'
                            and first_word_key!='Type'
                            and key!='ScaleFactor'
                            and not 'TimeStampsCode' in key
                            and not 'TimeStampsKey' in key
                            and not 'SaveDirectory' in key):
                    
                    fname = fname + [settings.value(key)]                    
        except:
            pass
        


        self.setWindowTitle("PhenoPY [*]")
        self.setWindowIcon(QIcon(os.path.join(image_dir,"logo.ico")))
        QTimer.singleShot(0, lambda Name = fname: self.loadInitialFile(Name))
#        self.Dataset = DatasetContainer_GUI(self.TimeStamps)
        self.Dataset = DatasetContainer_GUI(self.OriginalTimeStamps)
        self.Dataset.updateSignal.connect(self.updateDataListWidget)
        
#       Analisis single thread
        self.lock = QReadWriteLock()
        
        self.analysisThread = analysis_thread(self.Dataset,self.lock)

        # questi segnali vanno sistemati
        self.analysisThread.threadFinished.connect(lambda Type = 'General': self.completedAnalysis(Type))
        
#       connecting Dockwidget items to some methods   
        self.listWidgetLeft.itemClicked.connect(self.UpdateCurrentDataset)
        self.listWidgetLeft.customContextMenuRequested.connect(self.on_context_menu)
        self.listWidgetLeft.itemSelectionChanged.connect(self.enable_disable_actions)

    
    def enable_disable_actions(self):
        
        if len(self.listWidgetLeft.selectedItems()):
            self.fileSaveAsAction.setEnabled(True)
            self.fileExportAction.setEnabled(True)
        else:
            self.fileSaveAsAction.setEnabled(False)
            self.fileExportAction.setEnabled(False)
    
    def startWizard(self):
        dialog = new_Analysis_Wizard(parent=self)
        dialog.editedDictionary.connect(self.updateAnalysisDict)
        dialog.show()

    def updateAnalysisDict(self,analysisDict):
        # change to the new dict using singal connection from the wizard
        self.AnalysisAndLabels = analysisDict
        # get the central widget
        centralWidget = self.centralWidget()
        # check if the tabs are open and refresh the widget
        if type(centralWidget) == QTabWidget:
            for tabidx in range(centralWidget.count()):
                anWidget = centralWidget.widget(tabidx)
                anWidget.analysisDict = analysisDict

                anWidget.populateCombo()
        # method disconnect not working


        
    def startEditDlg(self):
        dialog = editDlg(parent=self)
        dialog.exec_()
        
    def exportData(self):
        item_selected = self.listWidgetLeft.selectedItems()
        if not len(item_selected):
            return
        dialog = get_export_info_dlg(parent=self)
        if not dialog.exec_():
            return
        path_folder = dialog.path_folder
        ext = dialog.ext
        delim = dialog.delim
        if delim == '\\t':
            delim = '\t'
        for item in item_selected:
            try:
                self.lock.lockForRead()
                label = item.text()
                if ext == '.phz':
                    data_exp = self.Dataset[label]
                else:
                    data_exp = self.Dataset.takeDataset(label)
            finally:
                self.lock.unlock()
            path = os.path.join(path_folder)
            res = select_export(data_exp,path,delimiter=delim)
            self.listWidgetRight.addItem(res[1])
            
        
    def importExternalData(self):
        
        if type(self.centralWidget()) is QTabWidget:
            tabWidget = self.centralWidget()
            for idx in range(tabWidget.count()):
                if type(tabWidget.widget(idx)) == importDlg:
                    return
        else:
            tabWidget = QTabWidget() 
        
        dlg = importDlg(parent=self)
        dlg.errorImport.connect(self.listWidgetRight.addItem)
        tabWidget.addTab(dlg,'Import data')
        self.setCentralWidget(tabWidget)
        func = lambda : self.removeTab(importDlg)
        dlg.closeSig.connect(func)
        
    
    def on_context_menu(self, point):
        self.listWidgetLeftMenu.exec_(self.listWidgetLeftMenu.mapToGlobal(point))  
        
    def loadInitialFile(self,fname):
        answ = QMessageBox.question(self,'Load last dataset?', 
                                    'Do you want to load last session dataset?',
                                    QMessageBox.No|QMessageBox.Yes)

        if answ != 16384:
            fname = []
        existingFile=[]
        
        for name in fname:

            if type(name) is str:
                if os.path.exists(name) and name.endswith('.phz'):
                    # need to ckeck if it is a string since the list contains also other objects.
                    # need to check why when it closes
                    # saves in memory weird stuff... anyway this will work smoothly anyway
                    existingFile += [name]

        if len(existingFile):
            self.loadFile(existingFile)
 
    def fileOpen(self):
        dire = (self.lastOpenFileDirectory
               if self.lastOpenFileDirectory is not None else ".")
        formats =(['*.phz'])
        Qfnames,_=(QFileDialog.getOpenFileNames(self,
                    "Phenopy - Load Dataset", dire,
                    "Input files ({0})".format(" ".join(formats))))
        fnames = []  
        for ind in range(len(Qfnames)):
                fnames = fnames + [str(Qfnames[ind])]
        if len(fnames)>0:
            self.lastOpenFileDirectory=os.path.dirname(fnames[0])
        if fnames:
            self.loadFile(fnames)
                    
    def loadFile(self, fnames=None):
        """
            Load npz file that are renamed as phz, because they must
            contain an object of the class Dataset_Container_GUI
        """
        self.filename = None
        list_npz = []
        for File in fnames:
            if File.endswith('.phz'):
                list_npz += [File]
        self.Dataset = load_npz(list_npz, self.Dataset)

    def updateDataListWidget(self):
        """
            Metodo chiamato da datacontainer ogni volta che viene aggiunto
            o tolto un dataset.
        """
        self.listWidgetLeft.clear()
        for item_name in list(self.Dataset.keys()):
            item = QListWidgetItem(item_name)
            item.setIcon(QIcon(os.path.join(image_dir,"table.png")))
            self.listWidgetLeft.addItem(item)
        
        # va ancora aggiunta la possibilita delle integrative
        if len(list(self.Dataset.keys())) >= 1:
            for dts in self.Dataset.keys():
                if self.Dataset[dts].Types == ['TSE']:
                    self.behaviourAction.setEnabled(True)
                
                elif self.Dataset[dts].Types == ['MED_SW']:
                    self.behaviourAction.setEnabled(True)
                
                elif self.Dataset[dts].Types == ['AM-Microsystems']:
                    self.behaviourAction.setEnabled(True)
                
                elif self.Dataset[dts].Types == ['EEG Binned Frequencies']:
                    self.sleepAction.setEnabled(True)
            
                elif self.Dataset[dts].Types == ['EEG Full Power Spectrum']:
                    self.sleepAction.setEnabled(True)
                
                elif self.Dataset[dts].Types == ['Unparsed Excel File']:
                    print('decidere con edo')
                
                elif self.Dataset[dts].Types == ['Parsed Excel']:
                    print('decidere con edo')
                
                elif self.Dataset[dts].Types == ['single unit struct']:
                    self.spikeAction.setEnabled(True)
                
                elif self.Dataset[dts].Types == ['nex_file']:
                    print('decidere con edo, pensavo ad un modulo ad hoc per la detection')    
                
                elif self.Dataset[dts].Types == ['EDF']:
                    self.sleepAction_option = True
                    
                    
        else:
            self.behaviourAction.setEnabled(False)
            self.sleepAction.setEnabled(False)
            self.integrativenAction.setEnabled(False)
            self.spikeAction.setEnabled(False)
        
        if self.sleepAction.isEnabled() and self.behaviourAction.isEnabled():
            self.integrativenAction.setEnabled(True)
        elif self.sleepAction.isEnabled() and self.sleepAction_option:
            self.integrativenAction.setEnabled(True)
        else:
            self.integrativenAction.setEnabled(False)


    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(os.path.join(image_dir,"%s.png" % icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)
    
    def fileSaveAs(self):
        item_selected = self.listWidgetLeft.selectedItems()
        if not len(item_selected):
            return
        list_save = []
        for item in item_selected:
            list_save += [item.text()]
        if self.lastSaveDirectory:
            directory = self.lastSaveDirectory
        else:
            directory = self.Dataset.path(list_save[0])
            if not directory:
                directory = os.path.curdir
        dirname = QFileDialog.getExistingDirectory(self,
                  "Phenopy - Save selection", directory)
        now = dt.datetime.now()
        time = now.year,now.month,now.day,now.hour,now.minute
        savename = os.path.join(dirname,'workspace_%d-%d-%dT%d_%d'%time + '.phz')
        try:
            self.lock.lockForWrite()
            for label in list_save:
                self.Dataset.changePath(label,savename)
            save_data_container(self.Dataset,list_save,dirname,fname=savename)
        finally:
            self.lock.unlock()
        self.lastSaveDirectory = dirname

    def DataInfo(self):
        Item = self.listWidgetLeft.currentItem()
        Dataname = str(Item.text())
        self.status.showMessage('Loading Dataset Info...',0)
        try:
            self.lock.lockForRead()
            dialog = datainfodlg(self.Dataset._DatasetContainer_GUI__Datas[Dataname],
                             Path=self.Dataset.path(Dataname),
                             TimeStamps=self.TimeStamps,lock=self.lock,parent=self)
            oldTypes=copy(self.Dataset.dataType(Dataname))
        finally:
            self.lock.unlock()
            self.status.showMessage('Dataset Loaded',0)
        self.status.clearMessage()
        dialog.exec_()
        try:
            self.lock.lockForRead()
            newTypes = self.Dataset.dataType(Dataname)
        finally:
            self.lock.unlock()
        if oldTypes != newTypes:
            self.listWidgetRight.addItem('Dataset %s types modified'%Dataname)
    
#    def ConvertToEditTimeStampsFormat(self):
#        List=[]
#        for key in self.TimeStampsKey:
#            List  = List + [(key,self.TimeStamps[key])]
#        return List
        
#    def updateLog(self,message):
#        self.listWidgetRight.addItem(message)
        
    def UpdateCurrentDataset(self):
        self.currentDatasetLabel=str(self.listWidgetLeft.item(self.listWidgetLeft.currentRow()).text())
        self.InputOrData = True
        
#    def UpdateCurrentInput(self):
#        Row = self.listInputWidgetLeft.currentRow()
#        self.currentInput['Analysis'] = str(self.listInputWidgetLeft.item(Row).text())
#        self.currentInput['Input'] = self.Input[str(self.listInputWidgetLeft.item(Row).text())]
#        self.listWidgetRight.addItem('Selected Input %s'%str(self.listInputWidgetLeft.item(Row).text()))
#        self.InputOrData = False
        
    def closeEvent(self, event):

        settings = QSettings()
        settings.setValue("MainWindow/Geometry", self.saveGeometry())
        settings.setValue("MainWindow/State", self.saveState())
        settings.setValue('LastOpenFileDirectory',self.lastOpenFileDirectory)
        settings.setValue('ScaleFactor',self.scale)
        settingsKeys = settings.childKeys()
        for key in settingsKeys:
            if (str(key) !="MainWindow/Geometry" and str(key)!="MainWindow/State" 
                and str(key)!='LastOpenFileDirectory' and key!='ScaleFactor'):
                settings.remove(key)
        try:
            self.lock.lockForRead()
            list_fname = []
            for key in list(self.Dataset.keys()):
                filename = self.Dataset.path(key)
                if filename and not (filename in list_fname):
                    list_fname += [filename]
                    settings.setValue(key,filename)
        finally:
            self.lock.unlock()
        
        KeyNum=0
        for key in self.TimeStampsKey:
            TimeStampLabel = key
            TimeStampCode = self.TimeStamps[key]
            settings.setValue('TimeStampsKey %d'%KeyNum,TimeStampLabel)
            settings.setValue('TimeStampsCode %d'%KeyNum,TimeStampCode)
            KeyNum+=1
        
            
    def RemoveDataset(self):
        if self.analysisThread.isRunning():
            QMessageBox.warning(self, 'Running analysis thread',
            'Wait until the analysis is finished')
            return
        list_items = self.listWidgetLeft.selectedItems()
        remove_list = []
        for item in list_items:
           remove_list += [item.text()]
        for label in remove_list:  
            self.Dataset.remove(label)
        
    def RemoveAllDataset(self):
        if self.analysisThread.isRunning():
            QMessageBox.warning(self, 'Running analysis thread',
            'Wait until the analysis is finished')
            return
        reply = QMessageBox.question(self, "Remove all Datasets", 
                                     "Remove all Datasets?",
                                     QMessageBox.Yes|QMessageBox.No)
        
        if reply == QMessageBox.Yes :
            self.listWidgetLeft.clear()
            self.Dataset.clear()
    

    # qui vanno lanciate le varie analisi    
    def startSpikeAnalysis(self):
        print('andrebbe ridesignato in base a cio che vogliamo mettere')
    
    def startSleepAnalysis(self):
        if type(self.centralWidget()) is QTabWidget:
            tabWidget = self.centralWidget()
            for idx in range(tabWidget.count()):
                if type(tabWidget.widget(idx)) == sleepDlg:
                    return
        else:
            tabWidget = QTabWidget() 
            
        dlg = sleepDlg(self.Dataset,self.AnalysisAndLabels,parent = self)
        
        tabWidget.addTab(dlg,'Sleep Toolbox')
        self.setCentralWidget(tabWidget)
        func = lambda : self.removeTab(sleepDlg)
        dlg.closeSig.connect(func)
        dlg.runAnalysisSig.connect(self.startAnalysis)
    
        
    def startBehaviourAnalysis(self):
        if type(self.centralWidget()) is QTabWidget:
            tabWidget = self.centralWidget()
            for idx in range(tabWidget.count()):
                if type(tabWidget.widget(idx)) == behavDlg:
                    return
        else:
            tabWidget = QTabWidget() 

        # In order to keep pheopy flexible we need to pass the available analysis to the widget
        # the checker box and layout them by itself...
        # we don't have a distinction
        dlg = behavDlg(self.Dataset,self.AnalysisAndLabels,parent=self)

        tabWidget.addTab(dlg,'Behaviour Toolbox')
        self.setCentralWidget(tabWidget)
        func = lambda : self.removeTab(behavDlg)
        dlg.closeSig.connect(func)
        dlg.runAnalysisSig.connect(self.startAnalysis)
    
    def startIntegrativeAnalysis(self):
        if type(self.centralWidget()) is QTabWidget:
            tabWidget = self.centralWidget()
            for idx in range(tabWidget.count()):
                if type(tabWidget.widget(idx)) == integrativeDlg:
                    return
        else:
            tabWidget = QTabWidget() 

        # In order to keep pheopy flexible we need to pass the available analysis to the widget
        # the checker box and layout them by itself...
        # we don't have a distinction
        dlg = integrativeDlg(self.Dataset,self.AnalysisAndLabels,parent=self)

        tabWidget.addTab(dlg,'Integrative Toolbox')
        self.setCentralWidget(tabWidget)
        func = lambda : self.removeTab(integrativeDlg)
        dlg.closeSig.connect(func)
        dlg.runAnalysisSig.connect(self.startAnalysis)
        
        
    def removeTab(self,tabName):
        tabWidget = self.centralWidget()
        for idx in range(tabWidget.count()):
            if type(tabWidget.widget(idx)) == tabName:
                tabWidget.removeTab(idx)
                break
        if tabWidget.count() == 0:
            Logo = QImage(os.path.join(image_dir,'phenopyLogo.png'))
            self.imageLabel = QLabel()
            self.imageLabel.setMinimumSize(200, 200)
            self.imageLabel.setAlignment(Qt.AlignCenter)
            self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
            self.imageLabel.setPixmap(QPixmap.fromImage(Logo))
            self.setCentralWidget(self.imageLabel)
        
    def startAnalysis(self,analysisDict):

        anType = analysisDict['anType']
        analysisName = analysisDict['analysisName']
        selectedDataDict = analysisDict['Groups']
        pairedGroups = analysisDict['Pairing']

        analysisThread = self.analysisThread
        if anType in ['Group', 'Integrative']:
            analysisCreator = Analysis_Group_GUI            
        else:
            analysisCreator = Analysis_Single_GUI
        
        createAnalysis = analysisCreator(analysisName)
        inputCreator = createAnalysis.inputCreator
        
        Input = self.inputDlgLauncher(inputCreator,selectedDataDict)  
        
        if Input == -1:
            self.enableActionAfterAnalysis(anType)
            return
        self.disableActionDuringAnalysis(anType) 
        
        analysisThread.initialize(Input, analysisName,
                                  selectedDataDict, self.TimeStamps,pairedGroups)

#        analysisThread.start() # uncomment for parallel execution
        analysisThread.run()
        self.status.showMessage('%s analysis is running'%analysisName)
        

            
    def inputDlgLauncher(self,inputCreator, selectedDataDict):
        Input = {}

        phaseSel = None
        if not inputCreator.returnInput(0,'PhaseSel') is None:
            phaseSel = [self.Dataset, np.hstack(list(selectedDataDict.values()))]
            
        for dialogNum in inputCreator.returnListDlg():
            dialog = inputDialog(inputCreator.returnInput(dialogNum,'DataName'),
                                 inputCreator.returnInput(dialogNum,'Combo'),
                                 inputCreator.returnInput(dialogNum,'TimeSpinBox'),
                                 inputCreator.returnInput(dialogNum,'DoubleSpinBox'),
                                 inputCreator.returnInput(dialogNum,'LineEdit'),
                                 inputCreator.returnInput(dialogNum,'SpinBox'),
                                 inputCreator.returnInput(dialogNum,'NewDataLineEdit'),
                                 1,
                                 inputCreator.returnInput(dialogNum,'ActivityList'),
                                 inputCreator.returnInput(dialogNum,'SavingDetails'),
                                 inputCreator.returnInput(dialogNum,'RadioButton'),
                                 inputCreator.returnInput(dialogNum,'Range'),
                                 inputCreator.returnInput(dialogNum,'TimeRange'),
                                 phaseSel,
                                 parent = self)
            if not dialog.exec_():
                return -1
            Input[dialogNum] = dialog.createStdOutput()

        return Input

    def disableActionDuringAnalysis(self,Type):
        self.renameDatasetAction.setEnabled(False)
        self.removeAllDatasetAction.setEnabled(False)
        self.removeDatasetAction.setEnabled(False)
        
    def enableActionAfterAnalysis(self,Type):
        self.renameDatasetAction.setEnabled(True)
        self.removeAllDatasetAction.setEnabled(True)
        self.removeDatasetAction.setEnabled(True)

    def completedAnalysis(self, Type):
        self.status.showMessage('')
        self.enableActionAfterAnalysis(Type)
        
        thread = self.analysisThread
        
        try:
            Dir = thread.savingDetails[0]
            Dir = Dir.rstrip('\\')
            ext = thread.savingDetails[1]
            Save = True
        except:
            Save = False

        analysisName = thread.analysisName
        dataDict = thread.outputData
        inputs = thread.inputForPlots
        info = thread.info
        if inputs is None:
            self.listWidgetRight.addItem('Unable to perform analysis %s'%analysisName)
            return

        
        figDict = select_Function_GUI_all(analysisName,inputs)
        
        if not Save:
            return
        for analysis in list(figDict.keys()):
            DirFig = os.path.join(Dir,analysis)
            if not os.path.exists(DirFig):
                os.mkdir(DirFig)
            for figKey in list(figDict[analysis].keys()):
                fig = figDict[analysis][figKey]
                try:
                    fileName = os.path.join(DirFig, figKey + ext)
                    fig.savefig(fileName)
                except IndexError:
                    print('Unable to save figure%s\n%s'\
                        %(analysis,figKey))
        for analysis in list(dataDict.keys()):


            if not os.path.exists(Dir):
                os.mkdir(Dir)
            
            try:
                writer = pd.ExcelWriter(os.path.join(Dir, analysis+ '.xlsx'))
    
                for dataKey in list(dataDict[analysis].keys()):
                    dataDict[analysis][dataKey].to_excel(writer,sheet_name=dataKey)
                    
                writer.save()
                writer.close()


        
            except IndexError:
                print('Unable to save data:\n%s\n%s'%(analysis,dataKey))
            
            try:
                self.AddDatasetToList(dataDict[analysis][dataKey],
                                      dataKey,info[dataKey]['Types'],
                                      None)
            except IndexError:
                print('Unable to add labels to list')
 
    def renameData(self):
        if self.analysisThread.isRunning():
            self.analysisThread.wait()
        row = self.listWidgetLeft.currentRow()
        title = "Rename Dataset"
        item = self.listWidgetLeft.item(row)
        if item is not None:
            string, ok = QInputDialog.getText(self, title, title,
                    QLineEdit.Normal, item.text())
            if ok and string != '':                
                k=1
                Item = self.listWidgetLeft.findItems(string,Qt.MatchExactly)
              
                while len(Item)==1:
                    row1 = self.listWidgetLeft.row(Item[0])
                    if row1==row:
                        return
                    elif len(string.split('.'))==2:
                        string=string.split('.')[0]+'_%d'%k+'.'+string.split('.')[1]
                    else:
                        string=string.split('.')[0]+'_%d'%k
                    Item = self.listWidgetLeft.findItems(string,Qt.MatchExactly)
                    k+=1
                
                item.setText(string)
                self.Dataset.changeKey(self.currentDatasetLabel,str(string))                
                self.listWidgetRight.addItem('Dataset %s\nrenamed to %s'%(self.currentDatasetLabel,str(string)))
                self.currentDatasetLabel = str(string)

                        
    def AddDatasetToList(self,Extracted_Data,Name,Types,FactorColumns=None):
        try:
            self.lock.lockForRead()
            boolean = Name in self.Dataset
        finally:
            self.lock.unlock()
        if boolean:
            reply=QMessageBox.question(self,'Name Conflict',\
                'Do you want to replace data %s?'\
                %Name,QMessageBox.No|QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                if self.analysisThread.isRunning():
                    self.analysisThread.wait()
                self.Dataset.pop(Name)
                self.flagData=False
                self.listWidgetRight.addItem('Replaced dataset %s'%Name)
                
        Items = self.listWidgetLeft.findItems(Name,Qt.MatchExactly)
        for item in Items:
            self.listWidgetLeft.takeItem(self.listWidgetLeft.row(item))
        data = Dataset_GUI(Extracted_Data,Name,Types=Types,FactorColumns=FactorColumns)
        try:
            self.lock.lockForWrite()
            self.Dataset.add(data)
        finally:
            self.lock.unlock()
            
def main():   
    
    app = QApplication(sys.argv)
    app.setOrganizationName("Qtrac Ltd.")
    app.setOrganizationDomain("qtrac.eu")
    app.setApplicationName("PhenoPy GUI")
    app.setWindowIcon(QIcon(os.path.join(image_dir,"logo.ico")))
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
