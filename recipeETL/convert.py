import os, json, re

folder = "食材字典_Jack"

os.chdir(folder)
xf = open(f'../{folder}.json', 'w', encoding='utf-8')
print(f"Write to {folder}.json")
for filename in os.listdir(os.getcwd()):
    if not re.match(r'^\d+.*\.csv', filename):
        print(filename)
        continue
    with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
        # skip 1 line
        line = f.readline()
        item = []
        obj = {}
        for line in f:
            item.append(re.sub(r'^"?\d+(.*?),?"?\n', r'\1', line))
        obj[item[0]]=item[1:]
        lntext = json.dumps(obj, ensure_ascii=False)[1:-1]+',\n'
        xf.write(lntext)

xf.close()