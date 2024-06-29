from re import findall, sub

path = "README.md"

def fetch() -> int:
    with open(path, "r", encoding="utf-8") as f:
        readme = f.read()
    latest = findall(r'<id latest="(\d+?)">', readme)[0]
    return int(latest)

def save(unixtime: int, title: str, notice: str):
    with open(path, "r", encoding="utf-8") as f:
        readme = f.read()
    readme = sub(r'<id latest="\d+?">', f'<id latest="{unixtime}">', readme)
    readme = sub(r'<start>\n*[\s\S]*?\n*<end>', f'<start>\n\n### {title}\n{notice}\n\n<end>', readme)
    with open(path, "w", encoding="utf-8") as f:
        f.write(readme)
