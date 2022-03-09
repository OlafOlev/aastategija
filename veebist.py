from bs4 import BeautifulSoup
import requests
import json
url = 'http://192.168.22.172/menu-example/'
r = requests.get(url)
doc = BeautifulSoup(r.text, "html.parser")
info = doc.find_all("h2")
u = 0
stats = []
#Scrapime infot veebilehelt, et leida kõik erinevad toidud/joogid ja panna neid ühte listi.
for sooke in info[:-1]:
    parent = info[u].parent
    for i in parent:
        stats.append([i.contents[0], i.contents[1].text.replace("\u20ac", ""), i.contents[3].text])
    u += 1
# Teeme JSON faili.
json_data = []
info2 = doc.find_all("h3")
a = 0
pealkirjad = []
# Loeme kokku kõik pealkirjad ja lisame JSON faili toidugruppide pealkirjad.
for pealkiri in info2:
    pealkirjad.append(pealkiri.contents[0].text)
    json_data.append({"nimetus": pealkirjad[a], "toidud": []})
    a += 1
b = 0
j = 0
i = 0
# Lisame JSON faili iga pealkirja juurde vastavad toidud.
while b <= a-1:
    info3 = info2[b].parent.parent.find_all("h2")[:-1]
# Loeme kokku, kui palju toite on antud pealkirjas.
    for toiduud in info3:
        j += 1
# Lisame konkreetsed toidud vastavatesse toidugruppidesse.
    while i <= j:
        stats2 = list(stats[i])
        json_data[b]["toidud"].append({"nimetus": f"{stats2[0]}", "hind": f"{stats2[1]}", "lisainfo": f"{stats2[2]}"})
        i += 1
        with open('json', 'w') as f:
            json.dump(json_data, f, indent=5)
    b += 1
    j += 1