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

def main(m):
    now = datetime.datetime.now()
    timeStr = now.isoformat(" ", timespec="seconds")

    print(timeStr, f'running {m["name"]}')
    status, content = asyncio.run(game(m["name"]))

    if not status:
        print(timeStr, f'failed to run {m["name"]}')

    for i in content:
        response = sendDiscord(m["webhook"], i)
        print(timeStr, response)
        if not response.ok:
            print(i)
        sleep(5)

main(settings)
