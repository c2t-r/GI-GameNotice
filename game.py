import requests
from datetime import datetime
import util
import data

async def game(name, lang) -> tuple[bool, list[dict]]:
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

    ann_list = sorted(util.flatten(list_obj["data"]["list"]), key=lambda x: x["ann_id"], reverse=True)

    saved_data = data.fetch()

    ann_list = [i for i in ann_list if i["ann_id"] > saved_data]
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
        ann_content = util.find(content_list, lambda x: x["ann_id"] == ann["ann_id"])
        if ann_content:
            embed["title"] = ann_content["title"]
            embed["image"]["url"] = ann_content["banner"]
            embed["fields"] = []

            if not is_saved:
                data.save(ann_list[0]["ann_id"], ann_content)
                is_saved = True

            text = util.unHtml(ann_content["content"])
            for s in util.splitbylength(text, 1000):
                embed["fields"].append({ "name": "", "value": s })
        contents.append({ "username": name+f' No.{ann["ann_id"]}', "embeds": [embed] })


    return True, reversed(contents)
