#New Scraper

import requests
from bs4 import BeautifulSoup

page = requests.get('https://money.cnn.com/data/fear-and-greed')
soup = BeautifulSoup(page.content, 'html.parser')
uls = soup.find(id='needleChart')
d = []
for ul in uls:
    newsoup = BeautifulSoup(str(ul), 'html.parser')
    lis = newsoup.find_all('li')
    for li in lis:
        #print(li.text)
        d.append(li.text)
#print(d)
#print("======")
#l = []
#string = "Fear & Greed Now: 91 (Extreme Greed)"
#for a in d:
    #for b in ['Y','h','P','v','i','u','s','C','l','s','W','k','A','g','M','n','u','l','F','e','d','a','r','&','G','N','o','w',':','(',')','x','t','m', 'E']:
        #a = a.replace(b,"")
    #l.append(a)


#print("****************************")

#string = str(d[0])       
#for i in range(len(string)):
    #for j in ['F','e','d','a','r','&','G','N','o','w',':','(',')','x','t','m', 'E']:
        #string = string.replace(j, "")
#print(int(string))
print(d[0][18:20])
print(d[1][29:31])
print(d[2][25:28])
print(d[3][26:29])
print(d[4][25:27])

 