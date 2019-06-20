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
from pairDataDlg import pairDataDlg
from datainfodlg import datainfodlg 
from protocol_save_files import load_npz,save_data_container
from AnalysisSingle_Std import analysisSingle_thread

from Input_Dlg_std import inputDialog
from copy import copy

from plot_Launcher import select_Function_GUI
from plot_Launcher_Gr import select_Function_GUI_Gr    

import datetime as dt
import numpy as np

#import matplotlib.pylab as plt


from importDatasetDlg import importDlg

from Class_Analisi import (Analysis_Single_GUI, Analysis_Group_GUI)

from export_files import select_export
from editDatasetDlg import editDlg
from Modify_Dataset_GUI import (OrderedDict,DatasetContainer_GUI,Dataset_GUI,
                               save_A_Data_GUI)

from AnalysisGroup_Std  import analysisGroup_thread
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
        self.AnalysisAndLabels = np.load(os.path.join(os.path.dirname(__file__),'Analysis.npy')).all()

        self.AnalysisAndLabels['Single'] = OrderedDict(self.AnalysisAndLabels['Single'])
        self.AnalysisAndLabels['Group'] = OrderedDict(self.AnalysisAndLabels['Group'])
        
        
        ind=0
        for key in self.TimeStampsKey:
            self.TimeStamps[key] = TimeStampsCode[ind]  
            ind+=1
            
#       Keeping Track of original timestamps
        self.OriginalTimeStamps = self.TimeStamps.copy()
        self.OriginalTimeStampsKey = copy(self.TimeStampsKey)
#        plt.ion()

#       Input will contain the input used as well as the dataset name
        self.Input = OrderedDict()

        self.filename = None
        self.currentDatasetLabel = None
        self.currentInput = None
        self.currentInputName = None
        self.lastOpenFileDirectory=None
        self.flagData=False
        self.flagInput = False
        self.lastSaveDirectory = None

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
        
        
#        self.analysisAction  = self.createAction('&Analyze Data',self.startAnalysis,
#                                        'Ctrl+A', None,'Perform a single group analysis')
        
                                              
        self.spikeAction = self.createAction('&Spike Analysis',self.startSpikeAnalysis,
                                             None,'wave_spike','Perform spike analysis')
        
        self.sleepAction = self.createAction('&Sleep Analysis',self.startSleepAnalysis,
                                             None,None,'Perform sleep analysis, EEG and EMG data')    
        
        self.behaviourAction = self.createAction('&Behaviour Analysis',self.startBehaviourAnalysis,
                                                 None,None,'Perform behavioural analysis, code action data')
        
        self.integrativenAction = self.createAction('&Integrative Analysis',self.startIntegrativeAnalysis,
                                                 None,None,'Perform analysis from different recordings')                      
                                              
#        self.extractingDataAction=self.createAction('Extract time stamps',self.extractingData,
#                                                    None,None,'Extract timestamps from dataset')    
                                   
        clearLogAction = self.createAction('Clear Log',self.listWidgetRight.clear,None,'rubber','Clear Log')
                                        
        self.removeDatasetAction = self.createAction('Remove selected dataset',self.RemoveDataset,
                                                     None,None,'Remove Dataset')
        self.removeAllDatasetAction = self.createAction('Remove all',self.RemoveAllDataset,
                                                        None,None,'Remove all')
        
        self.renameDatasetAction = self.createAction('Rename Dataset',self.renameData,
                                                     'F2',None,'Rename selected dataset')

        #c'è un seganle da sistemare
#        self.editSelectIntervalAction = self.createAction("Select &Interval",self.editSelectInterval,
#                                                          "Alt+I", None,"Keep only a selected time inteval",
#                                                          signal='triggered()')
        
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
            if 'TimeStampsKey 0' in settingsKeys:
                
                self.TimeStampsKey = []
                self.TimeStamps={}
                KeyNum=0
                while 'TimeStampsKey %d'%KeyNum in settingsKeys:
                    self.TimeStampsKey = self.TimeStampsKey + [settings.value('TimeStampsKey %d'%KeyNum)]
                    self.TimeStamps[self.TimeStampsKey[-1]]=settings.value('TimeStampsCode %d'%KeyNum)
                    KeyNum+=1
                    
            
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
        self.Dataset = DatasetContainer_GUI(self.TimeStamps)
        self.Dataset.updateSignal.connect(self.updateDataListWidget)
        
