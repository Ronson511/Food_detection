import os, json, re


def parseNumber(str):
    if str is None:
        return 1
    else:
        try:
            str = re.sub(r'(,|\n)', '', str)
            if '.' in str:
                return int(float(str)*10000)
            elif str == '':
                return 0
            else:
                return int(str)
        except:
            print('error:', str)


chiNum1 = [ "零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十" ]
chiNum2 = [ "０", "１", "２", "３", "４", "５", "６", "７", "８", "９" ]

def parseChiNum(ch):
    if ch in chiNum1:
        return str(chiNum1.index(ch))
    if ch in chiNum2:
        return str(chiNum2.index(ch))
    return ch


def splitUnit(str):
    au = re.split(r'((?:[0-9]+\+)?[0-9]+[/.~\-]?[0-9]*) *', str)
    if len(au) == 3:
        if '/' in au[1]:
            return [eval(au[1]), au[2]]
        elif '.' in au[1]:
            return [float(au[1]), au[2]]
        elif '-' in au[1] or '~' in au[1]:
            vals = re.split(r'[\-~]', au[1])
            return [eval(f'({vals[0]}0+{vals[1]}0)/20'), au[2]]
        else:
            return [int(au[1]), au[2]]
    elif str[0] == '半':
        return [0.5, str[1:]]
    else:
        return str


def replaceUnit(au):
    if isinstance(au, list):
        if au[1] in ['CC', 'cc', 'c.c', 'c.c.','C.C', 'mL', '毫升']:
            au[1] = 'ml'
        if au[1] in ['G', '克', '公克']:
            au[1] = 'g'
        if au[1] in ['大湯匙', '湯匙', '汤匙', '大匙', '甲匙', 'tbs', 'Tbs', 'tbsp', 'Tbsp', 'EL']:
            if not isinstance(au[0], str):
                return [au[0]*15, 'g']
            else:
                return au
        elif au[1] in ['小湯匙', '茶匙', '小匙', '丙匙', '匙', '茶匙tsp', 'TL']:
            if not isinstance(au[0], str):
                return [au[0]*5, 'g']
            else:
                return au
        elif au[1] in ['茶杯', '杯']:
            if not isinstance(au[0], str):
                return [au[0]*240, 'ml']
            else:
                return au
        elif au[1] in ['台兩', '兩']:
            if not isinstance(au[0], str):
                return [au[0]*37.5, 'g']
            else:
                return au
        return au
    else:
        return au

def parseline(line):
    obj = json.loads(line)
    obj["推讚數"] = parseNumber(obj["推讚數"])
    obj["瀏覽數"] = parseNumber(obj["瀏覽數"])
    obj["份數"]   = parseNumber(obj["份數"])
    x = obj["食譜"]
    for key, value in x.items():
        print(value, end=' ')
        value = "".join([parseChiNum(ch) for ch in value])
        if value[0]=='兩':
            value = '2'+value[1:]
        if value[0]=='約':
            value = value[1:]
        value = value.replace('¼', '0.25')
        value = value.replace('½', '0.5')
        value = value.replace('¾', '0.75')
        value = value.replace('又', '+')
        value = value.replace('～', '~')
        value = value.replace('—', '-')
        value = value.replace('－', '-')
        value = value.replace(' - ', '-')
        value = value.replace(' ~ ', '~')
        if '分之' in value:
            value = re.sub(r'([0-9]+)分之([0-9]+) *', r'\2/\1', value)
        x[key] = replaceUnit(splitUnit(value))
        print(key, x[key])

    obj["食譜"] = x
    # print(obj["food_ID"], obj["推讚數"], obj["瀏覽數"], obj["份數"])
    return json.dumps(obj, ensure_ascii=False)
        # re.sub(r'([0-9]+)/([0-9]+)', str(int), value)


os.chdir("食譜原始檔")
xf = open('../dump.txt', 'w', encoding='utf-8')
for filename in os.listdir(os.getcwd()):
    with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
        # do our stuff
        for line in f:
            if len(line) > 1:
                xf.write(parseline(line)+'\n')
    print(filename)

xf.close()