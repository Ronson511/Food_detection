import os, json, re

folder = "食材字典_Jack"

# def reSynonym(item):
#     rgxSynonym = { "蒜頭": r"蒜[頭头味香]?[粉粒]", "麵粉": r"麵包(預拌|專用)?粉"}
#     for key, rgx in rgxSynonym.items():
#         if re.search(rgx, item):
#             print(f'find {rgx}:{item}')

def dictSynonym():
    Synonym = ["蠔", "破布子", "瑤柱", ["塔皮", "派皮"], ["蘋果", "Apple"], ["鳳梨", "蘿菠"], "蒔蘿", "榴槤", "羅曼",
        "辣根", "腐皮", "荸齊", "蔭豉", "紅珊瑚", "帆立貝", "尾冬骨", "玉子燒", ["奶油", "忌廉"],
        "冰淇淋", "養樂多", ["羊肉", "羊排"], "斑蘭", "桑葚", "漢堡排", "OREO", ["醬料", "老乾媽"], 
        "伏特加", "梔子花", "李子", "可樂", "黃耆", "松露", ["明膠", "吉利丁", "洋菜", "果凍粉", "膠粉", "蒟蒻", "蒟篛", "寒天"], "香蜂草", 
        "蔘鬚", "熟地", ["乳酪", "乾酪", "Ricotta", "mozzarella"], ["草莓", "士多啤梨"], 
        ["肉乾", "Jerky"], "蕃荽", "芫荽", ["甜菊", "Stevia"], 
        ["發粉", "泡打粉", "塔塔粉", "小蘇打粉", "蘇打", "梳打"], ["椰子", "椰粉"], ["抹茶", "焙茶"], "蓮藕", ["洋車前", "洋前車"],
        ["酥脆粉", "脆漿粉", "脆酥粉"],
        ["太白粉", "薯粉", "粟粉", "栗粉", "地瓜粉", "生粉", "玉蜀粉"],
        ["通心麵", "通心意粉", "通心粉", "通粉", "螺旋粉", "蝴蝶粉"],
        ["麵粉", "麵包預拌粉", "麵包專用粉", "小麥", "小麦", "預拌粉", "鬆餅粉", "全粒粉", "低粉"],
        "燕麥", ["穀粉", "穀物"], ["涼粉", "粉絲", "冬粉"], "蕎麥粉", "苦荞粉", ["辣木", "青汁"],
        "葛根", "花生", "柚子", ["煙燻粉", "煙熏粉"], "巧克力", "芝麻", ["亞麻仁", "亞麻子", "亞麻籽"], "榛果", "杏仁", "核桃", "咖哩",
        ["梅子", "酸梅"], "奇亞子", "仙草", "蒸肉粉",
        ["蒜頭", "蒜头", "蒜味", "蒜粉", "蒜粒", "蒜香"],
        ["香草", "香草粉", "香草風味粉"], ["洋香菜粉", "巴西里粉", "百里香粉", "洋香葉"], "羅勒粉", "海苔粉", "阿魏粉",
        ["五香", "五味粉", "醃肉粉"], ["豆蔻", "豆寇", "荳蔻"], ["肉桂", "玉桂"], ["薑", "生薑"],
        "香料", "丁香", "胡椒", "孜然", "茴香", "薑黃", "芥末", ["鹽", "粉紅岩鹽"],
        "七味粉", ["辣椒", "唐辛子", "辣粉", "辛香"],
        ["BBQ調味粉", "撒神秘粉", "椒鹽粉"], ["調味粉", "鰹魚粉", "柴魚粉", "魚粉", "雞粉", "雞肉調味粉", "惹味粉", "干貝粉", "提鮮粉", "鮮味粉", "香菇粉", "洋蔥粉"]]
    objs = {}
    for item in Synonym:
        if isinstance(item, list):
            objs[item[0]] = item[:]
        else:
            objs[item] = [item]
    return objs

def lookupSynonym(item, values):
    # if item in ["蒜頭", "麵粉"]:
    #     reSynonym(item)
    for sym in values:
        if sym == item:
            return True, False
        elif sym in item:
            return True, True
    else:
        return False, False


os.chdir(folder)
infile = "195粉.csv"
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