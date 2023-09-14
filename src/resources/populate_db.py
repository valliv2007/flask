from concurrent.futures.process import ProcessPoolExecutor
from datetime import datetime
from pickle import TRUE
import bs4
import requests
import threading
from flask_restful import Resource

from src.services.film_service import FilmService
from src import db


def convert_time(time):
    hour = time[0]
    minute = time[6:].lstrip()[:2]
    return (60 * int(hour) + int(minute.strip('m')))


class PopulateDB(Resource):
    url = 'https://www.kinoafisha.info/'

    @staticmethod
    def populate_db(films):
        return FilmService.bulk_create(db.session, films)

    def post(self):
        t0 = datetime.now()
        films_urls = self.get_films_urls()
        films = self.parse_films(films_urls)
        created_films = self.populate_db(films)
        dt = datetime.now() - t0
        print(round(dt.total_seconds(), 2))
        return {'message': f'DB were populated with {created_films}'}, 201

    def get_films_urls(self):
        print('Getting films from urls', flush=True)
        url = self.url + 'rating/movies/'
        resp = requests.get(url)
        resp.raise_for_status()
        html = resp.text
        soup = bs4.BeautifulSoup(html, features='html.parser')
        movie_containers = soup.find_all(
            'div',
            class_='movieItem_info')
        movie_links = [movie.a.attrs['href'] for movie in movie_containers][27:55]
        return movie_links
    
    def parse_films(self, films_urls):
        films = []
        print(films_urls)
        for url in films_urls:
            print(f'Get film from {url}')
            film_content = requests.get(url)
            film_content.raise_for_status()
            html = film_content.text
            soup = bs4.BeautifulSoup(html, features='html.parser')
            title, release_date = soup.find('h1', class_="trailer_title").text.split(', ')
            rating = float(soup.find('span', class_="rating_num").text)
            description = soup.find('div', class_="visualEditorInsertion filmDesc_editor more_content").text.strip()
            length = convert_time(soup.find('span', class_="filmInfo_infoData").text.strip())
            print(f'recived information about {title}', flush=True)
            films.append(
                {'title': title, 'rating': rating, 'description': description, 
                 'release_date': datetime.strptime(release_date.strip(), '%Y'),
                 'length': length, 'distributed_by': 'Warner Bros.'})
        return films


class PopulateDBThread(PopulateDB):
    def post(self):
        threads = []
        films_to_create = []
        t0 = datetime.now()
        films_urls = self.get_films_urls()
        for url in films_urls:
            threads.append(threading.Thread(target=self.parse_films, args=(url, films_to_create), daemon=True))
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
        created_films = self.populate_db(films_to_create)
        dt = datetime.now() - t0
        print(round(dt.total_seconds(), 2))
        return {'message': f'DB were populated with {created_films}'}, 201
    
    def parse_films(self, url, films_to_create):
        print(f'Get film from {url}')
        film_content = requests.get(url)
        film_content.raise_for_status()
        html = film_content.text
        soup = bs4.BeautifulSoup(html, features='html.parser')
        title, release_date = soup.find('h1', class_="trailer_title").text.split(', ')
        rating = float(soup.find('span', class_="rating_num").text)
        description = soup.find('div', class_="visualEditorInsertion filmDesc_editor more_content").text.strip()
        length = convert_time(soup.find('span', class_="filmInfo_infoData").text.strip())
        print(f'recived information about {title}', flush=True)
        films_to_create.append(
            {'title': title, 'rating': rating, 'description': description, 
             'release_date': datetime.strptime(release_date.strip(), '%Y'),
             'length': length, 'distributed_by': 'Warner Bros.'})
        return films_to_create


class PopulateDBThreadPool(PopulateDB):
    def post(self):
        t0 = datetime.now()
        films_urls = self.get_films_urls()
        works = []
        with ProcessPoolExecutor() as executor:
            for url in films_urls:
                f = executor.submit(self.parse_films, url)
                works.append(f)
        films_to_create = [f.result() for f in works]
        created_films = self.populate_db(films_to_create)
        dt = datetime.now() - t0
        print(round(dt.total_seconds(), 2))
        return {'message': f'DB were populated with {created_films}'}, 201
 
    def parse_films(self, url):
        print(f'Get film from {url}', flush=True)
        film_content = requests.get(url)
        film_content.raise_for_status()
        html = film_content.text
        soup = bs4.BeautifulSoup(html, features='html.parser')
        title, release_date = soup.find('h1', class_="trailer_title").text.split(', ')
        rating = float(soup.find('span', class_="rating_num").text)
        description = soup.find('div', class_="visualEditorInsertion filmDesc_editor more_content").text.strip()
        length = convert_time(soup.find('span', class_="filmInfo_infoData").text.strip())
        print(f'recived information about {title}', flush=True)
        return {'title': title, 'rating': rating, 'description': description,
                'release_date': datetime.strptime(release_date.strip(), '%Y'),
                'length': length, 'distributed_by': 'Warner Bros.'}