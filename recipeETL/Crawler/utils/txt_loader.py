import json, csv
import numpy as np

def set_loader(path):
    '''
    Load lines in text file as a set(). 
    '''
    keyFile = path
    keySet  = set()
    try:
        with open(keyFile, "r", encoding='utf-8') as f:
            for line in f:
                line = line.replace('\n', '')
                if len(line) > 0:
                    keySet.add(line)
    except:
        print('No list loaded to set().')
    return keySet


def dict_loader(path):
    '''
    Load lines in text file as a dict(). 
    '''
    keyFile = path
    keyDict = dict()
    tmpDic = dict()
    try:
        with open(keyFile, "r", encoding='utf-8') as f:
            for line in f:
                if len(line) > 0:
                    dobj = json.loads('{'+line+'}')
                    for key, value in dobj.items():
                        if key not in tmpDic.keys():
                            tmpDic[key]=[key]
                        tmpDic[key].extend(value)
    except:
        print(f'Error on loading file:{path} to dict().')
    for key, value in tmpDic.items():
        keyDict[key] = list(set(value))
    return keyDict


def dict_csvloader(path):
    '''
    Load lines in text file as a dict(). 
    '''
    keyDict = dict()
    with open(path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = list(next(reader, None).keys())
        # if headers[0][0] == u'\ufeff':
        #     headers[0] = headers[0][1:]
        for row in reader:
            data = tuple(row.values())
            if data[2]=='':
                break
            vstr = np.array(data[3:])
            vstr[vstr==''] = '0'
            keyDict[data[2]] = vstr.astype(np.float32)

    return keyDict, headers

