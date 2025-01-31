from re import sub, split
from datetime import datetime
from html import unescape as unhtmlescape

def unix_time(time_str):
    dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    return int(dt.timestamp())

def flatten(_list: list):
    return [xi for i in _list for xi in i["list"]]

def find(_list: list, func):
    return next(filter(func, _list), None)

def splitbylength(text: str, length: int):
    s = split(r'(.+?[！。\n])', text)
    _list = []
    _t = ""
    if len(text) < 1024:
        return [text]
    else:
        for i in list(range(len(s))):
            if len(_t) + len(s[i]) > length:
                _list.append(_t)
                _t = ""
            _t += s[i]
        if _t: _list.append(_t)
        return _list

def embUrl(text: str):
    return sub(r'<a href=".*?\(\'(.+?)\'\);"\s*.*?>(.+?)</a>', "\n\n[\\2](\\1)\n", text) # embed url
