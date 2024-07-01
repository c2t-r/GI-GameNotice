from requests import get
import util
import data

async def game(name, lang) -> tuple[bool, list[dict]]:
    gid = "hk4e"

    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }

    url = f'https://sg-{gid}-api.hoyoverse.com/common/{gid}_global/announcement/api/getAnnList?game={gid}&game_biz={gid}_global&lang={lang}&bundle_id={gid}_global&level=60&platform=pc&region=os_usa&uid=1'
    response = get(url, headers=header)
    if not response:
        print(f'{name} failed.')
        return False, []
    list_obj = response.json()

    ann_list = sorted(util.flatten(list_obj["data"]["list"]), key=lambda x: util.unix_time(x["start_time"]), reverse=True)

    ann_list = [i for i in ann_list if not data.hasAnn(i)]
    if not ann_list: return True, []
    for ann in reversed(ann_list): data.save(ann)

    url = f'https://sg-{gid}-api-static.hoyoverse.com/common/{gid}_global/announcement/api/getAnnContent?game={gid}&game_biz={gid}_global&lang={lang}&bundle_id={gid}_global&platform=pc&region=os_asia&level=1'
    response = get(url, headers=header)
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
                data.update(ann_content)
                is_saved = True

            text = util.unHtml(ann_content["content"])
            for s in util.splitbylength(text, 1000):
                embed["fields"].append({ "name": "", "value": s })
        contents.append({ "username": name+f' No.{ann["ann_id"]}', "embeds": [embed] })

    return True, reversed(contents)
