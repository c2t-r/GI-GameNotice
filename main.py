import asyncio
from time import sleep
import datetime
import json
import requests
from game import game


def sendDiscord(webhook_url, content: dict):
    response = requests.post(webhook_url, data=json.dumps(content), headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
    })
    return response


with open("settings.json", "r") as f:
    settings = json.load(f)


def main(settings):
    now = datetime.datetime.now()
    timeStr = now.isoformat(" ", timespec="seconds")

    print(timeStr, f'running {settings["name"]}')
    status, content = asyncio.run(game(settings))

    if not status:
        print(timeStr, "something failed...")

    if content:
        with open("commit.txt", "w", encoding="utf-8") as f:
            f.write(
                f'{len(content)} new announcement{"s" if len(content) > 1 else ""} added')

    for i in content:
        response = sendDiscord(settings["webhook"], i)
        print(timeStr, response)
        if not response.ok:
            print(response.text)
            print(json.dumps(i, indent=2, ensure_ascii=False))
        sleep(5)


main(settings)
