from re import findall, sub
from html import unescape as unhtmlescape

path = "README.md"

def fetch() -> int:
    with open(path, "r", encoding="utf-8") as f:
        readme = f.read()
    latest = findall(r'<id latest="(\d+?)">', readme)[0]
    return int(latest)

def save(unixtime: int, content: dict):
    with open(path, "r", encoding="utf-8") as f:
        readme = f.read()
    readme = sub(r'<id latest="\d+?">', f'<id latest="{unixtime}">', readme)
    html = unhtmlescape(content["content"])
    readme = sub(r'<start>\n*[\s\S]*?\n*<end>', f'<start>\n\n### {content["title"]}\n<img src="{content["banner"]}">\n{html}\n\n<end>', readme)
    with open(path, "w", encoding="utf-8") as f:
        f.write(readme)
