import requests
from bs4 import BeautifulSoup

r = requests.get("http://www.econostatistics.co.za/MineralsHTMJava.asp?fname=index.html")
soup = BeautifulSoup(r.content)

for scr in soup.find_all("script"):
    if scr.text.lower().find("oil") >= 0:
        arr = [x.strip() for x in scr.text.split("\n")]

oil = []
for i in ar:
    try:
        ind = i.index("JLo")
    except ValueError:
        ind = 1
    if not ind:
        oil.append(i)

f = open("oil-data1.txt", "wb")
f.write(bytes("\n".join(oil), "UTF-8"))
f.close()
