import requests
from re import sub, split
from datetime import datetime
from html import unescape as unhtmlescape
import data

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

def unHtml(html):
    unhtml = html
    unhtml = sub(r'<a href=".*?\(\'(.+?)\'\);">(.+?)</a>', "[\\2](\\1)", unhtml) # embed url
    unhtml = sub(r'<[^\/]+?\s.*?>', "", unhtml)
    unhtml = sub(r'(<\/.*?>)+', "\n", unhtml)
    unhtml = sub(r'\\n(\\n)+', "\n", unhtml)
    unhtml = sub(r'&lt;.*?&gt;', "", unhtml) # unrich text
    unhtml = sub(r'〓\n', "〓\n\n", unhtml)
    unhtml = sub(r'\n〓', "\n\n〓", unhtml)
    unhtml = unhtml.replace("<br>", "\n")
    unhtml = unhtmlescape(unhtml)
    return unhtml

async def game(name) -> tuple[bool, list[dict]]:
    lang = "ja"
    gid = "hk4e"

    today = datetime.now()
    header = {
        "x-rpc-timezone": "Etc/GMT-9",
        "x-rpc-client_type": "4",
        "x-rpc-language": lang,
        "x-rpc-weekday": str(today.day),
        "x-rpc-hour": str(today.hour),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }

    url = f'https://sg-{gid}-api.hoyoverse.com/common/{gid}_global/announcement/api/getAnnList?game={gid}&game_biz={gid}_global&lang={lang}&bundle_id={gid}_global&level=60&platform=pc&region=os_usa&uid=1'
    response = requests.get(url, headers=header)
    if not response:
        print(f'{name} failed.')
        return False, []
    list_obj = response.json()

    ann_list = sorted(flatten(list_obj["data"]["list"]), key=lambda x: unix_time(x["start_time"]), reverse=True)

    saved_data = data.fetch()

    ann_list = [i for i in ann_list if unix_time(i["start_time"]) > saved_data]
    if not ann_list: return True, []

    url = f'https://sg-{gid}-api-static.hoyoverse.com/common/{gid}_global/announcement/api/getAnnContent?game={gid}&game_biz={gid}_global&lang={lang}&bundle_id={gid}_global&platform=pc&region=os_asia&level=1'
    response = requests.get(url, headers=header)
    if not response:
        print(f'{name} failed.')
        return False, []
    content_obj = response.json()
    content_list = content_obj["data"]["list"]

    contents = []
    is_saved = False
    for ann in ann_list:
        embed = {
            "color": 0x38f4af,
            "title": ann["title"],
            "image": {
                "url": ann["banner"]
            },
            "timestamp": ann["start_time"]
        }
        ann_content = find(content_list, lambda x: x["ann_id"] == ann["ann_id"])
        if ann_content:
            embed["title"] = ann_content["title"]
            embed["image"]["url"] = ann_content["banner"]
            embed["fields"] = []

            if not is_saved:
                data.save(unix_time(ann_list[0]["start_time"]), ann_content["title"], unhtmlescape(ann_content["content"]))
                is_saved = True

            text = unHtml(ann_content["content"])
            for s in splitbylength(text, 1000):
                embed["fields"].append({ "name": "", "value": s })
        contents.append({ "username": name, "embeds": [embed] })


    return True, reversed(contents)
