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


import numpy as np
import sys,os
import_dir = os.path.join(os.path.abspath(os.path.join(__file__,'../../..')),'import')
sys.path.append(import_dir)
#from functionCaller_Generator import get_Function_List
from copy import copy

class DataType_x_Analysis(object):
    def __init__(self):
        self.anList = {}
    def addAnalysis(self, anName,data_tuple):
        """
            Method objective:
            =================
                - This method adds info to the data analysis types for a specific
                analysis. It creates a nested dictionary contenining the data info
            Input:
            ======
                *1.*  anName = String, analysis name
                *2.* data_tuple = tuple. First element is the data type name
                    second element are the accepted types  as a list
                    (example: ('Behavior',['EEG','SleepSign']))
            
        """
        self.anList[anName] = {}
        for data_type in data_tuple:
            self.anList[anName][data_type[0]] = data_type[1]
            
    def __iter__(self):
        for anName in list(self.anList.keys()):
            for data_type in list(self.anList[anName].keys()):
                yield anName, data_type,self.anList[anName][data_type]
    def __getitem__(self,key):
        tuple_res = []
        for  data_type in list(self.anList[key].keys()):
            tuple_res += [(data_type,self.anList[key][data_type])]
        return tuple_res
    
    def pop(self,key):
        self.anList.pop(key)
    
    def addDataType(self,anName,tuple_type):
        self.anList[anName][tuple_type[0]] += [tuple_type[1]]
    
    def __repr__(self):
        string = 'Class DataType_x_Analysis:\n'
        for anName in list(self.anList.keys()):
            string += '\t' + anName + ':\n'
            for data_type in list(self.anList[anName].keys()):
                string += '\t\t' + data_type + ':\t' + self.anList[anName][data_type].__repr__()+'\n\n'
        return string

def remove_empty_and_comments(line_tuple):
    # remove empty lines
    for indent,line in copy(line_tuple):
        if line.rstrip().lstrip() is '':
            line_tuple.remove((indent,line))
    #remove comments
    for indent,line in copy(line_tuple):
        if line.lstrip().startswith('#'):
            line_tuple.remove((indent,line))
    # remove block comments 
    for comment_block in ['"""',"'''"]:
        max_ind = len(line_tuple)
        copy_tuple = copy(line_tuple)
        index = 0
        while index < max_ind:
            indent,line = copy_tuple[index]
            if line.lstrip().startswith(comment_block):
                first = True
                while not line.rstrip().endswith(comment_block) or first:
                    first = False
                    line_tuple.remove((indent,line))
                    index += 1
                    indent,line = copy_tuple[index]
                line_tuple.remove((indent,line))
            index += 1
    return line_tuple
       
def getminfind(line,ch0,ch1,pos=0):
    m = min(line.find(ch0,pos),line.find(ch1,pos))
    if m <0:
        m = max(line.find(ch0,pos),line.find(ch1,pos))
    return m

def openCloseCount(line,setStart,setEnd):
    """
        Return internal start and and of lists
    """
    ind = 0
    count = 0
    inString = False
    start_ch = getminfind(line,'"',"'")
    if start_ch is -1:
        stop_ch = -1
    else:
        stop_ch = line.find(line[start_ch],start_ch+1)
    for ch in line:
        inString = (ind > start_ch) * (ind < stop_ch)
        if ch == setStart and not inString:
            count += 1
        elif ch == setEnd and not inString:
            count -= 1
        elif ch == "'" and ind == stop_ch:
            start_ch = getminfind(line,'"',"'",stop_ch+1)
            if start_ch is -1:
                stop_ch = -1
            else:
                stop_ch = line.find(line[start_ch],start_ch+1)
        elif ch == '"' and stop_ch == ind:
            start_ch = getminfind(line,'"',"'",stop_ch+1)
            stop_ch = line.find(line[start_ch],start_ch+1)
            if start_ch is -1:
                stop_ch = -1
            else:
                stop_ch = line.find(line[start_ch],start_ch+1)
        ind += 1
    return count
    
def returnStartEndSets(line,setStart,setEnd):
    """
        Return internal start and and of lists
    """
    ind = 0
    listStart = []
    listBorder = []
    inString = False
    start_ch = getminfind(line,'"',"'")
    if start_ch is -1:
        stop_ch = -1
    else:
        stop_ch = line.find(line[start_ch],start_ch+1)
    for ch in line:
        inString = (ind > start_ch) * (ind < stop_ch)
        if ch == setStart and not inString:
            listStart += [ind]
        elif ch == setEnd and not inString:
            if len(listStart) is 1:
                listBorder += [(listStart.pop(-1),ind)]
            else:
                listStart.pop(-1)
        elif ch == "'" and ind == stop_ch:
            start_ch = getminfind(line,'"',"'",stop_ch+1)
            if start_ch is -1:
                stop_ch = -1
            else:
                stop_ch = line.find(line[start_ch],start_ch+1)
        elif ch == '"' and stop_ch == ind:
            start_ch = getminfind(line,'"',"'",stop_ch+1)
            stop_ch = line.find(line[start_ch],start_ch+1)
            if start_ch is -1:
                stop_ch = -1
            else:
                stop_ch = line.find(line[start_ch],start_ch+1)
        ind += 1