#       Analisis single thread
        self.lock = QReadWriteLock()
        self.analysisSingleThread = analysisSingle_thread(self.Dataset,
                                                          self.lock,
                                                          self)
        self.analysisGroupThread = analysisGroup_thread(self.Dataset,
                                                          self.lock)

        # questi segnali vanno sistemati
        self.analysisSingleThread.threadFinished.connect(lambda Type = 'Single': self.completedAnalysis(Type))
        self.analysisGroupThread.threadFinished.connect(lambda Type = 'Group': self.completedAnalysis(Type))
        
#       connecting Dockwidget items to some methods   
        self.listWidgetLeft.itemClicked.connect(self.UpdateCurrentDataset)
        self.listWidgetLeft.customContextMenuRequested.connect(self.on_context_menu)
        self.listWidgetLeft.itemSelectionChanged.connect(self.enable_disable_actions)

# vecchia modalità
# vecchia modalità, lho cambiat ma non debuggata, vedi sopra
#        self.connect(self.analysisSingleThread,pyqtSignal('threadFinished()'),\
#                     lambda Type = 'Single': self.completedAnalysis(Type))
#        self.connect(self.analysisGroupThread,pyqtSignal('threadFinished()'),\
#                     lambda Type = 'Group': self.completedAnalysis(Type))
#        self.connect(self.listWidgetLeft,pyqtSignal("itemClicked (QListWidgetItem *)"),self.UpdateCurrentDataset)
#        self.connect(self.listWidgetLeft,pyqtSignal('customContextMenuRequested(const QPoint&)'),self.on_context_menu)
#        self.connect(self.listWidgetLeft,pyqtSignal('itemSelectionChanged ()'),self.enable_disable_actions)
    
    def enable_disable_actions(self):
        
        if len(self.listWidgetLeft.selectedItems()):
            self.fileSaveAsAction.setEnabled(True)
            self.fileExportAction.setEnabled(True)
        else:
            self.fileSaveAsAction.setEnabled(False)
            self.fileExportAction.setEnabled(False)
    
    def startWizard(self):
        dialog = new_Analysis_Wizard(parent=self)
        dialog.show()
        
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

    # questo va sistemato in base a se trova sleep, behavior o entrambe
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
                    self.sleepAction.setEnabled(True)
                    
        else:
            self.behaviourAction.setEnabled(False)
            self.sleepAction.setEnabled(False)
            self.integrativenAction.setEnabled(False)
            self.spikeAction.setEnabled(False)
        
        if self.sleepAction.isEnabled() and self.behaviourAction.isEnabled():
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
#        plt.close('all')
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
        
        for key in ['Single','Group']:
            KeyNum=0
            
            for analysis in list(self.AnalysisAndLabels[key].keys()):
                Analysis = analysis
                settings.setValue('%s %d'%(key,KeyNum),Analysis)
                KeyNum += 1
        
        for analysis in list(self.AnalysisAndLabels.keys()):
            KeyNum=0
            Types = self.AnalysisAndLabels[analysis]
            for Type in Types:
               AnType = Type
               settings.setValue('Type %s %d'%(analysis,KeyNum),AnType)

            
    def RemoveDataset(self):
        if self.analysisSingleThread.isRunning():
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
        if self.analysisSingleThread.isRunning():
            QMessageBox.warning(self, 'Running analysis thread',
            'Wait until the analysis is finished')
            return
        reply = QMessageBox.question(self, "Remove all Datasets", 
                                     "Remove all Datasets?",
                                     QMessageBox.Yes|QMessageBox.No)
        
        if reply == QMessageBox.Yes :
            self.listWidgetLeft.clear()
            self.Dataset.clear()
    
