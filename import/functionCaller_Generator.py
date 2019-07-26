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

import os

def cancel_comments_and_empty_lines(list_lines):
    new_list = []
    for line in list_lines:
        stripline = line.lstrip()
        if stripline.startswith('#') or len(stripline) is 0:
            continue
        new_list += [(len(line)-len(stripline),line)]
    return new_list

def functionCaller_Generator(pythonFilePath,newName,Dir,analysisType):
    fh = open(pythonFilePath,'U')
    funcNameList = []
    if not newName.endswith('.py'):
        newName = newName.split('.')[0] + '.py'
    
    if not os.path.exists(Dir):
        raise ValueError('Directory %s not found'%Dir)
        
    list_lines = cancel_comments_and_empty_lines(fh.readlines())
    for indent, line in list_lines:
        word  = line.split()
        try:
            index = word.index('def')
        except ValueError:
            continue
        for item in word[index+1:]:
            if item == '':
                continue
            funcNameList += [item.split('(')[0]]
            break
    fh.close()
    fh = open(os.path.join(Dir, newName),'w')
    

    
    program = 'from analysis_functions import *\n\n'
    program += 'def function_Launcher(name,*myInput):\n'
    
    for name in funcNameList:
        if name == funcNameList[0]:
            program += '    if name == \'%s\':\n'%name
        else:
            program += '    elif name == \'%s\':\n'%name
            
        program += '        outputData, inputForPlots, info = %s(*myInput)\n'%name
        program += '        return outputData, inputForPlots, info\n'
    fh.write(program)
    fh.close()
    return

def add_To_Custom_Analysis(PathToAutonomice,PathToPythonFun,AddTo = 'analysis_functions.py'):
    fh = open(PathToPythonFun,'U')
    ProgString = ''
    StartCopy = False
    list_lines = cancel_comments_and_empty_lines(fh.readlines())
    
    for indent, line in list_lines:
        splitLine = line.split()
        if splitLine[0] == 'def' and not StartCopy:
            functionName = splitLine[1].split('(')[0]
            StartCopy = True
        elif indent is 0 and StartCopy is True:
            break
        if StartCopy:
            ProgString += line
    fh.close()
    
    if not ProgString.endswith('\n'):
        ProgString += '\n'
    ProgString = '\n' + ProgString
    
    if os.path.exists(os.path.join(PathToAutonomice, AddTo)):
        fh = open(os.path.join(PathToAutonomice, AddTo),'a')
    else:
        raise ValueError('Invalid path: \"%s\"'%(PathToAutonomice + AddTo))
        
    fh.write(ProgString)
    fh.close()
    return functionName
    
def remove_A_Funct(PathToPythonFile,FuncName):
    fh = open(PathToPythonFile,'U')
    ProgString = ''
    InFunction  = False
    for line in fh.readlines():
        if line == '\n':
            continue     
        if line.startswith(('def ','def\t')):
            FNAME = line[3:].lstrip()
            FNAME = FNAME.split('(')[0].rstrip()
            
            if not FNAME == FuncName:
                ProgString += line
                InFunction = False
                continue
            else:
                InFunction = True
                continue
        
        if not InFunction:
            ProgString += line
            continue
        
        stripLine = line.lstrip()
        if stripLine.startswith(('def ','def\t')):
            InFunction = False
            continue
    fh.close()
    fh = open(PathToPythonFile,'w')
    fh.write(ProgString)
    

def remove_An_If_Close(PathToPythonFile,FuncName,IfCond):
    fh = open(PathToPythonFile,'U')
    ProgString  = ''
    InFunction  = False
    InIf        = False
    for line in fh.readlines():
        if line == '\n':
            continue
        
        if line.startswith('def'):
            FNAME = line[3:].lstrip()
            FNAME = FNAME.split('(')[0].rstrip()
            
            if not FNAME == FuncName:
                ProgString += line
                InFunction = False
                continue
            else:
                InFunction = True
                ProgString += line
                continue
        if not InFunction:
            ProgString += line
            continue
        
        stripLine = line.lstrip()
        if stripLine.startswith('if'):
            IFCOND = stripLine[2:].lstrip()
            IFCOND = IFCOND.split(':')[0].rstrip()
            IFCOND = IFCOND.split(' ')[-1].split('\t')[-1]
            if IfCond in IFCOND:
                InIf = True
                continue
            
        elif stripLine.startswith('elif'):
            IFCOND = stripLine[4:].lstrip()
            IFCOND = IFCOND.split(':')[0].rstrip()
            IFCOND = IFCOND.split(' ')[-1].split('\t')[-1]
            if IfCond in IFCOND:
                InIf = True
                continue
            
        if not InIf:
            ProgString += line
            continue
        
        if stripLine.startswith(('return ','return\t')):
            InIf = False
                       
    fh.close()
    fh = open(PathToPythonFile,'w')
    fh.write(ProgString)
    fh.close()
    