#    print('square',listBorder)
    return listBorder

def returnStringBorder(line):
    listBorder = []
    listStart = []
    ch_st = ''
    ind = 0
    for ch in line:
        if ch == '"':
            if len(listStart):
                if ch == ch_st:
                    listBorder += [(listStart.pop(-1),ind+1)]
            else:
                listStart = [ind]
                ch_st = ch
        elif ch == "'":
            if len(listStart):
                if ch == ch_st:
                    listBorder += [(listStart.pop(-1),ind+1)]
            else:
                listStart = [ind]
                ch_st = ch
        ind += 1
    return listBorder

def getFuncInputString(line,funcName):
    """
        Given a line of the form "
        ...,X,...=...,funcName(...),..."
        and funcName, it retunrs the string of funcName inputs
    """
    tmp = line[:line.find(funcName)+len(funcName)]
    isAssign, assignInd = findAssigmentEqual(tmp)
    if not isAssign:
        raise ValueError('String "line" must contain an assignment')
    line = line[assignInd + 1:].split(funcName)[1]
#    print('bline',line)
    parentIndex = returnStartEndSets(line,'(',')')
    dist_vect = np.zeros(len(parentIndex))
    k = 0
    for i0,i1 in parentIndex:
       dist_vect[k] = i0-assignInd
       k+=1
#    print('line',line)
#    print(dist_vect,parentIndex)
    parent = parentIndex[np.argmin(dist_vect)]
    return line[parent[0]+1:parent[1]]

def chopInput(string):
    """
        stringa rappresentate l'insieme di variabili da suddividere in 
        singoli elementi
        esempio:
            "a,(b,11),x" ---> ["a","(b,11)","x"]
    """
    stringBorders = returnStringBorder(string)
    sqBracketsBorders = returnStartEndSets(string,'[',']')
    roBracketsBorders = returnStartEndSets(string,'(',')')
    grBracketsBorders = returnStartEndSets(string,'{','}')
    allBorders = stringBorders + sqBracketsBorders + roBracketsBorders +\
        grBracketsBorders
    i0 = string.find(',')
    comma_index = []
    invalid = False
    while i0 >= 0:
        for bord in allBorders:
            if i0 > bord[0] and i0 < bord[1]:
                invalid = True
                break
        if invalid:
            invalid = False
        else:
            comma_index += [i0]
        i0 = string.find(',',i0+1)
    if len(comma_index) is 0:
        input_list = [string.rstrip().lstrip()]
    else:
        input_list = [string[:comma_index[0]].rstrip().lstrip()]
        i = -1
        for i in range(len(comma_index)-1):
            input_list += [string[comma_index[i]+1:comma_index[i+1]].rstrip().lstrip()]
        input_list += [string[comma_index[i+1]+1:].rstrip().lstrip()]   
    return input_list
    
def extract_defs(line_tuple):
    """
        return a list of function defs
    """
    def_list = []
    # get in defs
    index = 0
    indent,line = line_tuple[index]
    while index < len(line_tuple):
        
        line = line.rstrip()
        # scorri fino alla prossima def
        if not (line.startswith('def ') or line.startswith('def\t')):
            indent,line = line_tuple[index]
            index += 1
            continue
        # incomincia una lista in def_list che contenga tutta la def
        def_list += [[line]]
        index += 1
        indent,line = line_tuple[index]
        while indent != 0 and index < len(line_tuple):
            def_list[-1] += [line]
            indent,line = line_tuple[index]
            index += 1
    return def_list

def findAssigmentEqual(string):
    """
        Trova le stringhe con un unico assegnamento e di ritorna vero o 
        false se c'è assegnamento + indice dell'uguale
    """
    stringBorders = returnStringBorder(string)
    sqBracketsBorders = returnStartEndSets(string,'[',']')
    roBracketsBorders = returnStartEndSets(string,'(',')')
    grBracketsBorders = returnStartEndSets(string,'{','}')
    allBorders = stringBorders + sqBracketsBorders + roBracketsBorders +\
        grBracketsBorders
    i0 = string.find('=')
    equal_index = []
    invalid = False
    while i0 >= 0:
        for bord in allBorders:
            if i0 > bord[0] and i0 < bord[1]:
                invalid = True
                break
        if invalid:
            invalid = False
        else:
            equal_index += [i0]
        i0 = string.find('=',i0+1)
    if len(equal_index) != 1:
        isAssign = False
        assignInd = None
    else:
        isAssign = True
        assignInd = equal_index[0]
    return isAssign, assignInd


