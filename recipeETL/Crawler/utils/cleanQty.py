import re

class qtyCleaner:

    def parseNumber(self, vstr):
        if vstr is None:
            return 1
        try:
            vstr = re.sub(r'(,|\n)', '', vstr)
            if '.' in vstr:
                return int(float(vstr)*10000)
            elif vstr == '':
                return 0
            else:
                return int(vstr)
        except Exception as e:
            print('error:', e)
            return 0


    _cnChar = list("适个条几两颗许汤块丝酙删头当丢选朶亳缶灌辦∼（）ｇ")
    _twChar = list("適個條幾兩顆許湯塊絲斟刪頭當丟選朵毫罐罐瓣~()g")
    def _cvtChar(self, ch):
        if ch in self._cnChar:
            return self._twChar[self._cnChar.index(ch)]
        return ch

    def _cvtStr(self, line):
        return "".join([self._cvtChar(ch) for ch in line]).strip()


    _chiNum1 = [ "零", "一", "二", "三", "四", "五", "六", "七", "八", "九" ] #, "十"
    _chiNum2 = [ "０", "１", "２", "３", "４", "５", "６", "７", "８", "９" ]
    def _cvtNumChar(self, ch):
        if ch in self._chiNum2:
            return str(self._chiNum2.index(ch))
        if ch in self._chiNum1:
            return str(self._chiNum1.index(ch))
        return ch

    _rgx1A = re.compile(r'^(.+?)\((.+)\)')
    _rgx1B = re.compile(r'^\((.+?)\)(.+)')
    def _splitStr(self, qtyStr):
        mat1 = self._rgx1A.search(qtyStr)
        if mat1:
            part1, part2 = mat1.groups()
            return part1, part2
        mat2 = self._rgx1B.search(qtyStr)
        if mat2:
            part1, part2 = mat2.groups()
            return part1, part2
        return qtyStr, ''


    _rgx3 = re.compile(r'(十(?:來|多|幾|五六))')
    _rgx4 = re.compile(r'(\d+)')
    _unitsA = list('塊個顆根尾份盒片杯罐包辦瓣支隻粒串副')
    _unitsB = ['克', 'g', 'cc', 'ml', 'mL']
    def _cvtNumStr(self, qtyStr):
        qtyStr = "".join([self._cvtNumChar(ch) for ch in qtyStr])

        qtyStr = self._rgx3.sub('15', qtyStr)
        if '二十' not in qtyStr and '數十' not in qtyStr:
            qtyStr = qtyStr.replace('十', '10')

        # if '顆(小型)' in qtyStr:
        #     print('1')
        part1, part2 = self._splitStr(qtyStr)
        if part2 != '':
            mat1 = self._rgx4.search(part1)
            mat2 = self._rgx4.search(part2)
            if mat1 and not mat2:
                qtyStr = part1
            elif mat2 and not mat1:
                qtyStr = part2
            elif mat1 and mat2:
                for unit in self._unitsA:
                    if unit in part1:
                        qtyStr = part2
                        break
                    elif unit in part2:
                        qtyStr = part1
                        break
                else:
                    for unit in self._unitsB:
                        if unit in part1:
                            qtyStr = part1
                            break
                        elif unit in part2:
                            qtyStr = part2
                            break
                    else:
                        for x in ['小型']:
                            if x in part2:
                                qtyStr = part1
                                break
                        qtyStr = f'{part1}({part2})'
                # print(f'Both: {part1}, {part2} use {qtyStr}')

        if len(qtyStr) > 0:
            if qtyStr[0]=='兩':
                qtyStr = '2'+qtyStr[1:]
            if qtyStr[0]=='約':
                qtyStr = qtyStr[1:]

        qtyStr = qtyStr.replace('¼', '0.25')
        qtyStr = qtyStr.replace('½', '0.5')
        qtyStr = qtyStr.replace('¾', '0.75')
        return qtyStr

    _rgx1 = re.compile(r'((?:[0-9]+\+)?[0-9]+[/.~\-+]?[0-9]*)\s*')
    def _splitUnit(self, qstr):
        # nonlocal id
        au = self._rgx1.split(qstr)
        # au = re.split(r'((?:[0-9]+\+)?[0-9]+[/.~\-]?[0-9]*) *', qstr)
        if len(au) == 3:
            if '/' in au[1]:
                return [eval(au[1]), au[2]]
            elif '.' in au[1]:
                return [float(au[1]), au[2]]
            elif '-' in au[1] or '~' in au[1]:
                vals = re.split(r'[\-~]', au[1])
                return [eval(f'({vals[0]}0+{vals[1]}0)/20'), au[2]]
            elif '+' in au[1]:
                vals = re.split(r'\+', au[1])
                return [eval(f'{vals[0]}+{vals[1]}'), au[2]]
            else:
                return [int(au[1]), au[2]]
        # elif qstr[0] == '半':
        #     return [0.5, qstr[1:]]
        else:
            return qstr

    _unitCvt = [
        { "val":   15, "unit": "g", "keys": ['大湯匙', '湯匙', '大匙', '甲匙', '湯匙tbs', 'tbs', '匙tbsp', 'tbsp', 'tabsp', '大匙tbsp.', 'el'] },
        { "val":    5, "unit": "g", "keys": ['小湯匙', '茶匙', '小匙', '丙匙', '匙', '茶匙tsp', 'tsp', 'tl', '小匙tsp.', 'tsp 茶匙'] },
        { "val":  240, "unit":"ml", "keys": ['茶杯', '杯'] },
        { "val":   30, "unit":"ml", "keys": ['shot'] },
        { "val":  300, "unit":"ml", "keys": ['嘜杯']},
        { "val": 1000, "unit":"ml", "keys": ['公升', 'L'] },
        { "val":   50, "unit": "g", "keys": ['市兩', '両'] },
        { "val": 37.5, "unit": "g", "keys": ['台兩', '兩'] },
        { "val":  600, "unit": "g", "keys": ['台斤', '斤'] },
        { "val":  500, "unit": "g", "keys": ['市斤'] },
        { "val": 1000, "unit": "g", "keys": ['公斤', 'kg'] },
        { "val":28.35, "unit": "g", "keys": ['oz', '盎司'] },
        { "val":453.6, "unit": "g", "keys": ['磅'] },
    ]
    def _replaceUnit(self, au):
        if not isinstance(au, list):
            return au
        if len(au[1]) == 0:
            return au

        # if 'g' in au[1]:
        #     x = bytearray(au[1], encoding='utf-8')
        #     if len(x) > 1:
        #         print(f'{len(x):2>}: {au[1]}')
        au1_lower = au[1].strip().lower()
        if au1_lower in ['cc', 'c.c', 'c.c.', 'ml', 'mls', 'ML', 'mI', '毫升', 'cc or不加', 'ml左右']:
            au[1] = 'ml'
        if au1_lower in ['g', '克', '公克', 'g/斤', '克g', '克左右']:
            au[1] = 'g'

        if isinstance(au[0], str):
            return au

        for cvt in self._unitCvt:
            for key in cvt['keys']:
                if au1_lower == key:    # Note: Should be exactly
                    return [au[0]*cvt['val'], cvt['unit']]
        # else:
        #     return au

        # if au[1] != 'g' and au[1] != 'ml' and len(au[1]) > 2:
        #     print('1')
        return au


    # Class Method
    def clean(self, id, qtyStr, bVerb=False):
        # key: ingredent, value: qty. + unit string
        if bVerb: print(f'{id:>8}: {qtyStr} -> ', end='')
        if len(qtyStr) == 0:    return qtyStr
        qtyStr = self._cvtStr(qtyStr)
        qtyStr = self._cvtNumStr(qtyStr)
        qtyStr = qtyStr.replace('又', '+')
        qtyStr = qtyStr.replace('～', '~')
        qtyStr = qtyStr.replace('—', '-')
        qtyStr = qtyStr.replace('－', '-')
        qtyStr = qtyStr.replace(' - ', '-')
        qtyStr = qtyStr.replace(' ~ ', '~')
        if '分之' in qtyStr:
            qtyStr = re.sub(r'([0-9]+)分之([0-9]+) *', r'\2/\1', qtyStr)

        # if id =='262188':
        #     print('1')
        try:
            qty_unit = self._replaceUnit(self._splitUnit(qtyStr))
        except Exception as er:
            qty_unit = qtyStr
            print(f'{id:>8}: qty-unit parse error.')
        if bVerb: print(f'{qty_unit}')
        return qty_unit

