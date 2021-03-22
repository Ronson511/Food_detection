import re
from .typoSyn import *

class ingredCleaner():
    def __init__(self):
        pass

    _typoDict = TypoSyn()
    _engTrans = EngSynonym()
    _zhcnTrans = ZhcnSynonym()

    # (...)?xxx(...)
    _rgx1 = re.compile(r'([(\[].*?[)\]])?\s*(.+?)\s*([(\[].*?[)\]])')
    # (...)xxx(...)?
    _rgx2 = re.compile(r'([(\[].*?[)\]])\s*(.+)\s*([(\[].*?[)\]])?')
    # Clean 'xx(~', '~)xx'
    # Disable some of _rgx3? due to using and exclude list of processing
    # _rgx3a = re.compile(r'^((?:7|7-|7-ELEVEN)11|7-ELEVEN)\s?', re.I)
    # _rgx3b = re.compile(r'^(.) {1,3}(.)$')
    # _rgx3c = re.compile(r'^([.\]、]|[1-9]：)')
    _rgx3d = re.compile(r'^[1-9]([^號吋層塊砂\x00-\xff].*)')
    _rgx3e = re.compile(r'^(小?蘇打粉?)$')
    _rgx4 = re.compile(r'(.+[：︰～]|[a-j1-9][.:\-])\s*(.+)', re.I)
    _rgx5 = re.compile(r'(.+)\s*\(.*')
    _rgx6 = re.compile(r'.+\)\s*(.+)')


    # Class Method
    def clean(self, id, vstr, bVerb=False, nClean=4):

        # Regex executer with log flag
        def _doRegex(rgx, vstr, bVerb=False):
            mat = rgx.match(vstr)
            if mat:
                if bVerb: print(f"{id:>8}, {mat.groups()}")
            return mat


        ## 處理程序
        # Part0: 簡中 --> 繁中
        def _cleanIng0(vstr):
            # 處理符號含全型半型...
            vstr = self._zhcnTrans.parseSymbol(vstr)
            vstr = self._zhcnTrans.parseWord(vstr)
            # 英轉中, 刪 食材字串 裡的重覆
            vstr = self._engTrans.replaceTran(vstr)
            return vstr

        # Part1: 處理有 () 的
        def _cleanIng1(vstr):
            mat = _doRegex(self._rgx1, vstr, bVerb)
            if mat: return mat.group(2)
            mat = _doRegex(self._rgx2, vstr, bVerb)
            if mat: return mat.group(2)

            return vstr

        # Part2: 處理 奇奇怪怪 的
        def _cleanIng2(vstr):
            # for i, x in enumerate([self._rgx3a, self._rgx3b, self._rgx3c, self._rgx3a]):
            #     xtmp = re.search(x, vstr)
            #     if xtmp:
            #         print(f'{id:>8}, {vstr}, {i}: {xtmp.group(1)}')
            # vstr = self._rgx3a.sub('[7-11] ', vstr)
            # vstr = self._rgx3b.sub(r'\1\2', vstr)
            # vstr = self._rgx3c.sub('', vstr)
            vstr = self._rgx3d.sub(r'\1', vstr)
            # 蘇打粉 --> 小蘇打粉
            if '蘇打' in vstr:
                # if id == '119465':
                #     print('1')
                vstr = self._rgx3e.sub(r'小蘇打粉', vstr)

            mat = _doRegex(self._rgx4, vstr, bVerb)
            if mat: return mat.group(2)
            mat = _doRegex(self._rgx5, vstr, bVerb)
            if mat: return mat.group(1)
            mat = _doRegex(self._rgx6, vstr, bVerb)
            if mat: return mat.group(1)

            return vstr


        # 處理符號含全型半型, 簡中 --> 繁中...
        nClean -= 1
        if nClean < 0:      return vstr
        vstr = _cleanIng0(vstr)

        # Part1: 處理有 () 的
        nClean -= 1
        if nClean < 0:      return vstr
        vstr = _cleanIng1(vstr)

        # Part2: 處理 奇奇怪怪 的
        nClean -= 1
        if nClean < 0:      return vstr
        vstr = _cleanIng2(vstr)

        # 錯別字合併 類似 食材字串
        nClean -= 1
        if nClean < 0:      return vstr
        return self._typoDict.replaceTypo(vstr.strip())


    # Class Method
    _skipA = set()
    _skipB = set()
    _skipC = set()
    _skipA_list = ["胡椒", "黑椒", "鹽", "蔥", "雞粉", "水"]
    def checkSkip(self, id, food, qty, bVerb=False):
        # if '小烤箱椰奶用量' in food:
        #     print(f'{id:>8}, {food}, {qty}')
        if isinstance(qty, list):
            return 0
        if qty == '' or qty == '-'or qty == '如下':
            self._skipC.add(id)
            if bVerb: print(f'{id:>8}, {food}, {qty}')
            return 1
        # if "、" in food:
        if "少許" in qty:
            if bVerb: print(f"{id:>8}, {food}, {qty}")
            self._skipA.add(id)
            return 2
        elif "適量" in qty:
            if bVerb: print(f"{id:>8}, {food}, {qty}")
            self._skipB.add(id)
            return 3
        return 0

    # Class Method
    def getSkip(self):
        return self._skipA, self._skipB, self._skipC
