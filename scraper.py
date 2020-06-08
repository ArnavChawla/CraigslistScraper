import requests
import bs4
from bs4 import BeautifulSoup as soup
import json
import pygsheets
gc = pygsheets.authorize()
sh = gc.open("scraper")
wks = sh.sheet1

session = requests.Session()
r = session.get("https://losangeles.craigslist.org/search/lss?query=math+tutor&sort=rel")
bs = soup(r.text,"html.parser")
links = []

emails = []
for element in bs.findAll("a",{"class":"result-title hdrlnk"}):
    links.append(element["href"])
print(links)

for link in links:
    r = session.get(link)
    firstPart = str(link).split(".org")[0]
    #print(firstPart)
    bs = soup(r.text, "html.parser")
    id = (str(bs.find("input",{"class":"lastLink"})["value"]).split("/")[2]).split(".")[0]
    #print(id)
    reigon = (str(bs.find("a", string="post")).split("/c/")[1]).split("\"")[0]
    #print(reigon)
    newLink  = firstPart+".org/contactinfo/"+reigon+"/lss/"+id
    r = session.get(newLink)
    jso = json.loads(r.text)
    bs = soup(jso["replyContent"],"html.parser")
    try:
        emails.append(bs.find("p",{"class":"anonemail"}).text)
        print("done")
    except:

        print("error")
print(emails)
wks.update_col(3, emails)
