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
        
*******************************************************************************
THIS IS AN ALTERNATIVE MAIN ANALYSIS IN WICH WE STARTED THE IMPLEMENTATION OF A
SPIKE ANALYSIS TOOLBOX

WHEN IT WILL BE FINISHED, THE FILEs SHOULD BE MOVEd IN THE APPEARED FOLDERS AND
THE PATH SHOULD BE CHANGED AS IN mainAnalysis.py
*******************************************************************************
          
"""
#==============================================================================
#  TODO: 
#  1- AGGIUNTA DELLA ANALISI EEG DA SELEZIONARE CON SILVIA E COMPLETAMENTO 
#  ANALISI DI GRUPPO
#  2- IMPLEMENTAZIONE ANALISI STATISTICHE E SALVATAGGIO DATI
#  3- IMPLEMENTAZIONE DELLE ANALISI STATISTICHE DA SINGLE SUBJECT
#  4- IMPLEMENTAZIONE METODO DI ESPORTAZIONE DATASET IN FORMATO CSV FACILMENTE
#  APRIBILE IN PYTHON, SELEZIONE DEL DELIMITER
#  5- IMPORTAZIONE DATASET CHE CONSENTA DI TRASFORMARE DATI IN FORMATO "PRISM"
#  IN DATI IN FORMATO OUTPUT ANALISI DI GRUPPO
#  6- ESTRAZIONE LATENCY E ALTRE INFO PIU' SMART
#==============================================================================

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys,os
import sip
try:
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
except ValueError, e:
    e.message
    print( e.message)

xx = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(xx,'mainScripts'))
file_dir = os.path.abspath(xx)
#file_dir = os.path.dirname(phenopy_dir)
import_directory = os.path.join(file_dir,'import')
image_dir = os.path.join(file_dir,'images')
sys.path.append(os.path.join(file_dir,'libraries'))
sys.path.append(os.path.join(file_dir,'dialogsAndWidget','analysisDlg'))
sys.path.append(os.path.join(file_dir,'classes','analysisClasses'))
sys.path.append(os.path.join(file_dir,'export'))
sys.path.append(os.path.join(file_dir,'future'))
sys.path.append(import_directory)

from future_builtins import *
import datetime as DT
import pandas as pd
from select_group_num_dlg import *
from get_folder_and_format_dlg_export import get_export_info_dlg
from export_files import *
from Analyzing_GUI import *
from Plotting_GUI import *
from Class_Analisi import Analysis_Single_GUI, Analysis_Group_GUI
from Modify_Dataset_GUI import *
from AnalysisSingle_Std import *
from AnalysisGroup_Std  import *
import platform
from editDatasetDlg import *
from Wizard_New_Analysis import new_Analysis_Wizard
from importDatasetDlg import *
from pairDataDlg import pairDataDlg
from spikeGUI import *

from datetime import datetime, timedelta
from PyQt4.QtCore import (QFile, QSettings,
          QTimer, Qt, SIGNAL,
        QReadWriteLock)
from PyQt4.QtGui import (QAction, QApplication,
        QDockWidget, QFileDialog, QFrame, QIcon, QImage
        , QInputDialog, QKeySequence, QLabel, QListWidget,QListWidgetItem,
        QMainWindow, QMessageBox, QPainter, QPixmap, QPrintDialog,
        QPrinter, QSpinBox, QMenu, QWidget, QVBoxLayout,QLineEdit,QAbstractItemView, QTabWidget)

#from Rescale_A_Datasetdlg import Rescale_A_Datasetdlg
from MergeDlg import MergeDlg
from datainfodlg import datainfodlg        
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar2
from protocol_save_files import load_npz,save_data_container
#from latencydlg import latencydlg
from AnalysisSingle_Std import analysisSingle_thread
from SearchDlg import SearchDlg
#from EditTimeStampsDlg import TimeStampsDlg
from Input_Dlg_std import inputDialog
from CreateGroupsDlg import CreateGroupsDlg
from ChangeRescalingFactordlg import ChangeRescalingFactordlg
from copy import copy
from plot_Launcher import select_Function_GUI
from plot_Launcher_Gr import select_Function_GUI_Gr
from analysis_data_type_class import refreshTypeList, getTypes


__version__ = "1.0.0"
def addDays(dateTime, daynum=0):
    return dateTime + timedelta(days=daynum)



class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
#       Recording Original TimeStamps:        
        self.TimeStamps={}
        self.TimeStampsKey=['Start Month','Start Day','Start Year','Start Hour',
                            'Start Minute','Start Second','End Month','End Day',
                            'End Year','House Light On','House Light Off',
                            'Left Light On','Left Light Off','Center Light On',
                            'Center Light Off','Right Light On','Right Light Off',
                            'Left NP In','Left NP Out','Center NP In',
                            'Center NP Out','Right NP In','Right NP Out',
                            'Give Pellet Left','Give Pellet Right',
                            'Start Intertrial Interval','End Intertrial Interval',
                            'Probe Trial','Add Nose Poke Exceded','Add Nose Poke Not Reached']
                            
        TimeStampsCode = [1,2,3,4,5,6,8,9,10,15,16,17,18,19,20,21,22,23,24,25,
                          26,27,28,29,30,36,33,35,37,38]
        refreshTypeList(import_directory)
#        self.AnalysisAndLabels = np.load(os.path.abspath('C:\\Users\\Ebalzani\Documents\\mypython_lib\\Analysis.npy')).all()
#        self.AnalysisAndLabels = np.load(os.path.join(os.path.dirname(__file__),'Analysis.npy')).all()
        self.AnalysisAndLabels = np.load(os.path.join(os.path.join(xx,'mainScripts'),'Analysis.npy')).all()

        self.AnalysisAndLabels['Single'] =\
            OrderedDict(self.AnalysisAndLabels['Single'])
        self.AnalysisAndLabels['Group'] =\
            OrderedDict(self.AnalysisAndLabels['Group'])
        print('HEY', self.AnalysisAndLabels['Single'].keys())
        ind=0
        for key in self.TimeStampsKey:
            self.TimeStamps[key] = TimeStampsCode[ind]  
            ind+=1
            
#       Keeping Track of original timestamps
        self.OriginalTimeStamps=self.TimeStamps.copy()
        self.OriginalTimeStampsKey=copy(self.TimeStampsKey)
        plt.ion()

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
#       dataset, if you press save when an input is the last selected you will save this
#       input, if a dataset is the last selected you will save this dataset
        self.InputOrData = None

#       Usual Time Scale in which the dataset are rescaled
        self.scale=1000

#       Image in the middle
        self.imageLabel = QLabel()
        self.imageLabel.setMinimumSize(200, 200)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        Logo=QImage(os.path.join(image_dir,u'autonomiceLogo.png'))
        self.imageLabel.setPixmap(QPixmap.fromImage(Logo))
        self.setCentralWidget(self.imageLabel)        
        
 
#       Dock widgets: 1 for the input, 1 for the dataset,1 for the log        
        logDockWidgetRight = QDockWidget("Log", self)
        logDockWidgetRight.setObjectName("LogDockWidgetRight")
        logDockWidgetRight.setAllowedAreas(
                                      Qt.RightDockWidgetArea)
        logDockWidgetRight.setMaximumWidth(300)
        self.listWidgetRight = QListWidget()
        logDockWidgetRight.setWidget(self.listWidgetRight)
        self.addDockWidget(Qt.RightDockWidgetArea, logDockWidgetRight)
        
        
        logDockWidgetLeft = QDockWidget("Loaded Datasets", self)
        logDockWidgetLeft.setObjectName("LoadedDockWidgetLeft")
        logDockWidgetLeft.setAllowedAreas(
                                      Qt.LeftDockWidgetArea)                                      
        logDockWidgetLeft.setMaximumWidth(300)
        self.listWidgetLeft = QListWidget()
        
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
                QKeySequence.Open, "fileopen",
                "Open an existing dataset")
        fileImportAction = self.createAction("&Import...", self.importExternalData,
                None, "fileImport",
                "Import an external dataset")
        self.fileExportAction = self.createAction("&Export...", self.exportData,
                None, "fileExport",
                "Import an external dataset")
        self.fileExportAction.setEnabled(False)
        
        self.fileSaveAsAction = self.createAction("Save &As...",
                self.fileSaveAs, icon="filesaveas",
                tip="Save the selected dataset")
        self.fileSaveAsAction.setEnabled(False)
        fileQuitAction = self.createAction("&Quit", self.close,
                "Ctrl+Q", "filequit", "Close the application")
                
        self.dataInfoAction = self.createAction("&Dataset Info",self.DataInfo,
                                           None,None,"Information about the dataset")
        
        self.imageLabel.addAction(fileQuitAction)
        
        
        self.analysisAction  = self.createAction('&Analyze Data',self.startAnalysis,
                                        'Ctrl+A', None,'Perform a single group analysis')
        startWizardAction = self.createAction('&Upload Analysis',self.startWizard,'Ctrl+U',
                                              None,'Upload a new function for data analysis.')
                                              
        self.spikeAction = self.createAction('&Spike Analysis',self.startSpikeAnalysis,None,
                                              'wave_spike','Upload a new function for data analysis.')
                                              
                                              
        self.extractingDataAction=self.createAction('Extract time stamps',self.extractingData,None,None,
                          'Extract timestamps from dataset')    
#        self.extractingLatencyAction=self.createAction('Extract latency',self.extractingLatency,None,None,
#                          'Extract latency between actions')                             
        clearLogAction = self.createAction('Clear Log',self.listWidgetRight.clear,None,'rubber','Clear Log')
                                        
        self.removeDatasetAction = self.createAction('Remove selected dataset',self.RemoveDataset,None,
                                                    None,'Remove Dataset')
        self.removeAllDatasetAction = self.createAction('Remove all',self.RemoveAllDataset,None,None,'Remove all')
        
        
        self.renameDatasetAction = self.createAction('Rename Dataset',self.renameData,'F2',None,'Rename selected dataset')
#        self.rescaleADatasetAction = self.createAction('Rescale Dataset',self.rescaleAData,None,None,'Rescale selected dataset')
        self.editSelectIntervalAction = self.createAction("Select &Interval",
                self.editSelectInterval, "Alt+I", None,
                "Keep only a selected time inteval",signal='triggered()')
        self.editFunctDlgAction = self.createAction('&Edit Dataset...',
                                                    self.startEditDlg,"CTRL+E",None)

    
#       Creating the Menu file, edit and analyzing, using the created action,
#       if an action is related to an icon, the icon will be displayed in the menu
        self.fileMenu = self.menuBar().addMenu("&File")
        
        fileMenuActions_Before = (fileOpenAction,fileImportAction,self.fileExportAction,
                 self.fileSaveAsAction)
        self.addActions(self.fileMenu,fileMenuActions_Before)
        
#        optionMenu = self.fileMenu.addMenu('Option') # how to insert additional menu inside a menu
                                    
        fileMenuActions_After = ( None,fileQuitAction)
        self.addActions(self.fileMenu,fileMenuActions_After)
        
        self.editMenu = self.menuBar().addMenu('&Edit')
        self.addActions(self.editMenu,(self.editFunctDlgAction,))
        analysisMenu=self.menuBar().addMenu("&Analysis")
        self.analysisAction.setEnabled(False)
        
        self.addActions(analysisMenu,(self.analysisAction,startWizardAction,self.spikeAction))
        
#       Creating a toolbar menu, as in the menus we use the action created that
#       are already associated with icon and connected
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, ( fileOpenAction,
                                      self.fileSaveAsAction))
                                      
        logToolbar = self.addToolBar("Log")
        logToolbar.setObjectName("LogToolBar")
        
        self.addActions(logToolbar,(clearLogAction,self.spikeAction))
                                      
        self.imageLabel.addAction(fileQuitAction)
        
        self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        self.addActions(self.listWidgetLeft,(self.fileSaveAsAction,
                                             self.renameDatasetAction,
                                             self.dataInfoAction,
#                                             self.rescaleADatasetAction,
                                             self.removeDatasetAction,
                                             self.removeAllDatasetAction))
        
        
        self.listWidgetLeft.setContextMenuPolicy(Qt.ActionsContextMenu)

#       Restoring previous settings like the geometry of the window, the movements
#       of the dock widgets, the last imported dataset, the time stamp list,
#       the last directory we used to open datasets

        fname=[]
        SingleAnalysis=[]
        GroupAnalysis=[]
        Types={}
        try:    
            settings = QSettings()
            settingsKeys = settings.childKeys()
    #        print('Settings keys type', settingsKeys, type(settingsKeys[0]))
    #       Restoring TimeStamps Code or Use the normal one
            if u'TimeStampsKey 0' in settingsKeys:
                
                self.TimeStampsKey = []
                self.TimeStamps={}
                KeyNum=0
                while u'TimeStampsKey %d'%KeyNum in settingsKeys:
                    self.TimeStampsKey = self.TimeStampsKey + [settings.value(u'TimeStampsKey %d'%KeyNum)]
                    self.TimeStamps[self.TimeStampsKey[-1]]=settings.value(u'TimeStampsCode %d'%KeyNum)
                    KeyNum+=1
                    
            
            self.restoreGeometry(
                    settings.value("MainWindow/Geometry"))
            self.restoreState(settings.value("MainWindow/State"))
            
            self.lastOpenFileDirectory = settings.value('LastOpenFileDirectory')
            if 'ScaleFactor' in settingsKeys:
                print('ScaleFactor',settings.value('ScaleFactor'))
                self.scale=settings.value('ScaleFactor')
            if not len(self.lastOpenFileDirectory):
                self.lastOpenFileDirectory=None
            
            
            for key in settingsKeys:
                key=unicode(key)
                first_word_key = key.split(' ')[0]
                
                if (key!=u'MainWindow/Geometry' and key!='MainWindow/State' 
                            and key!='LastOpenFileDirectory'
                            and first_word_key!='Group' and first_word_key!='Single'
                            and first_word_key!='Type'
                            and key!='ScaleFactor'
                            and not 'TimeStampsCode' in key
                            and not 'TimeStampsKey' in key
                            and not 'SaveDirectory' in key):
                    
                    fname = fname + [settings.value(key)]
                    print( 'RETRIVE SETTINGS',settings.value(key),key)
                    
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
        self.connect(self.analysisSingleThread,SIGNAL('threadFinished()'),\
                     lambda Type = 'Single': self.completedAnalysis(Type))
        self.connect(self.analysisGroupThread,SIGNAL('threadFinished()'),\
                     lambda Type = 'Group': self.completedAnalysis(Type))
#       connecting Dockwidget items to some methods        
        self.connect(self.listWidgetLeft,SIGNAL("itemClicked (QListWidgetItem *)"),self.UpdateCurrentDataset)
        self.connect(self.listWidgetLeft,SIGNAL('customContextMenuRequested(const QPoint&)'),self.on_context_menu)
        self.connect(self.listWidgetLeft,SIGNAL('itemSelectionChanged ()'),self.enable_disable_actions)
    
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
        dlg = importDlg(parent=self)
        dlg.errorImport.connect(self.listWidgetRight.addItem)
        dlg.show()
    
    def on_context_menu(self, point):
        self.listWidgetLeftMenu.exec_(self.listWidgetLeftMenu.mapToGlobal(point))  
        
    def loadInitialFile(self,fname):
        print('loadINITIAL',fname)
        answ = QMessageBox.question(self,'Load last dataset?', 'Do you want to load last session dataset?',QMessageBox.No|QMessageBox.Yes)
        if answ != 16384:
            fname = []
        existingFile=[]
        for name in fname:
            print(name)
            if name and QFile.exists(name) and name.endswith(('.csv','.phz','.txt')):
                existingFile += [name]
        if len(existingFile):
            self.loadFile(existingFile)

        
    def fileOpen(self):
        dire = (self.lastOpenFileDirectory
               if self.lastOpenFileDirectory is not None else ".")
        formats =([u'*.phz'])
        Qfnames=(QFileDialog.getOpenFileNames(self,
                    "Phenopy - Load Dataset", dire,
                    "Input files ({0})".format(" ".join(formats))))
        fnames = []  
        for ind in range(len(Qfnames)):
                fnames = fnames + [unicode(Qfnames[ind])]
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
        for item_name in self.Dataset.keys():
            print('I\'m Updating',item_name)
            item = QListWidgetItem(item_name)
            item.setIcon(QIcon(os.path.join(image_dir,"table.png")))
            self.listWidgetLeft.addItem(item)
        if len(self.Dataset.keys()) >= 1:
            self.analysisAction.setEnabled(True)
            self.editSelectIntervalAction.setEnabled(True)
        else:
            self.analysisAction.setEnabled(False)
            self.editSelectIntervalAction.setEnabled(False)

    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            if '.' in icon:
                action.setIcon(QIcon(os.path.join(image_dir,icon)))
            else:
                action.setIcon(QIcon(os.path.join(image_dir,"%s.png" % icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
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
        now = datetime.now()
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
        Dataname = unicode(Item.text())
        self.status.showMessage('Loading Dataset Info...',0)
        try:
            self.lock.lockForRead()
            dialog = datainfodlg(self.Dataset._DatasetContainer_GUI__Datas[Dataname],
                             Path=self.Dataset.path(Dataname),
                             TimeStamps=self.TimeStamps,lock=self.lock,parent=self)
            oldTypes=copy(self.Dataset.dataType(Dataname))
        finally:
            self.lock.unlock()
        self.status.clearMessage()
        dialog.exec_()
        try:
            self.lock.lockForRead()
            newTypes = self.Dataset.dataType(Dataname)
        finally:
            self.lock.unlock()
        if oldTypes != newTypes:
            self.listWidgetRight.addItem('Dataset %s types modified'%Dataname)
        

    def ConvertToEditTimeStampsFormat(self):
        List=[]
        for key in self.TimeStampsKey:
            List  = List + [(key,self.TimeStamps[key])]
        return List
        
        
        
    def updateLog(self,message):
        self.listWidgetRight.addItem(message)
        
    def UpdateCurrentDataset(self):
        self.currentDatasetLabel=unicode(self.listWidgetLeft.item(self.listWidgetLeft.currentRow()).text())
        self.InputOrData = True
        
    def UpdateCurrentInput(self):
        Row = self.listInputWidgetLeft.currentRow()
        self.currentInput['Analysis'] = unicode(self.listInputWidgetLeft.item(Row).text())
        self.currentInput['Input'] = self.Input[unicode(self.listInputWidgetLeft.item(Row).text())]
        self.listWidgetRight.addItem(u'Selected Input %s'%unicode(self.listInputWidgetLeft.item(Row).text()))
        self.InputOrData = False
        print(self.currentInput)
        
    def closeEvent(self, event):
        plt.close('all')
        settings = QSettings()
        settings.setValue("MainWindow/Geometry", self.saveGeometry())
        settings.setValue("MainWindow/State", self.saveState())
        settings.setValue('LastOpenFileDirectory',self.lastOpenFileDirectory)
        settings.setValue('ScaleFactor',self.scale)
        settingsKeys = settings.childKeys()
        for key in settingsKeys:
            if (unicode(key) !="MainWindow/Geometry" and unicode(key)!="MainWindow/State" 
                and unicode(key)!='LastOpenFileDirectory' and key!='ScaleFactor'):
                settings.remove(key)
        try:
            self.lock.lockForRead()
            list_fname = []
            for key in self.Dataset.keys():
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
            settings.setValue(u'TimeStampsKey %d'%KeyNum,TimeStampLabel)
            settings.setValue(u'TimeStampsCode %d'%KeyNum,TimeStampCode)
            KeyNum+=1
        
        for key in ['Single','Group']:
            KeyNum=0
            
            for analysis in self.AnalysisAndLabels[key].keys():
                Analysis = analysis
                settings.setValue(u'%s %d'%(key,KeyNum),Analysis)
                KeyNum += 1
        
        for analysis in self.AnalysisAndLabels.keys():
            KeyNum=0
            Types = self.AnalysisAndLabels[analysis]
            for Type in Types:
               AnType = Type
               settings.setValue(u'Type %s %d'%(analysis,KeyNum),AnType)

            
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
    
    def dataTypeList(self):
        """
            This function returns a dataTypeList of the imported data
        """
        type_list = []
        try:
            self.lock.lockForRead()
            for dataName, dataset in self.Dataset:
                this_type = self.Dataset.dataType(dataName)[0]
                if not this_type in type_list:
                    type_list +=  [this_type]
        finally:
            self.lock.unlock()
        return type_list
    
    def subSetDataPerType(self,type_list):
        """
            Select over a subset of data tipes and retunrs a list of data 
            names
        """
        data_list = []
        try:
            self.lock.lockForRead()
            for name, tmp in self.Dataset:
                if self.Dataset.dataType(name)[0] in type_list:
                    data_list += [name]
        finally:
            self.lock.unlock()
        return data_list
        
    def startSpikeAnalysis(self):
        
        if type(self.centralWidget()) is QTabWidget:
            tabWidget = self.centralWidget()
            for idx in range(tabWidget.count()):
                if type(tabWidget.widget(idx)) == spk_gui:
                    return
        else:
            tabWidget = QTabWidget() 
            
        dlg = spk_gui(self.Dataset,parent=self)
        
        tabWidget.addTab(dlg,'Spike Toolbox')
        self.setCentralWidget(tabWidget)
        func = lambda : self.removeTab(spk_gui)
        dlg.closeSpike.connect(func)
        
        
    def removeTab(self,tabName):
        
        tabWidget = self.centralWidget()
        for idx in range(tabWidget.count()):
            if type(tabWidget.widget(idx)) == tabName:
                tabWidget.removeTab(idx)
                break
        if tabWidget.count() == 0:
            Logo = QImage(os.path.join(image_dir,u'autonomiceLogo.png'))
            self.imageLabel = QLabel()
            self.imageLabel.setMinimumSize(200, 200)
            self.imageLabel.setAlignment(Qt.AlignCenter)
            self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
            self.imageLabel.setPixmap(QPixmap.fromImage(Logo))
            self.setCentralWidget(self.imageLabel)

    def startAnalysis(self):
        """
            SHOULD BE GENERAL FOR LAUNCHING ANY TYPE OF ANALYSIS
            Perform analysis single subject.
            Select Analysis --> Select Dataset --> Select Input --> Run thread
            The analysis is performed in a dedicated thread so that the 
            execution of the gui is not interrupted. This will be crucial
            when with the same software you'll be able to monitor cages
            status. While the thread is running no changes to the dataset
            must be done, for that reason the module for editing and saving
            will be unabled.
        """
        # self.AnalysisAndLabels contiene
        # key1: Single,Group or Integrative
        # key2: nome funzione analisi
        # value: tipo dato tipo "string"
        dialog = SearchDlg(self.AnalysisAndLabels,self.dataTypeList(),self)
        if not dialog.exec_():
            return
        anType = dialog.selectedType
        dataType = dialog.selectedDataTypes
        analysisName = dialog.selectedAnalysis
        if anType == 'Integrative':
            # Data select and pairing
            type_list = []
            for tl in dataType.values():
                type_list += tl
            paired_matrix = self.integrativeSpecificProcessing(analysisName)
            data_list = list(paired_matrix[paired_matrix.dtype.names[1]])
            if  paired_matrix is None:
                return
        else:
            type_list = dataType
            paired_matrix = None
            try:
                self.lock.lockForRead()
                data_list = self.subSetDataPerType(type_list)
            finally:
                self.lock.unlock()
        
        if anType in ['Group', 'Integrative']:
            dialog = select_group_num(parent=self)
            if not dialog.exec_():
                return
            num_group = dialog.spinBox.value()
            analysisCreator = Analysis_Group_GUI
            analysisThread = self.analysisGroupThread
            
        else:
            num_group = 1
            analysisCreator = Analysis_Single_GUI
            analysisThread = self.analysisSingleThread
            
        dialog = CreateGroupsDlg(num_group, data_list,
                                 DataContainer=self.Dataset,
                                 parent=self)
        if not dialog.exec_():
            return
        # da qui in poi da scrivere i select groups in caso di gruppo/integrative
        # numero gruppi = 1 in caso di single 
        # pairing in caso di integrative
        # continuo con gli input come al solito
        selectedDataDict = dialog.returnSelectedNames()
        
        pairedGroups = self.groupDictPerPaired(paired_matrix,selectedDataDict)
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
        self.status.showMessage('%s analysis is running...'%analysisName)
        
    def groupDictPerPaired(self,paired_matrix, selectedDataDict):
        if paired_matrix is None:
            groupDict = None
        else:
            groupDict = {}
            grouped = paired_matrix.dtype.names[1]
            for group in selectedDataDict.keys():
                groupDict[group] = {}
                for mat_type in paired_matrix.dtype.names[1:]:
                    groupDict[group][mat_type] = []
                for subject in selectedDataDict[group]:
                    findRow = np.where(paired_matrix[grouped] == subject)[0][0]
                    for mat_type in paired_matrix.dtype.names[1:]:
                        groupDict[group][mat_type] += [paired_matrix[mat_type][findRow]]
        return groupDict
                
        
    def integrativeSpecificProcessing(self,analysisName):
        dialog = pairDataDlg(self.AnalysisAndLabels['Integrative'][analysisName], self.Dataset,
                             self.lock)
        paired_matrix = None
        if dialog.exec_():
            paired_matrix = dialog.pairMatrix
        return paired_matrix
            
    def inputDlgLauncher(self,inputCreator, selectedDataDict):
        Input = {}
        print('inputDlg called')
        phaseSel = None
        if not inputCreator.returnInput(0,'PhaseSel') is None:
            phaseSel = [self.Dataset, np.hstack(selectedDataDict.values())]
            
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
            if Input[dialogNum].has_key('DoubleSpinBox'):
                print(Input[dialogNum]['DoubleSpinBox'])
        return Input

    def disableActionDuringAnalysis(self,Type):
        self.analysisAction.setEnabled(False)
        self.renameDatasetAction.setEnabled(False)
#        self.rescaleADatasetAction.setEnabled(False)
        self.removeAllDatasetAction.setEnabled(False)
        self.removeDatasetAction.setEnabled(False)
        
    def enableActionAfterAnalysis(self,Type):
        
        self.analysisAction.setEnabled(True)
        self.renameDatasetAction.setEnabled(True)
#        self.rescaleADatasetAction.setEnabled(True)
        self.removeAllDatasetAction.setEnabled(True)
        self.removeDatasetAction.setEnabled(True)

    def completedAnalysis(self, Type):
        print('completedAnalysis')
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
        plt.close('all')
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
        for analysis in figDict.keys():
            DirFig = os.path.join(Dir,analysis)
            if not os.path.exists(DirFig):
                os.mkdir(DirFig)
            for figKey in figDict[analysis].keys():
                fig = figDict[analysis][figKey]
                print('saving ',analysis,figKey)
                try:
                    plt.show(block=False)
                    fileName = os.path.join(DirFig, figKey + ext)
                    fig.savefig(fileName)
                except IndexError:
                    print('Unable to save figure%s\n%s'\
                        %(analysis,figKey))
        for analysis in dataDict.keys():
            DirData = os.path.join(Dir,analysis)
            if not os.path.exists(DirData):
                os.mkdir(DirData)
            for dataKey in dataDict[analysis].keys():
                fileName = os.path.join(DirData,dataKey + '.csv')
#==============================================================================
#   MODIFICARE LA PROCEDURA DI SALVATAGGIO DATI c Generalizzare il piu' possibile!!!
#==============================================================================
                try:
                    if info[dataKey].has_key('Factor'):
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
            
    def editSelectInterval(self):
        groupDialog=CreateGroupsDlg(1,self.Dataset.keys(),DataContainer=self.Dataset,
                                     Analysis=('Single','actogramPrint'),
                                    TypeList=['Time Action Dataset','Switch Latency',
                           'BART'],AnDict=self.AnalysisAndLabels,
                                     parent=self)
        if groupDialog.exec_():
            comboBox=[(u'Keep time interval:', ['Inside','Outside'],
                       ['Inside','Outside'], 0)]
            timeSpinBox = [('Day Time 0:', 0, 0),('Day Time 1:', 24, 0),None]
            Datalist=u''
            for ind in range(groupDialog.groupListWidget[0].count()):
                item=groupDialog.groupListWidget[0].item(ind)
                Datalist+=unicode(item.text())+u'<br>'
            Datalist=Datalist[:-4]
            dialog = inputDialog(Datalist,comboBox,timeSpinBox,None,NewDataLineEdit=True,
                                 DatasetNum=groupDialog.groupListWidget[0].count(),
                                 parent=self)
            if dialog.exec_():
                
                secStart = dialog.HourSpinBox[0].value()*3600+dialog.MinuteSpinbox[0].value()*60
                secEnd = dialog.HourSpinBox[1].value()*3600+dialog.MinuteSpinbox[1].value()*60
                InOrOut = unicode(dialog.ComboBox[0].itemText(dialog.ComboBox[0].currentIndex()))
                NameInput=None
                if len(unicode(dialog.NewDataLineEdit.text()))>0:
                    NameInput=unicode(dialog.NewDataLineEdit.text()).split(';')
                    try:
                        while True:
                            NameInput.remove('')
                    except ValueError:
                        pass
                                    
                if InOrOut==u'Inside':
                    InOrOut = 'In'
                else:
                    InOrOut = 'Out'
                Item = groupDialog.groupListWidget[0].takeItem(0)
                DataLabel=unicode(Item.text())
                
                while Item:
                    try:
                        Item=groupDialog.groupListWidget[0].takeItem(0)
                        Dataset = self.Dataset.takeDataset(DataLabel)
                        Types = self.Dataset.dataType(DataLabel)
                        edited = False
                        for typeName in Types:
                            if 'EEG' in typeName:
                                Dataset = self.editSelectInterval_EEG(Dataset, 
                                                                      secStart,
                                                                      secEnd,
                                                                      InOrOut)
                                edited = True
                                break
                        Scaled = self.Dataset.scaled(DataLabel)
                        if not edited:
                            
                            Start_exp,Start_Time,End_Time =\
                                Time_Details_GUI(Dataset,self.TimeStamps)
                            Dataset = Select_Interval_GUI(Dataset,secStart,
                                                          secEnd,self.TimeStamps,
                                                          InOrOut=InOrOut)
                    
                        message = 'Selected interval from Dataset %s'%DataLabel
                    
                        if NameInput:
                            self.currentDatasetLabel = NameInput[0]
                            NameInput.pop(0)
                            if '.'  not in self.currentDatasetLabel:
                                self.currentDatasetLabel+='.csv'
                        else:
                            strings = DataLabel.split('.')
                            self.currentDatasetLabel  = strings[0]+u'_SelectedInterval.csv'
                        self.flagData=True
                        if self.Dataset.has_key(self.currentDatasetLabel):
                            self.Dataset.pop(self.currentDatasetLabel)
                            self.flagData=False
                        data = Dataset_GUI(Dataset,self.currentDatasetLabel,
                                           Path=None,Types=Types,Scaled=Scaled)
                        self.Dataset.add(data)
                        
                        self.listWidgetRight.addItem(message)
                        try:
                            DataLabel=unicode(Item.text())
                        except:
                            pass
                    except IndexError:
                        message = 'Failed to cut Dataset %s'%DataLabel
                        self.listWidgetRight.addItem(message)
                    
    def editSelectInterval_EEG(self, Dataset, secStart, secEnd, InOrOut):
        Dataset = copy(Dataset)
        timeVect = Dataset.Timestamp
        if secStart//3600 == 24:
           start_time = DT.time(23, 59, 59)
        else:
            start_time = DT.time(secStart//3600, (secStart % 3600) // 60, 0)
        if secEnd//3600 == 24:
            end_time = DT.time(23, 59, 59)
        else:
            end_time = DT.time(secEnd//3600, (secEnd % 3600) // 60, 0)
        index = 0
        keep_index = []
        if InOrOut == 'In':
            for t in timeVect:
                if t.time() >= start_time and t.time() <= end_time:
                    keep_index += [index]
                index += 1
        else:
            for t in timeVect:
                if t.time() < start_time or t.time() > end_time:
                    keep_index += [index]
                index += 1
        Dataset.PowerSp = Dataset.PowerSp[keep_index]
        Dataset.Timestamp = Dataset.Timestamp[keep_index]
        Dataset.Stage = Dataset.Stage[keep_index]
        return Dataset
    
    
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
                self.Dataset.changeKey(self.currentDatasetLabel,unicode(string))                
                self.listWidgetRight.addItem('Dataset %s\nrenamed to %s'%(self.currentDatasetLabel,unicode(string)))
                self.currentDatasetLabel = unicode(string)

                
    def RenameDataColumns(self):
        if self.analysisSingleThread.isRunning():
            self.analysisSingleThread.wait()
        groupDialog=CreateGroupsDlg(1,self.Dataset.keys(),DataContainer=self.Dataset,
                                    Analysis=('Single','actogramPrint'),SetIndex=8,
                                     AnDict=self.AnalysisAndLabels,parent=self)
        if groupDialog.exec_():
            Datalist=u''
            LabelList=[]
            for ind in range(groupDialog.groupListWidget[0].count()):
                item=groupDialog.groupListWidget[0].item(ind)
                Datalist+=unicode(item.text())+u'<br>'
                LabelList+=[unicode(item.text())]
            Datalist=Datalist[:-4]
            tuple_0=(self.Dataset.takeDataset(LabelList[0])).dtype.names
            for label in LabelList[1:]:
                if (self.Dataset.takeDataset(label)).dtype.names !=tuple_0:
                    QMessageBox.warning(self,u'Type Error', u'All Dataset must have the same column labels in the same order!')    
                    return
            lineEdit=[]
            for col in tuple_0:
                lineEdit+=['Previus column name: %s\nNew column name:\n\n'%col]
            inputDlg=inputDialog(Datalist,None,None,None,lineEdit,[],parent=self)
            listCols=[]
            if inputDlg.exec_():
                for k in inputDlg.LineEdit.keys():
                    col=str(inputDlg.LineEdit[k].text())
                    if len(col):
                        listCols+=[col]
                    else:
                        listCols+=[None]
                
                for label in LabelList:
                    self.Dataset.renameColumns(label,listCols)
            
        
    def extractingData(self):
        groupDialog=CreateGroupsDlg(1,self.Dataset.keys(),DataContainer=self.Dataset,
                                     Analysis=('Single','actogramPrint'),
                                     AnDict=self.AnalysisAndLabels,
                                    TypeList=['Time Action Dataset','Switch Latency',
                                              'BART'],
                                     parent=self)
        if groupDialog.exec_():
            Datalist=u''
            for ind in range(groupDialog.groupListWidget[0].count()):
                item=groupDialog.groupListWidget[0].item(ind)
                Datalist+=unicode(item.text())+u'<br>'
            Datalist=Datalist[:-4]
            
                  
            On=self.TimeStamps.keys().index('Center Light On')
            Off=self.TimeStamps.keys().index('Start Intertrial Interval')
            Minuti=[]
            for i in [5,10,15,20,30,60]:
                Minuti+=['%d min'%i]
            comboBox=[(u'Extract:',
                       ['All Dataset','Inside Trial','Outside Trial'],
                        ['All Dataset','Inside Trial','Outside Trial'],0),
                      (u'Trial Start:',self.TimeStamps.keys(),
                       self.TimeStamps.keys(),On),
                       (u'Trial End:',self.TimeStamps.keys(),self.TimeStamps.keys()
                       ,Off),('Time Interval:',Minuti,Minuti,5)]
            doubleSpinBox = ([(u'Max Trial Duration:',(0,100000),30)]) 
            spinBox = [('Dark start:',(0,23),20)]
            inputdlg=inputDialog(Datalist,comboBox,None,doubleSpinBox,
                                 NewDataLineEdit=True,SpinBox = spinBox,
                                 ActivityList=self.TimeStamps.keys(),
                                    DatasetNum=groupDialog.groupListWidget[0].count(),
                                 parent=self)
            if inputdlg.exec_():
                NameInput=None
                if len(unicode(inputdlg.NewDataLineEdit.text()))>0:
                    NameInput=unicode(inputdlg.NewDataLineEdit.text()).split(';')
                    try:
                        while True:
                            NameInput.remove('')
                    except ValueError:
                        pass
                stdOutput = inputdlg.createStdOutput()
                Index=stdOutput['Combo'][0]
                if Index is 0:
                    InOutAll='All'
                elif Index is 1:
                    InOutAll='In'
                else:
                    InOutAll='Out'
                Actions=[]
                item=inputdlg.activitySelectedWidget.takeItem(0)
                while item:
                    Actions.append(unicode(item.text()))
                    item=inputdlg.activitySelectedWidget.takeItem(0)
                TrialOn=unicode(stdOutput['Combo'][1])
                TrialOff=unicode(stdOutput['Combo'][2])
                TimeIntervalText=unicode(stdOutput['Combo'][3]).split(' ')
                TimeInterval=int(TimeIntervalText[0])*60
                
                NumDailyTimePoint = 24 * (3600//TimeInterval)                
                StartH = stdOutput['SpinBox'][0]
                StartBin = StartH * (3600//TimeInterval)
                
                timeBinVec = np.arange(StartBin,StartBin + NumDailyTimePoint)%\
                    (NumDailyTimePoint)
                TimeVect =  TimeUnit_to_Hours_GUI(timeBinVec, TimeInterval)
                
                TimeToConsider = stdOutput['DoubleSpinBox'][0]
                allDataItems=[]
                item=groupDialog.groupListWidget[0].takeItem(0)
                while item:
                    allDataItems+=[item]
                    item=groupDialog.groupListWidget[0].takeItem(0)
                Index=0
                subjectNum = len(allDataItems)
                lung = 0
                for dataitem in allDataItems:
                    dataname=unicode(dataitem.text())
                    lung = max(len(dataname),lung)
                averageMatrix = np.zeros(subjectNum * len(TimeVect),
                                         dtype = {'names':
                                             ('Subject','Time',
                                             'Mean','Median','SEM',),
                                             'formats':
                                             ('|S%d'%lung,'|S5',
                                              float,float,float)})
                for dataitem in allDataItems:
                    dataname=unicode(dataitem.text())
                    try:
                    
                        Extracted_Data=Extracting_Data_GUI(self.Dataset.takeDataset(dataname),self.TimeStamps,
                                            Actions,TrialOn,TrialOff,InOutAll=InOutAll,
                                            TimeToConsider=TimeToConsider,TimeInterval=TimeInterval)
                        minBinUnit = Extracted_Data['Bins_Unit'][0]
                        maxBinUnit = Extracted_Data['Bins_Unit'][-1]
                        binVect = np.arange(minBinUnit,maxBinUnit + 1)
                        binTot  = np.zeros(len(binVect), dtype = int)

                        indBin = 0
                        for hourBin in binVect:
                            binTot[indBin] =  len(np.where(\
                                Extracted_Data['Bins_Unit'] == hourBin)[0])
                            indBin += 1
                        Mean, Median, SEM = [],[],[]
                        for hourBin in timeBinVec:
                            binIndex = np.where(binVect %\
                                NumDailyTimePoint == hourBin)[0]
                            Mean += [sts.nanmean(binTot[binIndex])]
                            SEM  += [sts.nanstd(binTot[binIndex])/\
                                np.sqrt(len(binIndex))]
                            Median += [sts.nanmedian(binTot[binIndex])]
                        averageMatrix['Mean']\
                            [Index * len(TimeVect) :\
                            (Index + 1) * len(TimeVect)] = Mean 
                        averageMatrix['SEM']\
                            [Index * len(TimeVect) :\
                            (Index + 1) * len(TimeVect)] = SEM
                        averageMatrix['Median']\
                            [Index * len(TimeVect) :\
                            (Index + 1) * len(TimeVect)] = Median
                        averageMatrix['Subject']\
                            [Index * len(TimeVect) :\
                            (Index + 1) * len(TimeVect)] = dataname
                        averageMatrix['Time']\
                            [Index * len(TimeVect) :\
                            (Index + 1) * len(TimeVect)] = TimeVect
                            
                        data = Dataset_GUI(Extracted_Data,NameInput[Index],Types=['Extracted Time Stamps'])
                        try:
                            self.lock.lockForWrite()
                            self.Dataset.add(data)
                        finally:
                            self.lock.unlock()
                        self.listWidgetRight.addItem('Timestamps extracted from dataset\n%s'%dataname)
                        Index+=1
                    except NameError:
                        
                        self.listWidgetRight.addItem('Unable to extract timestamps from dataset\n%s'%dataname)
                        Index+=1
                NameInput = 'Daily_Activity.csv'
                Types = ['Single Subject', 'Extracted Time Stamps']
                data = Dataset_GUI(averageMatrix,NameInput,Types=Types)
                try:
                    self.lock.lockForWrite()
                    self.Dataset.add(data)               
                finally:
                    self.lock.unlock()
                
                        
#    def extractingLatency(self):
#        groupDialog=CreateGroupsDlg(1,self.Dataset.keys(),DataContainer=self.Dataset,
#                                     Analysis=('Single','actogramPrint'),
#                                    TypeList=['Time Action Dataset','Switch Latency',
#                           'BART'],AnDict=self.AnalysisAndLabels,
#                                     parent=self)
#        if groupDialog.exec_():
#            Datalist=u''
#            for ind in range(groupDialog.groupListWidget[0].count()):
#                item=groupDialog.groupListWidget[0].item(ind)
#                Datalist+=unicode(item.text())+u'<br>'
#            Datalist=Datalist[:-4]
#            print(self.TimeStamps.keys())
#                  
#            inputdlg=latencydlg(Datalist,DatasetNum=groupDialog.groupListWidget[0].count(),
#                                ActivityList=self.TimeStamps.keys(),parent=self)
#            if inputdlg.exec_():
#                pass
#                NameInput=None
#                if len(unicode(inputdlg.NewDataLineEdit.text()))>0:
#                    NameInput=unicode(inputdlg.NewDataLineEdit.text()).split(';')
#                    try:
#                        while True:
#                            NameInput.remove('')
#                    except ValueError:
#                        pass
#                Index=inputdlg.InOutAllCombo.currentIndex()
#                if Index is 0:
#                    InOutAll='All'
#                elif Index is 1:
#                    InOutAll='In'
#                else:
#                    InOutAll='Out'
#                ActionA=unicode(inputdlg.listActionA.item(0).text())
#                ActionB=unicode(inputdlg.listActionB.item(0).text())
#
#                TrialOn=unicode(inputdlg.timeStampsComboBox0.itemText(inputdlg.timeStampsComboBox0.currentIndex()))
#                TrialOff=unicode(inputdlg.timeStampsComboBox1.itemText(inputdlg.timeStampsComboBox1.currentIndex()))
#                TimeToConsider = inputdlg.doubleSpinBox.value()
#                TimeIntervalText=unicode(inputdlg.timeIntervalComboBox.currentText()).split(' ')[0]
#                TimeInterval=int(TimeIntervalText)*60
#                allDataItems=[]
#                item=groupDialog.groupListWidget[0].takeItem(0)
#                while item:
#                    allDataItems+=[item]
#                    item=groupDialog.groupListWidget[0].takeItem(0)
#                Index=0
#                for dataitem in allDataItems:
#                    dataname=unicode(dataitem.text())
#                    try:
#                    
#                        Extracted_Data=Extracting_Latencies_GUI(self.Dataset.takeDataset(dataname),self.TimeStamps,
#                                            ActionA,ActionB,TrialOn,TrialOff,InOutAll=InOutAll,TimeInterval=TimeInterval,
#                                            TimeToConsider=TimeToConsider)
#                        
#                        if self.Dataset.has_key(NameInput[Index]):
#                            self.Dataset.pop(NameInput[Index])
#                            self.flagData=False
#                        Items = self.listWidgetLeft.findItems(NameInput[Index],Qt.MatchExactly)
#                        for item in Items:
#                            self.listWidgetLeft.takeItem(self.listWidgetLeft.row(item))
#                        data = Dataset_GUI(Extracted_Data,NameInput[Index],Types=['Extracted Latency'])
#                        
#                        self.Dataset.add(data)
#                        Item=QListWidgetItem()
#                        Item.setText(NameInput[Index])
#                        Item.setIcon(QIcon(os.path.join(phenopy_dir,"table.png")))
#                        self.listWidgetLeft.addItem(Item)
#                        self.listWidgetRight.addItem('Latencies extracted from dataset\n%s'%dataname)
#                        Index+=1 
#                    except:
#                        
#                        self.listWidgetRight.addItem('Unable to extract latencies from dataset\n%s'%dataname)
#                        Index+=1

                        
    def AddDatasetToList(self,Extracted_Data,Name,Types,FactorColumns=None):
        print('ADD DATASET TO LIST')
        try:
            self.lock.lockForRead()
            boolean = self.Dataset.has_key(Name)
        finally:
            self.lock.unlock()
        if boolean:
            reply=QMessageBox.question(self,u'Name Conflict',\
                u'Do you want to replace data %s?'\
                %Name,QMessageBox.No|QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                if self.analysisSingleThread.isRunning():
                    self.analysisSingleThread.wait()
                self.Dataset.pop(Name)
                self.flagData=False
                self.listWidgetRight.addItem(u'Replaced dataset %s'%Name)
                
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
    app.setApplicationName("Autonomice GUI")
    app.setWindowIcon(QIcon(os.path.join(image_dir,"logo.ico")))
    form = MainWindow()
    form.show()
    app.exec_()
    print(form.Dataset.keys(),'\n',form.currentInput,form.currentDatasetLabel)

if __name__ == '__main__':
    main()
