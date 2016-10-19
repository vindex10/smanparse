import json
import os

path = "data/"
skip = 4

res = list()

def fskip(f, num):
    for _ in range(num):
        next(f)

for f in os.listdir(path):
    local = dict()
    fullpath = path + f
    if not os.path.isfile(fullpath) or f.startswith("."):
        continue
    file = open(fullpath, "r")

    fskip(file, 1)
    buf = file.readline()
    local.update({"name": buf.split("=")[1]})

    buf = file.readline()
    local.update({"ts": int(buf.split("=")[1].strip())})

    fskip(file, 1)

    data = json.loads(file.readline())["windows"]
    tabs = list()
    for win in data:
        tabs = tabs + win["tabs"]
    data = [{key: tab["entries"][0][key] for key in ("title", "url")} for tab in tabs]
    local.update({"data": data})
    file.close()

    res.append(local)

res.sort(key=lambda x: x["ts"], reverse=True)

output = open("output/articles.html", "w")
s = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Articles</title>
    </head>
    <body>
    <h1>Articles I like</h1>
    """
output.write(s)

for item in res:
    s = "<H3>"+item["name"]+"</H3>\n<ul>"
    for ent in item["data"]:
        s += "\t<li><a href=\""+ent["url"]+"\">"+ent["title"]+"</a></li>\n"
    s += "</ul>\n"
    output.write(s)

s = """
    </body>
    </html>
    """
output.write(s)
output.close()
