from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def getsources(article):
    html = urlopen("https://en.wikipedia.org/w/index.php?title=Special:WhatLinksHere/" + article + "&limit=1000")
    bsObj = BeautifulSoup(html, "html.parser")
    thislinks = bsObj.find("div", {"id": "mw-content-text"}).findAll("li")
    sources = []
    for thislink in thislinks:
        sources.extend(thislink.findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")))
    clean = []
    for source in sources:
        clean.append(source.attrs["href"])
    return clean

inf = open('Entity List.txt')
for counter, line in enumerate(inf):
    strs = line.strip().split('\t')
    ents = strs[1:]
    print(ents)
    entity1ist = [[],[],[],[],[],[],[],[],[],[]]
    frequencydic = dict()
    for el in range(10):
        entity1ist[el] = getsources(ents[el].replace(' ','_'))
        for link in entity1ist[el]:
            if link not in frequencydic:
                frequencydic[link] = 1
            else:
                frequencydic[link] = frequencydic[link] + 1
    common = {k: v for k, v in frequencydic.items() if v >= 3}
    print(common)
    file = open(str(counter) + ".txt", "w",encoding='utf-8')
    count = 0
    for c in common:
        html1 = urlopen("https://en.wikipedia.org" + c)
        bsObj1 = BeautifulSoup(html1, "html.parser")
        alllinks = [[], [], [], [], [], [], [], [], [], []]
        links = bsObj1.find("div", {"id": "bodyContent"}).findAll("p")
        for link in links:
            for i in range(10):
                alllinks[i].extend(link.findAll("a", href="/wiki/" + ents[i].replace(' ','_')))
        articleflag = False
        for i in range(10):
            if len(alllinks[i]) != 0:
                articleflag = True

        if articleflag:
            file.write("Article: " + c.split("/")[-1].replace('_', ' ') + "\n")
            for i in range(10):
                if len(alllinks[i]) != 0:
                    for alllink in alllinks[i]:
                        file.write(ents[i] + "\t" + alllink.string + "\t")
                        for string in alllink.parent.strings:
                            file.write(string)
    #file.close()

