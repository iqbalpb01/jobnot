import requests 
import pandas as pd
from itertools import zip_longest
from bs4 import BeautifulSoup as bs4
url = "https://in.linkedin.com/jobs/search?keywords="

key = ["HTML","CSS","JAVASCRIPT","PYTHON","JAVA","GO","BASH","data","software-developement-intern","networking-intern","machinelearning-datascience-intern","Web developer", "front end developer", "back end developer", "ui/ux designer", "software tester", "data analyst", "data architect", "cloud engineer", "cloud architect", "network administrator", "network engineer", "network architect", "data scientist","Systems","Designing", "testing admin ","graphic designers","content writers","digital","social media"]
data={}
for i in key:
    data_url=url+i
    html = requests.get(data_url).text
    soup = bs4(html, "lxml")
    links =[]
    for ultag in soup.find_all('ul', {'class': 'jobs-search__results-list'}):
        for litag in ultag.find_all('li'):
            for atag in ultag.find_all('a'):
                links.append(atag.get('href'))
    data[i]=links

zl = list(zip_longest(*data.values()))
df = pd.DataFrame(zl, columns=data.keys())
df.to_csv('out.csv')