def varNameGet(list_string,varName):
    varVal = None
    for line in list_string[::-1]:
        # check if var name in line
        if not varName  in line:
            continue
        # check if the line contains an assignment
        isAssign, assignInd = findAssigmentEqual(line)
        if not isAssign:
            continue
        lhs = line[:assignInd]
        # lista di output a cui vengono assegnati i valori
        outputs = chopInput(lhs)
        # controllo se la mia variabile è nella lista
        if not varName in outputs:
            continue
        # se c'è tiro fuori l'indice
        input_num = outputs.index(varName)
        rhs = line[assignInd + 1:]
        inputs = chopInput(rhs)
        varVal = inputs[input_num]
        break
    return varVal

def merge_split_string(string_list):
    prev_line = string_list[0]
    new_list = []
    for line in string_list[1:]:
        if prev_line.rstrip().endswith('\\'):
            prev_line = prev_line[::-1].replace('\\','',1)[::-1]
            prev_line = prev_line.rstrip() + line.lstrip()
        else:
            new_list += [prev_line]
            prev_line = line
    new_list += [prev_line]
    return new_list

def merge_split_parenthesis(string_list,openPar,closePar):
    prev_line = string_list[0]
    new_list = []
    for line in string_list[1:]:
        if openCloseCount(prev_line,openPar,closePar) > 0:
            prev_line = prev_line[::-1].replace('\\','',1)[::-1]
            prev_line = prev_line.rstrip() + line.lstrip()
        else:
            new_list += [prev_line]
            prev_line = line
    new_list += [prev_line]
    return new_list

def getIndentLevel(string_list):
    line_tuple = []
    for line in string_list:
        indent_lev = len(line) - len(line.lstrip())
        line_tuple += [(indent_lev,line)]
    return line_tuple

def returnFirstCalledFunc(list_string, fname):
    for line in list_string[::-1]:
        if fname in line:
            tmp = line[:line.find(fname)+1]
            isAssign,assignInd = findAssigmentEqual(tmp)
        else:
            continue
        if isAssign:
            rhs = line[assignInd+1:].replace(' ','').replace('\t','')
            if fname+'(' in rhs:
                return line
        else:
            continue
    return

def getTypeInfo(input_list,ind=3):
    foundTypes = False
    for i in input_list:
        if 'Types=' in i.replace(' ','').replace('\t',''):
            foundTypes = True
            break
    if foundTypes:
        isAssign,assignInd = findAssigmentEqual(i)
        input_var = i[assignInd+1:].rstrip().lstrip()
    else:
        input_var = input_list[ind]
    boolean = input_var.startswith(('"',"'"))
    return boolean,input_var
        
def getTypes(pathToImport):
    type_list = []
    fh = open(pathToImport)
    all_lines = fh.readlines()
    fh.close()
    # merge continued strings
    all_lines = merge_split_string(all_lines)
    
    all_lines = merge_split_parenthesis(all_lines,'(',')')
    all_lines = merge_split_parenthesis(all_lines,'[',']')
    all_lines = merge_split_parenthesis(all_lines,'{','}')
    # get indentation levels
    line_tuple = getIndentLevel(all_lines)
    #remove comments and empty lines
    line_tuple = remove_empty_and_comments(line_tuple)
    # return a list of string lists containing one def function each
    def_list = extract_defs(line_tuple)
    ii=0
    for function in def_list:
        line = returnFirstCalledFunc(function,'Dataset_GUI')
#        print(line)
        ii+=1
        if line is None:
            continue
        string = getFuncInputString(line,'Dataset_GUI')
        list_input = chopInput(string)
        boolean,input_var = getTypeInfo(list_input,3)
        if not boolean:
           input_var = varNameGet(function,input_var)
        type_list += [input_var[2:-2]]
    return type_list

def refreshTypeList(path_to_phenopy):
    tl = getTypes(os.path.join(path_to_phenopy,'importDataset.py'))
    np.save(os.path.join(path_to_phenopy,'data_type_list.npy'),tl)
    return

if __name__ == '__main__':
    tl = getTypes(import_dir+'/importDataset.py')
#    print(tl)
#    a = ['ciao(,{,[' , 'mucca{,{','miao}}},)' ,']sa', 'sa']
#    l=merge_split_parenthesis(a,'{','}')
#    
#    print l
#    
#    l=merge_split_parenthesis(l,'(',')')
#    print l 
#    
#    l=merge_split_parenthesis(l,'[',']')
#    print l