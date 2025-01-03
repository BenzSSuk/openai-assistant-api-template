import json
from .file import *

def read_json(pathFile, mode='r'):
    f = open(pathFile, mode)
    dict_json = json.load(f)
    f.close()

    return dict_json

def read_json_folder(folder):
    listDir, listFolder, listName = findFile(folder, "*.json", nSubFolderSearch=0, searchBy='extension')

    list_json = []
    for path_json in listDir:
        list_json.append(read_json(path_json))

    return list_json
