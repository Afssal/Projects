# from bs4 import BeautifulSoup
# import cloudscraper
# from tqdm import tqdm
# from sqlalchemy import create_engine
# from sqlalchemy.engine import URL
# from sqlalchemy import Column,Integer,String,Text,DateTime,Float
# from sqlalchemy.orm import declarative_base
# from datetime import datetime
# from sqlalchemy.orm import sessionmaker



# scraper = cloudscraper.create_scraper()


# url = URL.create(
#     drivername='postgresql',
#     username="postgres",
#     password=12345,
#     host="localhost",
#     port=5432,
#     database="MoviesData"
# )

# engine = create_engine(url)

# connection = engine.connect()


# Base = declarative_base()


# class Movies(Base):

#     __tablename__ = "movies"


#     id = Column(Integer(),primary_key=True)
#     title = Column(Text)
#     country = Column(Text)
#     rating = Column(Float)
#     content = Column(Text)


# Base.metadata.create_all(engine)


# Session = sessionmaker(bind=engine)
# session = Session()


# MainUrl = 'https://mydramalist.com/'


# start = 1
# end = 251

# def GetData(url):
    
#     response = scraper.get(url)
#     soup = BeautifulSoup(response.text,'html.parser')
#     return soup

# for i in tqdm(range(start,end)):

#     url = f'https://mydramalist.com/movies/top?page={i}'

#     soup = GetData(url)

#     getlink = soup.find_all('a',class_='block')

#     for mlink in getlink:

#         sublink = MainUrl + mlink['href']

#         soup = GetData(sublink)

#         title = soup.find('h1',class_='film-title').text

#         rating = soup.find('div',class_='box deep-orange').text

#         country_grand = soup.find('div',class_='box-body light-b')

#         country = country_grand.findAll('li',class_='list-item p-a-0')
#         temp = country[3].text
#         country = temp.split(':')[1].strip()
#         grandparent = soup.find('div',class_='show-synopsis')
#         if grandparent:
#             parent = grandparent.find('p')
#             content = parent.find('span').text
        
#         data = Movies(title=title,country=country,rating=rating,content=content)
#         session.add(data)
#         session.commit()


from bs4 import BeautifulSoup
import cloudscraper
from tqdm import tqdm
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import Column, Integer, Text, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

scraper = cloudscraper.create_scraper()

url = URL.create(
    drivername='postgresql',
    username="postgres",
    password="12345",
    host="localhost",
    port=5432,
    database="MoviesData"
)

engine = create_engine(url)
connection = engine.connect()

Base = declarative_base()

class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer(), primary_key=True)
    title = Column(Text)
    country = Column(Text)
    rating = Column(Float)
    content = Column(Text)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

MainUrl = 'https://mydramalist.com/'

start = 1
end = 251

def GetData(url):
    try:
        response = scraper.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except Exception as e:
        print(f"[ERROR] Failed to fetch {url} -> {e}")
        return None

for i in tqdm(range(start, end)):
    url = f'https://mydramalist.com/movies/top?page={i}'
    soup = GetData(url)
    if not soup:
        continue

    getlink = soup.find_all('a', class_='block')

    for mlink in getlink:
        try:
            sublink = MainUrl + mlink['href']
            soup = GetData(sublink)
            if not soup:
                continue

            # Extract fields safely
            title = soup.find('h1', class_='film-title')
            title = title.text.strip() if title else "Unknown"

            rating = soup.find('div', class_='box deep-orange')
            try:
                rating = float(rating.text.strip()) if rating else None
            except ValueError:
                rating = None

            country = None
            country_grand = soup.find('div', class_='box-body light-b')
            if country_grand:
                country_items = country_grand.findAll('li', class_='list-item p-a-0')
                if len(country_items) >= 4:
                    temp = country_items[3].text
                    if ':' in temp:
                        country = temp.split(':')[1].strip()

            content = None
            grandparent = soup.find('div', class_='show-synopsis')
            if grandparent:
                parent = grandparent.find('p')
                if parent:
                    span = parent.find('span')
                    content = span.text.strip() if span else None

            # Save to DB
            data = Movies(title=title, country=country, rating=rating, content=content)
            session.add(data)

        except Exception as e:
            print(f"[ERROR] While parsing {sublink} -> {e}")

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"[ERROR] Commit failed on page {i}: {e}")


    