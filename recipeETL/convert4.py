import os, json, re

folder = "食材字典_Edden"

from typoSyn import *


os.chdir(folder)
infile = "太雜的.csv"
outfile = f"{folder}-{infile[:-4]}.json"

xf = open(f'../{outfile}', 'w', encoding='utf-8')

typoDict = typoSyn()
grpSyn  = groupSyn()
grpDict = groupSyn().dict

for filename in os.listdir(os.getcwd()):
    if not filename == infile:
        continue
    with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
        # skip 1 line
        line = f.readline()
        items = []
        for line in f:
            item = re.sub(r'^\d+(.*)\n', r'\1', line)
            item_norm = typoDict.replaceTypo(item)
            grpSyn.lookups(item, item_norm)
        # print(groupDict)
        print(f"Write to {folder}-{filename[:-4]}.json")
        for key, values in grpDict.items():
            obj = {}
            obj[key]=values[1:]
            lntext = json.dumps(obj, ensure_ascii=False)[1:-1]+',\n'
            xf.write(lntext)

xf.close()