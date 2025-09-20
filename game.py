from requests import get
from markdownify import markdownify as md
from re import sub
import util
import data

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
}


async def game(settings) -> tuple[bool, list[dict]]:
    name = settings["name"]
    lang = settings["language"]
    repo = settings["repo"]

    url = f'https://sg-hk4e-api.hoyoverse.com/common/hk4e_global/announcement/api/getAnnList?game=hk4e&game_biz=hk4e_global&lang={lang}&bundle_id=hk4e_global&level=60&platform=pc&region=os_usa&uid=1'
    response = get(url, headers=header)
    if not response:
        print(f'{name} failed.')
        return False, []
    list_obj = response.json()

    ann_list = sorted(util.flatten(list_obj["data"]["list"]), key=lambda x: util.unix_time(
        x["start_time"]), reverse=True)

    ann_list = [i for i in ann_list if not data.hasAnn(i)]
    if not ann_list:
        return True, []

    url = f'https://sg-hk4e-api-static.hoyoverse.com/common/hk4e_global/announcement/api/getAnnContent?game=hk4e&game_biz=hk4e_global&lang={lang}&bundle_id=hk4e_global&platform=pc&region=os_asia&level=1'
    response = get(url, headers=header)
    if not response:
        print(f'{name} failed.')
        return False, []
    content_obj = response.json()
    content_list = content_obj["data"]["list"]

    contents = []
    added_list = []
    for ann in ann_list:
        print(f'new announcement {ann["ann_id"]} found. {ann["title"]}')
        embed = {
            "color": 0x38f4af,
            "title": ann["title"],
            "image": {
                "url": ann["banner"]
            },
            "timestamp": ann["start_time"]
        }
        ann_content = util.find(
            content_list, lambda x: x["title"] == ann["title"])

        if ann_content:
            embed["title"] = ann_content["title"]
            embed["url"] = f'https://github.com/{repo}/tree/main/log/{ann["ann_id"]}.md'
            embed["image"]["url"] = ann_content["banner"]
            embed["fields"] = []

            data.update(ann["ann_id"], ann_content)

            added_list.append(
                f'[{ann_content["title"]}](log/{ann_content["ann_id"]}.md)')

            text = util.embUrl(ann_content["content"])
            text = md(text)
            text = util.removeTTag(text)
            splitcontent = util.splitbylength(text, 1000)
            for s in splitcontent[:3]:  # embed size limit? idk
                embed["fields"].append({"name": "", "value": s})
            if len(splitcontent) > 3:
                embed["fields"].append(
                    {"name": "", "value": f'[see more...]({f'https://github.com/{repo}/tree/main/log/{ann["ann_id"]}.md'})'})
        else:
            print("it doesn't match any content.")
            raise KeyError()  # for now
        contents.append(
            {"username": f'{name} No.{ann["ann_id"]}', "embeds": [embed]})

    if added_list:
        with open("README.md", "r", encoding="utf-8") as f:
            readme = f.read()
        announcements = "  \n".join(added_list)
        readme = sub(r'## Recent Announcements\n*[\s\S]*?\n*<end>',
                     f'## Recent Announcements\n{announcements}\n<end>', readme)
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme)

    return True, contents[::-1]
