from bs4 import BeautifulSoup as bs4
import requests
url = "https://in.linkedin.com/jobs/search?keywords="

key = ["HTML","CSS","JAVASCRIPT","PYTHON","JAVA","GO","BASH","data","software-developement-intern","networking-intern","machinelearning-datascience-intern"]

python_url = url+"software-developement-intern"

html = requests.get(python_url).text
soup = bs4(html, "lxml")
links =[]
for ultag in soup.find_all('ul', {'class': 'jobs-search__results-list'}):
    for litag in ultag.find_all('li'):
        for atag in ultag.find_all('a'):
           links.append(atag.get('href'))

print(python_url , len(links))