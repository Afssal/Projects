from bs4 import BeautifulSoup
import requests
import cloudscraper


scraper = cloudscraper.create_scraper()
url = f'https://mydramalist.com/movies/top?page=1'
MainUrl = 'https://mydramalist.com/'

response = scraper.get(url)
soup = BeautifulSoup(response.text,'html.parser')
# print(soup)

lin = soup.find_all('a',class_='block')
for l in lin:
    new = MainUrl + l['href']
    response = scraper.get(new)
    soup = BeautifulSoup(response.text,'html.parser')
    title = soup.find('h1',class_='film-title').text
    rating = soup.find('div',class_='box deep-orange').text
    country_grand = soup.find('div',class_='box-body light-b')
    # country_parent = country_grand.find('ul',class_='list m-b-0')
    country = country_grand.findAll('li',class_='list-item p-a-0')
    temp = country[3].text
    country = temp.split(':')[1].strip()
    grandparent = soup.find('div',class_='show-synopsis')
    if grandparent:
        parent = grandparent.find('p')
        content = parent.find('span').text
    # print(title)
    # print(rating)
    print(country)
    # print(content)

# print(lin)

# print(soup.find_all('div',class_='box-body'))
# print(lin['href'])