#    def dataTypeList(self):
#        """
#            This function returns a dataTypeList of the imported data
#        """
#        type_list = []
#        try:
#            self.lock.lockForRead()
#            for dataName, dataset in self.Dataset:
#                this_type = self.Dataset.dataType(dataName)[0]
#                if not this_type in type_list:
#                    type_list +=  [this_type]
#        finally:
#            self.lock.unlock()
#        return type_list
    
#    def subSetDataPerType(self,type_list):
#        """
#            Select over a subset of data tipes and retunrs a list of data 
#            names
#        """
#        data_list = []
#        try:
#            self.lock.lockForRead()
#            for name, tmp in self.Dataset:
#                if self.Dataset.dataType(name)[0] in type_list:
#                    data_list += [name]
#        finally:
#            self.lock.unlock()
#        return data_list
    
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

        tabWidget.addTab(dlg,'Behaviour Toolbox')
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
#        dataType = analysisDict['dataType']
        analysisName = analysisDict['analysisName']
        selectedDataDict = analysisDict['Groups']
        pairedGroups = analysisDict['Pairing']

#        if anType == 'Integrative':
#            # Data select and pairing
#            type_list = []
#            for tl in list(dataType.values()):
#                type_list += tl
#            paired_matrix = self.integrativeSpecificProcessing(analysisName)
#            if paired_matrix is None:
#                return
#        else:
#            type_list = dataType
#            paired_matrix = None

        
        if anType in ['Group', 'Integrative']:
            analysisCreator = Analysis_Group_GUI
            analysisThread = self.analysisGroupThread
            
        else:
            analysisCreator = Analysis_Single_GUI
            analysisThread = self.analysisSingleThread
        
#        pairedGroups = self.groupDictPerPaired(paired_matrix,selectedDataDict)
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
        
#    def groupDictPerPaired(self,paired_matrix, selectedDataDict):
#        if paired_matrix is None:
#            groupDict = None
#        else:
#            groupDict = {}
#            grouped = paired_matrix.dtype.names[1]
#            for group in list(selectedDataDict.keys()):
#                groupDict[group] = {}
#                for mat_type in paired_matrix.dtype.names[1:]:
#                    groupDict[group][mat_type] = []
#                for subject in selectedDataDict[group]:
#                    findRow = np.where(paired_matrix[grouped] == subject)[0][0]
#                    for mat_type in paired_matrix.dtype.names[1:]:
#                        groupDict[group][mat_type] += [paired_matrix[mat_type][findRow]]
#        return groupDict
                
        
#    def integrativeSpecificProcessing(self,analysisName):
#        dialog = pairDataDlg(self.AnalysisAndLabels['Integrative'][analysisName], self.Dataset,
#                             self.lock)
#        paired_matrix = None
#        if dialog.exec_():
#            paired_matrix = dialog.pairMatrix
#        return paired_matrix
            
    def inputDlgLauncher(self,inputCreator, selectedDataDict):
        Input = {}
#        print('inputDlg called')
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
#            if 'DoubleSpinBox' in Input[dialogNum]:
#                print(Input[dialogNum]['DoubleSpinBox'])
        return Input

    def disableActionDuringAnalysis(self,Type):
#        self.analysisAction.setEnabled(False)
        self.renameDatasetAction.setEnabled(False)
#        self.rescaleADatasetAction.setEnabled(False)
        self.removeAllDatasetAction.setEnabled(False)
        self.removeDatasetAction.setEnabled(False)
        
    def enableActionAfterAnalysis(self,Type):
        
#        self.analysisAction.setEnabled(True)
        self.renameDatasetAction.setEnabled(True)
#        self.rescaleADatasetAction.setEnabled(True)
        self.removeAllDatasetAction.setEnabled(True)
        self.removeDatasetAction.setEnabled(True)

    def completedAnalysis(self, Type):
        self.status.showMessage('')
        self.enableActionAfterAnalysis(Type)
       
        if Type == 'Single':
            thread = self.analysisSingleThread
            select_plotFun = select_Function_GUI
        else:
            thread = self.analysisGroupThread
            select_plotFun = select_Function_GUI_Gr
        try:
            Dir = thread.savingDetails[0]
            Dir = Dir.rstrip('\\')
            ext = thread.savingDetails[1]
            Save = True
        except:
            Save = False
