import pandas as pd
import os
import numpy as np
from .file import *

def loadCombineExport(pathType,pathLoad,pathSave,nameSave):

    if pathType == 'fullPath':
        listFil_dir = pathLoad
        nFiles = len(listFil_dir)
        for ifeat in range(nFiles):

            if ifeat == 0:
                dfFeatsAll = pd.read_csv(listFil_dir[ifeat])
            else:
                dfFeatsLoad = pd.read_csv(listFil_dir[ifeat])
                dfFeatsAll = pd.concat([dfFeatsAll, dfFeatsLoad], ignore_index=True)

        dfFeatsAll.to_csv( os.path.join(pathSave,nameSave) )

def filterTable(df, dictFilter):
    '''
    dictFilter = {
        "header_1": {
            "val": 99
            "inverse": True or False
        },
        "header_2": {
            "val": "A",
            "inverse": True or False
        }
    }

    :param df:
    :param dictFilter:
    :return:
    '''
    nrow = df.shape[0]
    isFirstItem = True
    for headerFil, dictVal in dictFilter.items():
        filterVal = dictVal['val']
        inverse = dictVal['inverse']

        if isinstance(filterVal, list):
            raise ValueError('filter valuse is list, can not process')

        if not inverse:
            indexFilterOut = df[headerFil].values == filterVal
        else:
            indexFilterOut = df[headerFil].values != filterVal

        if isFirstItem:
            indexFilterAll = indexFilterOut.copy()
            isFirstItem = False
        else:
            indexFilterAll = np.logical_and(indexFilterAll, indexFilterOut)

    dfFilter = df.loc[indexFilterAll, ]
    dfFilter.reset_index(inplace=True)

    return dfFilter, indexFilterAll



def read_csv_folder(pathFolder):
    listDir, listFolder, listName = findFile(pathFolder, '*.csv', 0)

    nFiles = len(listName)

    if nFiles == 1:
        df = pd.read_csv(listDir[0])

        return df

    elif nFiles > 1:
        listDF = []

        for ifile in range(len(listName)):
            df = pd.read_csv(listDir[ifile])

            listDF.append(df)

        return listDF

    else:
        df = []
        return df

def readCSVInfolder(pathFolder):
    listDir, listFolder, listName = findFile(pathFolder, '*.csv', 0)

    nFiles = len(listName)

    if nFiles == 1:
        df = pd.read_csv(listDir[0])

        return df

    elif nFiles > 1:
        listDF = []

        for ifile in range(len(listName)):
            df = pd.read_csv(listDir[ifile])

            listDF.append(df)

        return listDF

    else:
        df = []
        return df

def read_concat_write_csv_folder(folderLoad, folderSave, nameSave):
    listDir, listFolder, listName = findFile(folderLoad, '*.csv', 0)

    for ifile in range(len(listName)):
        df = pd.read_csv(listDir[ifile])

        if ifile == 0:
            dfAll = df
        else:
            dfAll = pd.concat((dfAll, df), axis=0)

    dfAll.to_csv(os.path.join(folderSave, nameSave))
