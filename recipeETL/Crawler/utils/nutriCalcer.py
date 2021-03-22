from utils.txt_loader  import dict_csvloader
import numpy as np

class nutriCalcer():
    def __init__(self):
        self._nutriTbl, self._headers = dict_csvloader('./utils/nutrition.csv')

    def _lookup(self, ingred):
        return self._nutriTbl[ingred]

    def calc(self, std_ingreds):
        data = np.zeros((19,), dtype=np.float32)
        for ingred, qty in std_ingreds.items():
            # if ingred == '胡蘿蔔':
            #     print('1')
            vary = self._lookup(ingred)
            if qty[1] == 'g' or qty[1] == 'ml':
                data = data + vary * np.float32(qty[0] / 100)
            else:
                print(f'Error: qty Unit not allowed.')
            # for v in self._lookup(ingred):
            #     data[i] += v*qty/100
            # data = [v*qty/100 for v in self._lookup(ingred)]
        return data
