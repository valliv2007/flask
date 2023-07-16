import http
import json
from dataclasses import dataclass
from datetime import date
from unittest.mock import patch
from src import db

from .. import app


@dataclass
class FakeActor:
    name = 'Fake actor'
    is_active = True
    birthday = date(2022, 5, 15)


class TestActor:
    uuid = []

    def test_get_actors_with_db(self):
        client = app.test_client()
        resp = client.get('/actors')
        assert resp.status_code == http.HTTPStatus.OK

    @patch('src.db.session.query', autospec=True)
    def test_get_actors_mock_db(self, mock_db_call):
        client = app.test_client()
        resp = client.get('/actors')
        mock_db_call.assert_called_once()
        assert resp.status_code == http.HTTPStatus.OK

    def test_create_actor_with_db(self):
        client = app.test_client()
        data = {
            "name": 'Test actor1',
            "is_active": True,
            "birthday": "2001-11-04"}
        resp = client.post('/actors', data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json['birthday'] == "2001-11-04"
        self.uuid.append(resp.json['uuid'])

    def test_create_actor_with_mock_db(self):
        with (patch('src.db.session.add', autospec=True) as mock_session_add,
                patch('src.db.session.commit', autospec=True) as mock_session_commit):
            client = app.test_client()
            data = {
                "name": 'Test actor',
                "is_active": True,
                "birthday": "2001-11-04"}
            resp = client.post('/actors', data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_update_actor_with_db(self):
        client = app.test_client()
        url = f'/actors/{self.uuid[0]}'
        data = {
            "name": 'update actor',
            "is_active": False,
            "birthday": "2002-11-04"}
        resp = client.put(url, data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json['name'] == "update actor"

    def test_update_film_with_mock_db(self):
        with (patch('src.db.session.query', autospec=True) as mocked_query,
                patch('src.db.session.add', autospec=True) as mock_session_add,
                patch('src.db.session.commit', autospec=True) as mock_session_commit):
            mocked_query.return_value.filter.return_value = FakeActor()
            client = app.test_client()
            url = '/actors/1/'
            data = {
                "name": 'update actor',
                "is_active": False}
            resp = client.patch(url, data=json.dumps(data), content_type='application/json')
            print(resp.json)
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()
    
    def test_get_film_with_db(self):
        client = app.test_client()
        resp = client.get(f'/actors/{self.uuid[0]}/')
        print(resp.json)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json['uuid'] == self.uuid[0]
        assert resp.json['name'] == "update actor"

    def test_delete_actor_with_db(self):
        client = app.test_client()
        url = f'/actors/{self.uuid[0]}'
        resp = client.delete(url)
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
