import http
from unittest.mock import patch

from .. import app


class TestFilms:
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
