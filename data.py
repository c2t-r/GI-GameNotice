from os.path import isfile
from json import load, dump
from re import sub
from html import unescape as unhtmlescape
import util

log_path = "log.json"
readme_path = "README.md"

if not isfile(log_path):
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("{}")

def hasAnn(ann: dict) -> bool:
    with open(log_path, "r", encoding="utf-8") as f:
        log = load(f)
    if str(ann["ann_id"]) in log: return True
    else: return False

def save(ann: dict):
    with open(log_path, "r", encoding="utf-8") as f:
        log = load(f)
    log[str(ann["ann_id"])] = {
        "title": ann["title"],
        "banner": ann["banner"],
        "start_time": ann["start_time"],
        "end_time": ann["end_time"],
        "type": ann["type"]
    }
    with open(log_path, "w", encoding="utf-8") as f:
        dump(log, f, indent=2, ensure_ascii=False)

def update(content: dict):
    with open(readme_path, "r", encoding="utf-8") as f:
        readme = f.read()
    html = unhtmlescape(content["content"])
    readme = sub(r'<start>\n*[\s\S]*?\n*<end>', f'<start>\n\n### {content["title"]}\n<img src="{content["banner"]}">\n{util.embUrl(html)}\n\n<end>', readme)
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme)
