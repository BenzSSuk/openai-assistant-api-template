import os
import glob


def getFullpath_Folder_Filename(path):
    head, tail = os.path.split(path)
    if '.' in tail:
        filename = tail
        fullpath = path

        head2, tail2 = os.path.split(head)
        folderName = tail2

    else:
        # this is path of folder not file
        filename = None
        fullpath = None
        folderName = None

    return fullpath, folderName, filename


def splitAndConcatPathFolderFilename(listPath):
    listDir = []
    listFolder = []
    listName = []
    for ipath in range(len(listPath)):
        path = listPath[ipath]
        fullpath, folderName, filename = getFullpath_Folder_Filename(path)

        if filename is not None:
            listDir.append(fullpath)
            listFolder.append(folderName)
            listName.append(filename)

    return listDir, listFolder, listName


def findNSubfolder(path):
    path = os.path.normpath(path)
    nSubFolderPath = len(path.split(os.sep))

    return nSubFolderPath


def findFile(pathSearch, stringSearch, nSubFolderSearch=0, searchBy='extension'):
    '''
        Example

        folderA
            |
            ---file01.csv     --\
            ---file02.csv        > nSubFolderSearch = 0
            ---file03.csv     --/
            ---folderB
                |
                ---file04.csv   --\
                ---file05.csv      >  nSubFolderSearch = 1
                ---file06.csv   --/

        Input:
            pathSearch = ...\...\folderA
            stringSearch = '*.csv' >> all file that contain .csv
                         = '*' >> all folder or file in pathSearch
            nSubFolderSearch = 0

        output: file01.csv,file02.csv,file03.csv

        Input:
            pathSearch = ...\...\folderA
            stringSearch = '*.csv' >> all file that contain .csv
            nSubFolderSearch = 1

        output: file04.csv, file05.csv, file06.csv
    '''
    # os.chdir(pathSearch)
    nSubFolderPath = findNSubfolder(pathSearch)

    if nSubFolderSearch == -1:
        pathSearchExtend = os.path.join(pathSearch, '**/{}')
        listFileAll = glob.glob(pathSearchExtend.format(stringSearch), recursive=True)
        listDir, listFolder, listName = splitAndConcatPathFolderFilename(listFileAll)

        return listDir, listFolder, listName

    elif nSubFolderSearch == 0:
        if searchBy == 'extension':
            pathSearchExtend = os.path.join(pathSearch, stringSearch)
            # pathSearchExtend = pathSearch
            listFileAll = glob.glob(pathSearchExtend, recursive=False)



        elif searchBy == 'partOfName':
            listFileAll = []
            countSubFolder = -1
            for (root, dirs, files) in os.walk(pathSearch, topdown=True):
                countSubFolder = countSubFolder + 1

                nRoots = len(root)
                nFolders = len(dirs)
                nFiles = len(files)
                # print(f'root {count}/{nRoots}: {root}')
                # for ifolder in range(nFolders):
                # print(f'-{dirs[ifolder]}')

                if countSubFolder == nSubFolderSearch:
                    for ifile in range(nFiles):
                        fileName = files[ifile]
                        if stringSearch in fileName:
                            # print(f'--{files[ifile]}')
                            listFileAll.append(os.path.join(pathSearch, fileName))

                    break

        listDir, listFolder, listName = splitAndConcatPathFolderFilename(listFileAll)

        return listDir, listFolder, listName

    elif nSubFolderSearch > 0:
        pathSearchExtend = os.path.join(pathSearch, '**/{}')
        listFileAll = glob.glob(pathSearchExtend.format(stringSearch), recursive=True)
        # for (root, dirs, files) in os.walk(pathSearch, topdown=True):
        #     count = count + 1
        listFileMatchSubFolder = []
        for path in listFileAll:
            nSubFolderPathWalk = findNSubfolder(path)
            layerFolder = (nSubFolderPathWalk - nSubFolderPath)

            if (nSubFolderSearch == layerFolder):
                listFileMatchSubFolder.append(path)

        listDir, listFolder, listName = splitAndConcatPathFolderFilename(listFileMatchSubFolder)

        return listDir, listFolder, listName

    # nSubFolderSearch = nSubFolderSearch + 1
    # nFileFound = len(listFileAll)
    # listFil_folder = []
    #
    # listFil_name = []
    # listFil_dir = []
    # for ifile in range(nFileFound):
    #     listFileIn = listFileAll[ifile]
    #     if '/' in listFileIn:
    #         # dir from mac and linux
    #         listSplit = listFileIn.split('/')
    #         folderFile = listSplit[-2]
    #         fileName = listSplit[-1]
    #         nSplit = len(listSplit)
    #     elif '\\' in listFileIn:
    #         # dir from window
    #         listSplit = listFileIn.split('\\')
    #         folderFile = listSplit[-2]
    #         fileName = listSplit[-1]
    #         nSplit = len(listSplit)
    #     else:
    #         folderFile = listFileIn
    #         fileName = listFileIn
    #         nSplit = 1
    #
    #     if nSubFolderSearch == -1 or (nSplit - 1) == nSubFolderSearch:
    #
    #         listDirFile = os.path.join(pathSearch,listFileIn)
    #         #        print('loading...')
    #
    #         listFil_dir.append(listDirFile)
    #
    #         listFil_name.append(fileName)
    #
    #         listFil_folder.append(folderFile)

    # return listDir, listFolder, listName


def listFolder(pathFolder):
    '''
    list all folder in directory
    '''

    listExperiment = os.listdir(pathFolder)

    # delete all file that include .
    for filefound in listExperiment:
        if '.' in filefound:
            listExperiment.remove(filefound)

    return listExperiment


def filterList(listIn, wordFilter, inverse=False):
    listFilter = []
    for ielement in listIn:
        if wordFilter in ielement:
            listFilter.append(ielement)

    if len(listFilter) == 1:
        listFilter = listFilter[0]

    return listFilter


def isFolderExist(pathFolder):
    '''
    check is input path exist, if not create folder
    '''

    if not os.path.exists(pathFolder):
        os.makedirs(pathFolder)

def get_n_file_in_folder(folder):
    list_folder = listFolder(folder)

    dict_class_file = {}
    for class_id in list_folder:
        FOLDER_CLASS = os.path.join(folder, class_id)
        list_file = os.listdir(FOLDER_CLASS)

        dict_class_file[class_id] = len(list_file)

    return dict_class_file

def greeting():
    print("Hello world")


def get_greeting():
    return "Hello world, from SignalProcessing"