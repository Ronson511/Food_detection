import sys

cnChar = list("仼优兰刴发咸国圣块坚塩头姜嫰岛庄徳择掦无柠榄殻温湿炼猕现瑶盐筛籮类緑红绿苹荀荞葱蓝蔴蕯虾记调辢过选酱针铃铝铺锦门韮须饺马鱼鲍鲜鳯鸡麦黄黒龙⽔")
# 你 should change '姜'->'薑', '籮'->'蘿', '荀'->'筍' manually. and add '⽔' -> '水' manually. if run convertZ.exe to generate twChar
twChar = list("任優蘭剁發鹹國聖塊堅鹽頭薑嫩島莊德擇揚無檸欖殼溫濕煉獼現瑤鹽篩蘿類綠紅綠蘋筍蕎蔥藍麻薩蝦記調辣過選醬針鈴鋁鋪錦門韭須餃馬魚鮑鮮鳳雞麥黃黑龍水")

cn2twWord = {
    '豆乾': '豆干',
    '魚乾': '魚干',
    '梅乾': '梅干',
    '菜乾': '菜干',
    '肉乾': '肉干',
    '乾果': '干果',
    '干貝': '乾貝',
    '葡萄乾': '葡萄干',
    '芥末': '芥苿',
    '豆豉': '豆鼓',
    '伍斯特辣醬': '喼汁',
    '豬鍵子': '豬𦟌肉',
    '牛鍵': '牛𦟌肉',
    '豬鍵': '豬𦟌',
    '牛鍵': '牛𦟌',
    # '伊籐': '伊藤',
    '蘿蔔': '萝卜',
    '麵粉': '面粉',
    '麵包': '面包',
    '龍鬚麵': '龍須面',
    }

def parseCnChar(ch):
    if ch in cnChar:
        return twChar[cnChar.index(ch)]
    return ch

def parseCnWord(line):
    line = "".join([parseCnChar(ch) for ch in line]).strip()
    for twW, cnW in cn2twWord.items():
        if cnW in line:
            line = line.replace(cnW, twW)
            break
    # Run twice in case there're 2 cnWords
    for twW, cnW in cn2twWord.items():
        if cnW in line:
            line = line.replace(cnW, twW)
            break
    return line

def main(iFname, oFname):
    xf = open(oFname, 'w', encoding='utf-8')
    with open(iFname, 'r', encoding='utf-8') as f:
        for line in f:
            data = parseCnWord(line)
            xf.write(data+'\n')
    xf.close()

if __name__ == "__main__":
    iFname = sys.argv[1] if len(sys.argv) > 1 else "food_frequency_2.0-0.txt"
    oFname = sys.argv[2] if len(sys.argv) > 2 else "food_frequency_2.0-0u.txt"
    main(iFname, oFname)
    sys.exit(0)