#        plt.close('all')
        analysisName = thread.analysisName
        dataDict = thread.outputData
        inputs = thread.inputForPlots
        info = thread.info
        if inputs is None:
            self.listWidgetRight.addItem('Unable to perform analysis %s'%analysisName)
            return
#==============================================================================
#   modifico single subject plot come in gr analysis 
#==============================================================================
        
        figDict = select_plotFun(analysisName,inputs)
        
        if not Save:
            return
        for analysis in list(figDict.keys()):
            DirFig = os.path.join(Dir,analysis)
            if not os.path.exists(DirFig):
                os.mkdir(DirFig)
            for figKey in list(figDict[analysis].keys()):
                fig = figDict[analysis][figKey]
#                print('saving ',analysis,figKey)
                try:
#                    plt.show(block=False)
                    fileName = os.path.join(DirFig, figKey + ext)
                    fig.savefig(fileName)
                except IndexError:
                    print('Unable to save figure%s\n%s'\
                        %(analysis,figKey))
        for analysis in list(dataDict.keys()):
            DirData = os.path.join(Dir,analysis)
            if not os.path.exists(DirData):
                os.mkdir(DirData)
            for dataKey in list(dataDict[analysis].keys()):
                fileName = os.path.join(DirData,dataKey + '.csv')
#==============================================================================
#   MODIFICARE LA PROCEDURA DI SALVATAGGIO DATI c Generalizzare il piu' possibile!!!
#==============================================================================
                try:
                    if 'Factor' in info[dataKey]:
                        fct = info[dataKey]['Factor']
                    else:
                        fct = None
                    if not\
                        save_A_Data_GUI(dataDict[analysis][dataKey],
                                        info[dataKey]['Types'],
                                        (True,1), fileName,
                                        fct):
                        raise IndexError
                except IndexError:
                    print('Unable to save data\n%s\n%s'\
                            %(analysis,dataKey))
                self.AddDatasetToList(dataDict[analysis][dataKey],
                                      dataKey,info[dataKey]['Types'],
                                      fct)
            
#    def editSelectInterval(self):
#        groupDialog=CreateGroupsDlg(1,list(self.Dataset.keys()),DataContainer=self.Dataset,
#                                     Analysis=('Single','actogramPrint'),
#                                    TypeList=['Time Action Dataset','Switch Latency',
#                           'BART'],AnDict=self.AnalysisAndLabels,
#                                     parent=self)
#        if groupDialog.exec_():
#            comboBox=[('Keep time interval:', ['Inside','Outside'],
#                       ['Inside','Outside'], 0)]
#            timeSpinBox = [('Day Time 0:', 0, 0),('Day Time 1:', 24, 0),None]
#            Datalist=''
#            for ind in range(groupDialog.groupListWidget[0].count()):
#                item=groupDialog.groupListWidget[0].item(ind)
#                Datalist+=str(item.text())+'<br>'
#            Datalist=Datalist[:-4]
#            dialog = inputDialog(Datalist,comboBox,timeSpinBox,None,NewDataLineEdit=True,
#                                 DatasetNum=groupDialog.groupListWidget[0].count(),
#                                 parent=self)
#            if dialog.exec_():
#                
#                secStart = dialog.HourSpinBox[0].value()*3600+dialog.MinuteSpinbox[0].value()*60
#                secEnd = dialog.HourSpinBox[1].value()*3600+dialog.MinuteSpinbox[1].value()*60
#                InOrOut = str(dialog.ComboBox[0].itemText(dialog.ComboBox[0].currentIndex()))
#                NameInput=None
#                if len(str(dialog.NewDataLineEdit.text()))>0:
#                    NameInput=str(dialog.NewDataLineEdit.text()).split(';')
#                    try:
#                        while True:
#                            NameInput.remove('')
#                    except ValueError:
#                        pass
#                                    
#                if InOrOut=='Inside':
#                    InOrOut = 'In'
#                else:
#                    InOrOut = 'Out'
#                Item = groupDialog.groupListWidget[0].takeItem(0)
#                DataLabel=str(Item.text())
#                
#                while Item:
#                    try:
#                        Item=groupDialog.groupListWidget[0].takeItem(0)
#                        Dataset = self.Dataset.takeDataset(DataLabel)
#                        Types = self.Dataset.dataType(DataLabel)
#                        edited = False
#                        for typeName in Types:
#                            if 'EEG' in typeName:
#                                Dataset = self.editSelectInterval_EEG(Dataset, 
#                                                                      secStart,
#                                                                      secEnd,
#                                                                      InOrOut)
#                                edited = True
#                                break
#                        Scaled = self.Dataset.scaled(DataLabel)
#                        if not edited:
#                            
#                            Start_exp,Start_Time,End_Time =\
#                                Time_Details_GUI(Dataset,self.TimeStamps)
#                            Dataset = Select_Interval_GUI(Dataset,secStart,
#                                                          secEnd,self.TimeStamps,
#                                                          InOrOut=InOrOut)
#                    
#                        message = 'Selected interval from Dataset %s'%DataLabel
#                    
#                        if NameInput:
#                            self.currentDatasetLabel = NameInput[0]
#                            NameInput.pop(0)
#                            if '.'  not in self.currentDatasetLabel:
#                                self.currentDatasetLabel+='.csv'
#                        else:
#                            strings = DataLabel.split('.')
#                            self.currentDatasetLabel  = strings[0]+'_SelectedInterval.csv'
#                        self.flagData=True
#                        if self.currentDatasetLabel in self.Dataset:
#                            self.Dataset.pop(self.currentDatasetLabel)
#                            self.flagData=False
#                        data = Dataset_GUI(Dataset,self.currentDatasetLabel,
#                                           Path=None,Types=Types,Scaled=Scaled)
#                        self.Dataset.add(data)
#                        
#                        self.listWidgetRight.addItem(message)
#                        try:
#                            DataLabel=str(Item.text())
#                        except:
#                            pass
#                    except IndexError:
#                        message = 'Failed to cut Dataset %s'%DataLabel
#                        self.listWidgetRight.addItem(message)
                    
