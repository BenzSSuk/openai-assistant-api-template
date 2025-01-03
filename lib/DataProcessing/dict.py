import numpy as np
import json

def dictAppend(myDict,newKeyName,newKeyVal):
    '''
    newKeyValue must be scalar or array that match with exist size
    '''
    if newKeyName in myDict.keys():
        # already create header of this feature, just append it.
        if isinstance(newKeyVal, list):
            for i in range(len(newKeyVal)):
                myDict[newKeyName].append(newKeyVal[i])
        else:
            myDict[newKeyName].append(newKeyVal)

    else:
        # found new feature name, create new dict.
        myDictNew = {newKeyName:[]}
        myDictNew[newKeyName].append(newKeyVal)
        myDict.update(myDictNew)

    return myDict

def appendDictToDict(dict_ori, dict_add):

    for newKeyName in dict_add.keys():
        dictAppend(dict_ori, newKeyName, dict_add[newKeyName])

    return dict_ori

def isVectorOrMatric(arrayIn):
    if isinstance(arrayIn, np.ndarray):
        nElements = arrayIn.size
        featureShape = arrayIn.shape
        nShape = len(featureShape)
        isArray1Index = (nShape == 1) and (featureShape[0]>1)
        isArray2Index = (nShape == 2) and ( 1 in featureShape)

        if isArray1Index or isArray2Index:
            arrayIs = 'vector'
        elif nShape > 2 and featureShape[0] > 1 and featureShape[1] > 1:
            arrayIs = 'matric'
        else:
            ValueError('dimension of data was not recognite ! ')

    else:
        arrayIs = 'scalar'
        nElements = 1
        # ValueError('Input not numpy array !')

    return arrayIs, nElements

def checkFeatureVal(featureVal, addType):
    # loop for support array of feature value
    if isinstance(featureVal, np.ndarray):
        # it must be extenRow or extenCol
        featureType, nFeat = isVectorOrMatric(featureVal)
        if featureType == 'matric':
            addType = 'extenCol'

    elif isinstance(featureVal, list):
        featureType = 'vector'
        nFeat = len(featureVal)

    elif isinstance(featureVal, dict):
        featureType = 'dict'
        nFeat = 1

    else:
        featureType = 'scalar'
        nFeat = 1

    if isinstance(featureVal, np.ndarray) and featureType == 'vector':
        featureVal = featureVal.flatten()

    return addType, featureType, nFeat

def addFeatureToDict(dictFeature, featureName, featureVal, addType='fix'):
    '''
    Input:
        addType: 'fix'       = append scalar data to dict
                'extenCol'   = split array data to scalar and append to dict with new key "featureName_1", "featureName_2", ...
                'extenRow'   = append array data to dict with key "featureName"
                'listArray'  = convert array to list and store in cell
                'dict'
    '''

    addType, featureType, nFeat = checkFeatureVal(featureVal, addType)

    if addType == 'fix':
        if featureType == 'scalar' and nFeat == 1:
            dictFeature = dictAppend(dictFeature, featureName, featureVal)

        elif featureType == 'dict':
            dictFeature = appendDictToDict(dictFeature, featureVal)

        elif featureType == 'vector':
            # a_list = ["a", "b", "c"]
            listFeat = list(featureVal)
            converted_list = [str(element) for element in listFeat]
            joined_string = ",".join(converted_list)
            joined_string = "{" + joined_string + "}"
            dictFeature = dictAppend(dictFeature, featureName, joined_string)

        else:
            ValueError('addType=fix but nFeat > 1, Please select addType = extenCol or extenRow.')

    elif addType == 'extenRow':
        if featureType == 'vector':
            for ifeat in range(nFeat):
                dictFeature = dictAppend(dictFeature, featureName, featureVal[ifeat])

    elif addType == 'extenCol':
        if featureType == 'vector':
            for ifeat in range(nFeat):
                nameDict = featureName + '_' + str(ifeat+1)
                dictFeature = dictAppend(dictFeature, nameDict, featureVal[ifeat])

        elif featureType == 'matric':
            nRow, nCol = featureVal.shape
            for ic in range(nCol):
                nameDict = featureName + '_' + str(ic+1)
                for ir in range(nRow):
                    dictFeature = dictAppend(dictFeature, nameDict, featureVal[ir,ic])


    return dictFeature

def write_dict(dictWrite, path, filetype="json", indent=1):
    if filetype == "json":
        fileSave = open(path, 'w')
        json.dump(dictWrite, fileSave, indent=indent)
        fileSave.close()