def add_To_Plot_Launcher(PathToAutonomice,funName,ifCond,
                         AddTo = 'plot_Launcher.py'):
    """
        ifCond e' il nome dell'analisi
        funName e' il nome della funzione di plotting da lanciare
    """
    String =  '\n    elif funcName == \'%s\':\n'%ifCond
    String += '        fig = %s(*otherInputs)\n'%funName
    String += '        return fig\n'
    try:
        fh = open(os.path.join(PathToAutonomice, AddTo),'a')
    except:
        print('Unable to open \"%s\"'%(os.path.join(PathToAutonomice, AddTo)))
    fh.write(String)
    fh.close()
    
def get_Function_List(PathToPythonFile):
    """
        Function Mehtod:
        ================
            This function return all the names of python functions contained
            in a file specified by *PathToPythonFile*
        Input:
        ------
            - *PathToPythonFile*: string, path to a *.py* script
        Output:
        -------
            - *functionList*: list, list of all function names
    """
    if not (PathToPythonFile.endswith('.py') or
            PathToPythonFile.endswith('.pyw')):
        raise ValueError('Must inser a path to a python file')
    fh = open(PathToPythonFile,'U')
    functionList = []
    for line in fh.readlines():
        
        if line.startswith('def'):
            splitLine = line.split('def')[1].lstrip()
            functionList += [splitLine.split('(')[0].rstrip()]
    fh.close()
    return functionList
    
def getPlotFunctName(PathToPltLauncher,anFunName):
    fh = open(PathToPltLauncher,'U')
    inFunct = False
    inIfClose = False
    for line in fh.readlines():
        if line.startswith(('def ','def\t')):
            FNAME = line[3:].lstrip().split('(')[0].rstrip()
            if FNAME in ['select_Function_GUI']:
                inFunct = True
                continue
            else:
                inFunct = False
                continue
        if not inFunct:
            continue
        stripLine = line.lstrip()
        if stripLine.startswith(('elif','if')):
            ANNAME = stripLine.split()[3].rstrip(':').rstrip('\'').lstrip('\'').rstrip('\"').lstrip('\"')
            if ANNAME == anFunName:
                inIfClose = True
                continue
            else:
                inIfClose = False
                continue
        if inIfClose and '(' in stripLine:
            return stripLine.split('=')[1].lstrip().split('(')[0].rstrip()
        
            

def remove_Functions(PathToAutonomice,functionList,analysis_dict):
    path_to_launcher = os.path.join(os.path.dirname(PathToAutonomice),'classes','analysisClasses')
    PathToCustomAnalysis = os.path.join(PathToAutonomice, 'analysis_functions.py')
    PathToCustomPlots    = os.path.join(PathToAutonomice, 'custom_Plots.py')
    PathToLauncher       = os.path.join(path_to_launcher, 'launcher_all.py')
    PathToPltLauncher    = os.path.join(path_to_launcher, 'plot_Launcher_all.py')
    PathToInputCreator   = os.path.join(path_to_launcher, 'inputDlgCreator.py')
    
    for func in functionList:
        an_func = analysis_dict[func]['analysis_function']
        plt_func = analysis_dict[func]['plot_function']
        remove_A_Funct(PathToCustomAnalysis, an_func)
        remove_A_Funct(PathToCustomPlots, plt_func)
        remove_An_If_Close(PathToLauncher,'function_Launcher',an_func)
        remove_An_If_Close(PathToInputCreator,'inputDlgCreator',an_func)
        remove_An_If_Close(PathToPltLauncher,'select_Function_GUI',an_func)
    print('Functions Removed')
    return

if __name__ == '__main__':
#    anFunName = 'Sleep_Time_Course'
#    print getPlotFunctName(PathToPltLauncher,anFunName)
    PathToAutonomice = '/Users/Matte/Python_script/Phenopy3/old/Autonomice-Git'
    PathToPythonFun = '/Users/Matte/Python_script/Phenopy3/future/TEST_tmp.py'
    add_To_Custom_Analysis(PathToAutonomice,PathToPythonFun,AddTo = 'custom_Analysis_Gr_tmp.py')
#    ifCond = 'Power_Density'
#    funcName = 'function_Launcher_Gr'
#    remove_A_Funct(PathToPythonFile,funcName)
    