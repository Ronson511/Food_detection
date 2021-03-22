import os, json, re

folder = "食材字典_Jack"


def dictSynonym():
    Synonym = ["蠔", "破布子", "瑤柱", ["塔皮", "派皮"], ["蘋果", "Apple"], ["鳳梨", "蘿菠"], "蒔蘿", "榴槤", "羅曼",
        "辣根", "腐皮", "荸齊", "蔭豉", "紅珊瑚", "帆立貝", "尾冬骨", "玉子燒", ["奶油", "忌廉"],
        "冰淇淋", "養樂多", ["羊肉", "羊排"], "斑蘭", "桑葚", "漢堡排", "OREO", ["醬料", "老乾媽"], 
        "伏特加", "梔子花", "李子", "亞麻子", "可樂", "黃耆", "松露", ["明膠", "吉利丁"], "香蜂草", 
        "蔘鬚", "熟地", ["乳酪", "乾酪", "Ricotta", "mozzarella"], ["草莓", "士多啤梨"], 
        ["肉乾", "Jerky"], "蕃荽", ["甜菊", "Stevia"] ]
    objs = {}
    for item in Synonym:
        if isinstance(item, list):
            objs[item[0]] = item[:]
        else:
            objs[item] = [item]
    return objs

def lookupSynonym(item, values):
    for sym in values:
        if sym == item:
            return True, False
        elif sym in item:
            return True, True
    else:
        return False, False


os.chdir(folder)
infile = "太雜的.csv"
outfile = f"{folder}-{infile[:-4]}.json"

xf = open(f'../{outfile}', 'w', encoding='utf-8')
for filename in os.listdir(os.getcwd()):
    if not filename == infile:
        continue
    with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
        # skip 1 line
        line = f.readline()
        items = []
        objs = dictSynonym()
        for line in f:
            item = re.sub(r'^\d+(.*)\n', r'\1', line)
            for key, values in objs.items():
                bFind, bAppend = lookupSynonym(item, values)
                if bFind:
                    if bAppend:
                        objs[key].append(item)
                    break
            else:
                print('NG', item)
        # print(objs)
        print(f"Write to {folder}-{filename[:-4]}.json")
        for key, values in objs.items():
            obj = {}
            obj[key]=values[1:]
            lntext = json.dumps(obj, ensure_ascii=False)[1:-1]+',\n'
            xf.write(lntext)

xf.close()