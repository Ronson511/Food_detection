import os, re

mod_path = os.path.relpath(os.path.dirname(__file__))
ipath = os.path.join(mod_path, 'images/')

class imgCounter():
    _rgx1 = re.compile(r'([0-9]+)\..*')     # filename match
    _rgx2 = re.compile(r'^image/(.*)')      # content_type
    def __init__(self, path) -> None:
        self._path = str(path)
        flist = [int(self._rgx1.search(file).group(1)) for file in os.listdir(path) if self._rgx1.search(file)]
        self.counter = max(flist)+1 if len(flist) > 0 else 0

    def _getNext(self, n: int):
        ret = self.counter
        self.counter += 1
        fstr = f'{{:>0{n}d}}'
        return self._path+fstr.format(ret)

    def _getExt(self, ctx_type: str):
        mat = self._rgx2.search(ctx_type)
        if mat:
            return mat.group(1)
        else:
            return 'jpg'

    def getName(self, n: int, ctx_type: str):
        return self._getNext(3)+'.'+self._getExt(ctx_type)

