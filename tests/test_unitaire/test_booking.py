import pytest

from flask import session
from server import research_club_in_clubs_by_email
from server import research_club_in_clubs_by_name
from server import research_competition_in_competitions_by_name
from tests.fixtures import club_one, clubs, competition_one, competitions


def _login(client, email):
    return(client.post('/login', data={'email': email}, follow_redirects=True))

def test_research_clubs_in_clubs_by_name(clubs, club_one):
    result = research_club_in_clubs_by_name(clubs, 'club_test1_name')
    assert result == club_one

def test_research_competition_in_competitions_by_name(competitions,
                                                 competition_one):
    result = research_competition_in_competitions_by_name(competitions,
                                                          "Compet du printemps")
    assert result == competition_one

def test_book_status_ok(client, mocker, club_one, competition_one):
    mocker.patch('server.research_club_in_clubs_by_email',
                 return_value=club_one)
    _login(client, 'club_test1_name')

    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_one)

    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_one)

    response = client.get('/book/<competition_name>/<club_name>')
    assert response.status_code == 200
    assert b'club_test1_name' in response.data
    assert b'Compet du printemps' in response.data

def test_book_status_wrong(client, mocker, club_one, competition_one):
    mocker.patch('server.research_club_in_clubs_by_email',
                 return_value=club_one)
    _login(client, 'club_test1_name')

    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_one)

    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=None)

    response = client.get('/book/<competition_name>/<club_name>')
    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data