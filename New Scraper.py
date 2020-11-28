#New CNN Fear Greed Scraper

import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

#defining a function to transform the output of the scrape into a list to insert into a dataframe
def extract(lst):
    return [[el] for el in lst]

#function for scraping the Fear & Greed Index values from CNN and storing into a df
def scrapefgi():
    page = requests.get('https://money.cnn.com/data/fear-and-greed') #fear&greed website
    soup = BeautifulSoup(page.content, 'html.parser')
    uls = soup.find(id='needleChart') #the html object of interest
    d = [] #creating an empty list for the values
    #looping throug the html to extract the html phrases information of interest
    for ul in uls:
        newsoup = BeautifulSoup(str(ul), 'html.parser')
        lis = newsoup.find_all('li') 
        for li in lis:
        #print(li.text)
            d.append(li.text)
        #trimming off the html <>'s from the information

    #print(d[0][18:20])
    #print(d[1][29:31])
    #print(d[2][25:28])
    #print(d[3][26:29])
    #print(d[4][25:27])
    d[0] = d[0][18:20]
    d[1] = d[1][29:31]
    d[2] = d[2][25:27]
    d[3] = d[3][26:28]
    d[4] = d[4][25:27]
#print(extract(d))
    d = extract(d)

#df = DataFrame(d, columns=['Today','Yesterday','Week','Month','Year'])
#print(df)
    df = DataFrame(d).T
#df = DataFrame(d, columns=['Today','Yesterday','Week','Month','Year'])
    df.columns = ['Today','Yesterday','Week','Month','Year']



import sqlite3
conn = sqlite3.connect('fgi.db')
df.to_sql('CNN_FGI', con = conn, if_exists = 'append')
conn.commit()
conn.close()

import datetime


def dynamic_data_entry():
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(
        unix).strftime('%Y-%m-%d %H:%M:%S'))
    keyword = 'Python'
    value = random.randrange(0, 10)
    c.execute("INSERT INTO stonkdata (unix, datestamp, keyword, value) VALUES (?, ?, ?, ?)",
              (unix, date, keyword, value))
    conn.commit()





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

