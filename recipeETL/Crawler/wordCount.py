import sys, json, csv

# import utils
from utils.cleanQty    import qtyCleaner
from utils.cleanIngred import ingredCleaner
from utils.txt_loader  import set_loader
from utils.typoSyn     import groupSyn

from utils.nutriCalcer import nutriCalcer


folders = ["低脂","生酮","低醣","沙拉","高蛋白","健身","高纖"]

cntTotal = 0
cntProcs = 0
foodList = []
foodFreq = {}

nClean = int(sys.argv[1])  if len(sys.argv) > 1 else 4
bVerb  = bool(sys.argv[2]) if len(sys.argv) > 2 else False

ignore_IDs = set_loader('ID_exclude.txt')
nCalcer  = nutriCalcer()
skip_IDs = set()

iCleaner = ingredCleaner()
qCleaner = qtyCleaner()
grpSynom = groupSyn()

def procIngrdent(food_ID, ingreds, bVerb=bVerb, nClean=nClean):
    global foodList, foodFreq, cntTotal
    global iCleaner

    ingTbl = {}     # to avoid change ingreds in for-loop
    nutris = {}
    for food, qty in ingreds.items():  # 抓出"食譜"中的所有 key 和 值
        bAllOK = True
        if nClean > 0:
            nfood = iCleaner.clean(food_ID, food, bVerb=bVerb, nClean=nClean)
            qty_unit = qCleaner.clean(food_ID, qty, bVerb=bVerb)
            # print(f'{food_ID:>8}: {nfood:20}, {qty_unit}')
            # if food_ID == '276239':
            #     print('1')
            bFound, ingred = grpSynom.lookup(nfood)
            if bFound:
                if isinstance(qty_unit, list):
                    # if ingred == '胡蘿蔔':
                    #     print('1')
                    if qty_unit[1] == 'g' or qty_unit[1] == 'ml':
                        nutris[ingred] = qty_unit
                    else:
                        bAllOK = False
                        print(f'{food_ID:>8} {nfood}: {qty_unit[1]} != "g" or "ml".')
                else:
                    bAllOK = False
                    if qty_unit != '適量' and qty_unit != '少許':
                        print(f'{food_ID:>8} {nfood}: {qty_unit} not split.')
            else:
                bAllOK = False
                print(f'{food_ID:>8} {nfood} not in standard ingredent group.')
        else:
            bAllOK = False
            qty_unit = qty
            nfood    = food

        if iCleaner.checkSkip(food_ID, nfood, qty_unit, bVerb=True) > 0:
            skip_IDs.add(food_ID)
            # continue

        # 計算食材出現詞頻
        if nfood in foodList:
            foodFreq[nfood] += 1
        else:
            foodFreq[nfood] = 1
        foodList.append(nfood)
        #print(food) # 所有食材
        ingTbl[nfood] = qty_unit

    return bAllOK, ingTbl, nutris

xf1 = open('./clr-Long.txt', 'w', encoding='utf-8')
xf2 = open('./clr-Short.txt', 'w', encoding='utf-8')


## method1
# fd = open('./ok-nutris.csv', 'w', encoding='utf-8-sig')
# xf3 = csv.writer(fd, delimiter=',', quotechar='"')
# xf3.writerow(dataList)

## method2
# xf3 = open('./ok-nutris.csv', 'w', encoding='utf-8')
# xf3.write(u'\uFEFF')
# xf3.write(string+'\n')


xf3fd = open('./ok-nutris.csv', 'w', newline='', encoding='utf-8-sig')
hdrs = ['food_ID','菜名','group', 'ranking','份數',nCalcer._headers[3],'每份'+nCalcer._headers[3]]
hdrs.extend(nCalcer._headers[4:])
xf3 = csv.writer(xf3fd, delimiter=',', quotechar='"')
xf3.writerow(hdrs)
for i in folders:
    with open(f'{i}/{i}.txt', 'r', encoding='utf-8') as f:
        for line in f:              # 使用迴圈方式一條一條抓
            data = json.loads(line)

            cntTotal += 1
            food_ID = data['food_ID']
            if food_ID not in ignore_IDs:
                data['group'] = i
                data['推讚數'] = qCleaner.parseNumber(data['推讚數'])
                data['瀏覽數'] = qCleaner.parseNumber(data['瀏覽數'])
                if data['瀏覽數'] != 0:
                    ranking = data['推讚數']/data['瀏覽數'] * 100
                else:
                    ranking = 0
                data['份數']   = qCleaner.parseNumber(data['份數'])
                bflag, data['食譜'], nutri = procIngrdent(food_ID, data['食譜'], bVerb=bVerb, nClean=nClean)
                if bflag:
                    result = list(nCalcer.calc(nutri))
                    total  = result[0]
                    result = [str(v/data['份數']) for v in result]
                    food_Name = data["菜名"].replace('\n', '').strip()
                    # if '"' in food_Name:
                    #     food_Name = food_Name.replace('"', '""')
                    #     food_Name = f'"{food_Name}"'
                    # if ',' in food_Name:
                    #     # food_Name = food_Name.replace(',', '\\,')
                    #     food_Name = f'"""{food_Name}"""'
                    data3 = [food_ID,food_Name,i,ranking,data["份數"],total]
                    data3.extend(result)
                    xf3.writerow(data3)
                cntProcs += 1
                xf1.write(json.dumps(data, ensure_ascii=False)+'\n')
                xf2.write(json.dumps({'id':food_ID, 'group':i, 'ingredents':data['食譜']}, ensure_ascii=False)+'\n')
xf1.close()
xf2.close()
# xf3.close()

skipA, skipB, skipC = iCleaner.getSkip()
print(f"少許:{len(skipA)}\nList:{skipA}\n\n適量:{len(skipB)}\nList:{skipB}\n\n空白:{len(skipC)}\nList:{skipC}\n")
print(f'To Skip:{len(skip_IDs)}\nList:{skip_IDs}')

print(len(foodList)) # 總共多少食材
print(cntTotal, cntProcs) # 總共幾個食譜


# 詞頻轉成表格
import pandas as pd
df = pd.DataFrame.from_dict(foodFreq, orient='index', columns=['詞頻']) # 將字典轉為表格

# df = df.sort_index(ascending=False)
# df.to_csv("照食材順序排的food_frequency_2.0.csv", encoding="utf-8-sig")

df = df.sort_values(by='詞頻', ascending=False) # 照"詞頻"這欄的值，由大到小做排列 ascending=False
df.to_csv("照詞頻順序排的food_frequency_2.0.csv", encoding="utf-8-sig")
