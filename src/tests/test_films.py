import http
import json
from dataclasses import dataclass
from unittest.mock import patch

from .. import app


@dataclass
class FakeFilm:
    rating = 2.2
    description = "Fake description"
    distributed_by = "Fake dist"
    release_date = "2031-11-04"
    length = 11.1
    title = "Fake title"


class TestFilms:
    uuid = []

    def test_get_films_with_db(self):
        client = app.test_client()
        resp = client.get('/films')
        assert resp.status_code == http.HTTPStatus.OK

    @patch('src.services.film_service.FilmService.fetch_all_films', autospec=True)
    def test_get_films_mock_db(self, mock_db_call):
        client = app.test_client()
        resp = client.get('/films')
        mock_db_call.assert_called_once()
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json) == 0

    def test_create_film_with_db(self):
        client = app.test_client()
        data = {
            "rating": 6.6,
            "description": "test description",
            "distributed_by": "test dist",
            "release_date": "2001-11-04",
            "length": 99.9,
            "title": "Test title"}
        resp = client.post('/films', data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json['title'] == "Test title"
        self.uuid.append(resp.json['uuid'])

    def test_create_film_with_mock_db(self):
        with (patch('src.db.session.add', autospec=True) as mock_session_add,
                patch('src.db.session.commit', autospec=True) as mock_session_commit):
            client = app.test_client()
            data = {
                "rating": 6.6,
                "description": "test description",
                "distributed_by": "test dist",
                "release_date": "2001-11-04",
                "length": 99.9,
                "title": "Test title"}
            resp = client.post('/films', data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_update_film_with_db(self):
        client = app.test_client()
        url = f'/films/{self.uuid[0]}'
        data = {
            "description": "update description",
            "distributed_by": "update dist",
            "release_date": "2021-11-04",
            "title": "update title"}
        resp = client.put(url, data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json['title'] == "update title"

    def test_update_film_with_mock_db(self):
        with (patch('src.services.film_service.FilmService.fetch_film_by_uuid', autospec=True) as mocked_query,
                patch('src.db.session.add', autospec=True) as mock_session_add,
                patch('src.db.session.commit', autospec=True) as mock_session_commit):
            mocked_query.return_value = FakeFilm()
            client = app.test_client()
            url = '/films/1/'
            data = {
                "description": "update description",
                "distributed_by": "update dist",
                "release_date": "2021-11-04",
                "title": "update title"}
            resp = client.put(url, data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_delete_film_with_db(self):
        client = app.test_client()
        url = f'/films/{self.uuid[0]}'
        resp = client.delete(url)
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
