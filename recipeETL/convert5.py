import os, json, re

folder = "食材字典"

from typoSyn import *


os.chdir(folder)
infile = "太雜的.csv"
outfileM = f"{folder}.json"
outfileX = f"{folder}-{infile[:-4]}.json"

mf = open(f'../{outfileM}', 'w', encoding='utf-8')
xf = open(f'../{outfileX}', 'w', encoding='utf-8')

typoDict  = typoSyn()
grpSyn = groupSyn()
grpDict = groupSyn().dict

for filename in os.listdir(os.getcwd()):
    rgxFn = re.compile(r'^\d+(.*)\.csv')
    if re.match(rgxFn, filename):
        print(filename)
        mKey=re.split(rgxFn, filename)[1]
        with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
            # skip 1 line
            line = f.readline()
            items = []
            obj = {}
            for line in f:
                items.append(re.sub(r'^"?\d+(.*?),?"?\n', r'\1', line))
            obj[mKey]=items
            lntext = json.dumps(obj, ensure_ascii=False)[1:-1]+',\n'
            mf.write(lntext)
            continue

    # elif filename == infile:
    #     with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
    #         # skip 1 line
    #         line = f.readline()
    #         items = []
    #         for line in f:
    #             item = re.sub(r'^\d+(.*)\n', r'\1', line)
    #             item_norm = typoDict.replaceTypo(item)
    #             for key, values in grpDict.items():
    #                 bFind, bAppend = grpSyn.lookup(item_norm, values)
    #                 if bFind:
    #                     if bAppend or item_norm != item:
    #                         grpDict[key].append(item)
    #                     # if item_norm != item:
    #                     #     print('1')
    #                     break
    #             else:
    #                 print('NG', item)
    #         # print(groupDict)
    #         print(f"Write to {folder}-{filename[:-4]}.json")
    #         for key, values in grpDict.items():
    #             obj = {}
    #             obj[key]=values[1:]
    #             lntext = json.dumps(obj, ensure_ascii=False)[1:-1]+',\n'
    #             xf.write(lntext)

mf.close()
xf.close()