import pandas as pd
import requests
from bs4 import BeautifulSoup
index = 1
notFound = 'No Results Found'

car_link = []
while (True):
    url = "https://www.one2car.com/en/used-cars-for-sale/toyota/hilux-revo?page_number=" + \
        str(index) + "&page_size=50"
    r = requests.get(url)
    index += 1
    soup = BeautifulSoup(r.content, "html.parser")
    header = soup.find('h1', {'class': 'headline'})
    if(notFound in header.text):
        break

    data = soup.find_all("a",  {'class': 'js-ellipsize-text'})
    for i in data:
        car_link.append(i['href'])

carList = []
k = 0
for link in car_link:
    print(link, end='\n')
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    details = soup.find_all('div', {'class': 'list-item'})
    listprice = soup.find('div', {'class': 'listing__price'}).text
    car = {
        'URL': link,
        'List Price': listprice
    }
    for detail in details:

        index = detail.find('span', {'class': 'text--muted'})
        value = detail.find('span', {'class': 'float--right'})
        index1 = detail.find('span', {'class': 'text--left'})
        value1 = detail.find('span', {'class': 'text--right'})
        if(index != None and value != None):
            car[index.text] = value.text
            index = None

        if(index1 != None and value1 != None):
            car[index1.text] = value1.text
            index1 = None
    carList.append(car)
    print(k)
    k += 1


df = pd.DataFrame(carList)

df.to_csv('Hilux_revo.csv', index=False)
