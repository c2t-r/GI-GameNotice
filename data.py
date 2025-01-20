from os.path import isfile, join as pathjoin
from os import makedirs
from html import unescape as unhtmlescape
import util

log_dir = "log"

makedirs(log_dir, exist_ok=True)

def hasAnn(ann: dict) -> bool:
    log_path = pathjoin(log_dir, f'{ann["ann_id"]}.md')
    return isfile(log_path)

def update(content: dict):
    log_path = pathjoin(log_dir, f'{content["ann_id"]}.md')
    html = unhtmlescape(content["content"])
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f'## {content["title"]}\n<img src="{content["banner"]}">\n{util.embUrl(html)}\n')
