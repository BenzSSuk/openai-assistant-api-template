import numpy as np

def removeNan(arr):
    if isinstance(arr, np.ndarray):
        arrRemoveNan = arr[~np.isnan(arr)]
        n = arrRemoveNan.size
        if n == 0:
            arrRemoveNan = np.nan
            n = np.nan

        return arrRemoveNan, n
def findError(ref, output, data_type='number', only_acc=False):
    dictError = {}

    if data_type == 'number':
        error = ref - output
        nRaw = ref.size

        if nRaw == 0:
            error = np.nan
            nRaw = np.nan
            n = np.nan
        else:
            # remove nan
            # error = error[~np.isnan(error)]
            # n = error.size
            # if n == 0:
            #     error = np.nan
            #     n = np.nan
            error, n = removeNan(error)

        error_pow2 = np.power(error, 2)

        # accuracy
        nCorrects = np.sum(error == 0)
        dictError['accuracy'] = nCorrects/n
        # Sum square
        dictError['se'] = np.sum(error_pow2)
        # mean sum square
        dictError['mse'] = np.average(error_pow2)
        # Root mean square
        dictError['rms'] = np.sqrt(dictError['se']/n)
        # mean abs
        dictError['mae'] = np.average(np.abs(error))
        # mean
        dictError['mean'] = np.average(error)
        # SD
        dictError['sd'] = np.std(error)
        dictError['n_all'] = nRaw
        dictError['n_nan'] = nRaw - n
        dictError['perc_nan'] = (dictError['n_nan']/nRaw)*100

    elif data_type == 'class':
        arrBoolMatch = (output == ref)
        n = arrBoolMatch.size

        if n > 0:
            arrBoolMatch, n_no_nan = removeNan(arrBoolMatch)
            n_no_nan = arrBoolMatch.size
            n_nan = n - n_no_nan

            # accuracy
            nCorrects = np.sum(arrBoolMatch)

            if only_acc:
                dictError['accuracy'] = nCorrects / n_no_nan

            else:
                dictError['n'] = n
                dictError['n_correct'] = nCorrects
                dictError['accuracy'] = nCorrects / n_no_nan

        else:
            n_no_nan = 0
            n_nan = 0

    return dictError, arrBoolMatch

def findErrorDF(df, headerRef, headerOut, multipleCompare=False,
                data_type='number'):

    ref = df[headerRef].values
    output = df[headerOut].values

    dictError, error = findError(ref, output, data_type)

    return dictError, error