#    def editSelectInterval_EEG(self, Dataset, secStart, secEnd, InOrOut):
#        Dataset = copy(Dataset)
#        timeVect = Dataset.Timestamp
#        if secStart//3600 == 24:
#           start_time = dt.time(23, 59, 59)
#        else:
#            start_time = dt.time(secStart//3600, (secStart % 3600) // 60, 0)
#        if secEnd//3600 == 24:
#            end_time = dt.time(23, 59, 59)
#        else:
#            end_time = dt.time(secEnd//3600, (secEnd % 3600) // 60, 0)
#        index = 0
#        keep_index = []
#        if InOrOut == 'In':
#            for t in timeVect:
#                if t.time() >= start_time and t.time() <= end_time:
#                    keep_index += [index]
#                index += 1
#        else:
#            for t in timeVect:
#                if t.time() < start_time or t.time() > end_time:
#                    keep_index += [index]
#                index += 1
#        Dataset.PowerSp = Dataset.PowerSp[keep_index]
#        Dataset.Timestamp = Dataset.Timestamp[keep_index]
#        Dataset.Stage = Dataset.Stage[keep_index]
#        return Dataset
    
    
    def renameData(self):
        if self.analysisSingleThread.isRunning():
            self.analysisSingleThread.wait()
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

                
#    def RenameDataColumns(self):
#        if self.analysisSingleThread.isRunning():
#            self.analysisSingleThread.wait()
#        groupDialog=CreateGroupsDlg(1,list(self.Dataset.keys()),DataContainer=self.Dataset,
#                                    Analysis=('Single','actogramPrint'),SetIndex=8,
#                                     AnDict=self.AnalysisAndLabels,parent=self)
#        if groupDialog.exec_():
#            Datalist=''
#            LabelList=[]
#            for ind in range(groupDialog.groupListWidget[0].count()):
#                item=groupDialog.groupListWidget[0].item(ind)
#                Datalist+=str(item.text())+'<br>'
#                LabelList+=[str(item.text())]
#            Datalist=Datalist[:-4]
#            tuple_0=(self.Dataset.takeDataset(LabelList[0])).dtype.names
#            for label in LabelList[1:]:
#                if (self.Dataset.takeDataset(label)).dtype.names !=tuple_0:
#                    QMessageBox.warning(self,'Type Error', 'All Dataset must have the same column labels in the same order!')    
#                    return
#            lineEdit=[]
#            for col in tuple_0:
#                lineEdit+=['Previus column name: %s\nNew column name:\n\n'%col]
#            inputDlg=inputDialog(Datalist,None,None,None,lineEdit,[],parent=self)
#            listCols=[]
#            if inputDlg.exec_():
#                for k in list(inputDlg.LineEdit.keys()):
#                    col=str(inputDlg.LineEdit[k].text())
#                    if len(col):
#                        listCols+=[col]
#                    else:
#                        listCols+=[None]
#                
#                for label in LabelList:
#                    self.Dataset.renameColumns(label,listCols)
            
        
#    def extractingData(self):
#        groupDialog=CreateGroupsDlg(1,list(self.Dataset.keys()),DataContainer=self.Dataset,
#                                     Analysis=('Single','actogramPrint'),
#                                     AnDict=self.AnalysisAndLabels,
#                                    TypeList=['Time Action Dataset','Switch Latency',
#                                              'BART'],
#                                     parent=self)
#        if groupDialog.exec_():
#            Datalist=''
#            for ind in range(groupDialog.groupListWidget[0].count()):
#                item=groupDialog.groupListWidget[0].item(ind)
#                Datalist+=str(item.text())+'<br>'
#            Datalist=Datalist[:-4]
#            
#                  
#            On=list(self.TimeStamps.keys()).index('Center Light On')
#            Off=list(self.TimeStamps.keys()).index('Start Intertrial Interval')
#            Minuti=[]
#            for i in [5,10,15,20,30,60]:
#                Minuti+=['%d min'%i]
#            comboBox=[('Extract:',
#                       ['All Dataset','Inside Trial','Outside Trial'],
#                        ['All Dataset','Inside Trial','Outside Trial'],0),
#                      ('Trial Start:',list(self.TimeStamps.keys()),
#                       list(self.TimeStamps.keys()),On),
#                       ('Trial End:',list(self.TimeStamps.keys()),list(self.TimeStamps.keys())
#                       ,Off),('Time Interval:',Minuti,Minuti,5)]
#            doubleSpinBox = ([('Max Trial Duration:',(0,100000),30)]) 
#            spinBox = [('Dark start:',(0,23),20)]
#            inputdlg=inputDialog(Datalist,comboBox,None,doubleSpinBox,
#                                 NewDataLineEdit=True,SpinBox = spinBox,
#                                 ActivityList=list(self.TimeStamps.keys()),
#                                    DatasetNum=groupDialog.groupListWidget[0].count(),
#                                 parent=self)
#            if inputdlg.exec_():
#                NameInput=None
#                if len(str(inputdlg.NewDataLineEdit.text()))>0:
#                    NameInput=str(inputdlg.NewDataLineEdit.text()).split(';')
#                    try:
#                        while True:
#                            NameInput.remove('')
#                    except ValueError:
#                        pass
#                stdOutput = inputdlg.createStdOutput()
#                Index=stdOutput['Combo'][0]
#                if Index is 0:
#                    InOutAll='All'
#                elif Index is 1:
#                    InOutAll='In'
#                else:
#                    InOutAll='Out'
#                Actions=[]
#                item=inputdlg.activitySelectedWidget.takeItem(0)
#                while item:
#                    Actions.append(str(item.text()))
#                    item=inputdlg.activitySelectedWidget.takeItem(0)
#                TrialOn=str(stdOutput['Combo'][1])
#                TrialOff=str(stdOutput['Combo'][2])
#                TimeIntervalText=str(stdOutput['Combo'][3]).split(' ')
#                TimeInterval=int(TimeIntervalText[0])*60
#                
#                NumDailyTimePoint = 24 * (3600//TimeInterval)                
#                StartH = stdOutput['SpinBox'][0]
#                StartBin = StartH * (3600//TimeInterval)
#                
#                timeBinVec = np.arange(StartBin,StartBin + NumDailyTimePoint)%\
#                    (NumDailyTimePoint)
#                TimeVect =  TimeUnit_to_Hours_GUI(timeBinVec, TimeInterval)
#                
#                TimeToConsider = stdOutput['DoubleSpinBox'][0]
#                allDataItems=[]
#                item=groupDialog.groupListWidget[0].takeItem(0)
#                while item:
#                    allDataItems+=[item]
#                    item=groupDialog.groupListWidget[0].takeItem(0)
#                Index=0
#                subjectNum = len(allDataItems)
#                lung = 0
#                for dataitem in allDataItems:
#                    dataname=str(dataitem.text())
#                    lung = max(len(dataname),lung)
#                averageMatrix = np.zeros(subjectNum * len(TimeVect),
#                                         dtype = {'names':
#                                             ('Subject','Time',
#                                             'Mean','Median','SEM',),
#                                             'formats':
#                                             ('|S%d'%lung,'|S5',
#                                              float,float,float)})
#                for dataitem in allDataItems:
#                    dataname=str(dataitem.text())
#                    try:
#                    
#                        Extracted_Data=Extracting_Data_GUI(self.Dataset.takeDataset(dataname),self.TimeStamps,
#                                            Actions,TrialOn,TrialOff,InOutAll=InOutAll,
#                                            TimeToConsider=TimeToConsider,TimeInterval=TimeInterval)
#                        minBinUnit = Extracted_Data['Bins_Unit'][0]
#                        maxBinUnit = Extracted_Data['Bins_Unit'][-1]
#                        binVect = np.arange(minBinUnit,maxBinUnit + 1)
#                        binTot  = np.zeros(len(binVect), dtype = int)
#
#                        indBin = 0
#                        for hourBin in binVect:
#                            binTot[indBin] =  len(np.where(\
#                                Extracted_Data['Bins_Unit'] == hourBin)[0])
#                            indBin += 1
#                        Mean, Median, SEM = [],[],[]
#                        for hourBin in timeBinVec:
#                            binIndex = np.where(binVect %\
#                                NumDailyTimePoint == hourBin)[0]
#                            Mean += [sts.nanmean(binTot[binIndex])]
#                            SEM  += [sts.nanstd(binTot[binIndex])/\
#                                np.sqrt(len(binIndex))]
#                            Median += [sts.nanmedian(binTot[binIndex])]
#                        averageMatrix['Mean']\
#                            [Index * len(TimeVect) :\
#                            (Index + 1) * len(TimeVect)] = Mean 
#                        averageMatrix['SEM']\
#                            [Index * len(TimeVect) :\
#                            (Index + 1) * len(TimeVect)] = SEM
#                        averageMatrix['Median']\
#                            [Index * len(TimeVect) :\
#                            (Index + 1) * len(TimeVect)] = Median
#                        averageMatrix['Subject']\
#                            [Index * len(TimeVect) :\
#                            (Index + 1) * len(TimeVect)] = dataname
#                        averageMatrix['Time']\
#                            [Index * len(TimeVect) :\
#                            (Index + 1) * len(TimeVect)] = TimeVect
#                            
#                        data = Dataset_GUI(Extracted_Data,NameInput[Index],Types=['Extracted Time Stamps'])
#                        try:
#                            self.lock.lockForWrite()
#                            self.Dataset.add(data)
#                        finally:
#                            self.lock.unlock()
#                        self.listWidgetRight.addItem('Timestamps extracted from dataset\n%s'%dataname)
#                        Index+=1
#                    except NameError:
#                        
#                        self.listWidgetRight.addItem('Unable to extract timestamps from dataset\n%s'%dataname)
#                        Index+=1
#                NameInput = 'Daily_Activity.csv'
#                Types = ['Single Subject', 'Extracted Time Stamps']
#                data = Dataset_GUI(averageMatrix,NameInput,Types=Types)
#                try:
#                    self.lock.lockForWrite()
#                    self.Dataset.add(data)               
#                finally:
#                    self.lock.unlock()

                        
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
                if self.analysisSingleThread.isRunning():
                    self.analysisSingleThread.wait()
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
