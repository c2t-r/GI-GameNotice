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
    return sub(r'<a href=".*?\(\'(.+?)\'\);">(.+?)</a>', "[\\2](\\1)", text) # embed url

def unHtml(html):
    unhtml = html
    unhtml = embUrl(unhtml)
    unhtml = sub(r'<[^\/]+?\s.*?>', "", unhtml)
    unhtml = sub(r'(<\/.*?>)+', "\n", unhtml)
    unhtml = sub(r'\\n(\\n)+', "\n", unhtml)
    unhtml = sub(r'&lt;.*?&gt;', "", unhtml) # unrich text
    unhtml = sub(r'〓\n', "〓\n\n", unhtml)
    unhtml = sub(r'\n〓', "\n\n〓", unhtml)
    unhtml = unhtml.replace("<br>", "\n")
    unhtml = unhtmlescape(unhtml)
    return unhtml