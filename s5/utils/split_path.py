from collections import deque
from os.path import split

def Split_Path(sPath):
    sHead, sTail = split(sPath)
    d = deque([])
    if sTail != '':
        d = deque([sTail])
        d.extend(Split_Path(sHead))
    else:
        return d
    d.rotate(-1)
    return list(d)

