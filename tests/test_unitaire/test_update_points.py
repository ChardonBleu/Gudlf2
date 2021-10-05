from os import stat_result
import pytest

from server import research_club_in_clubs_by_name
from server import research_competition_in_competitions_by_name
from tests.fixtures import club_one, clubs, competition_one, competitions


def test_status_code_ok_when_logged(logged_client, mocker):
    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_one)
    mocker.patch('server.research_competition_in_clubs_by_name',
                 return_value=club_one)
    response = logged_client.post('/purchasePlaces', data={'places': '4'})
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data


def test_redirect_when_unlogged(client, mocker):
    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_one)
    mocker.patch('server.research_competition_in_clubs_by_name',
                 return_value=club_one)
    response = client.post('/purchasePlaces', data={'places': '4'})
    assert response.status_code == 302
