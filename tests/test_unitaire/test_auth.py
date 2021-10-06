import pytest

from flask import session
from server import research_club_in_clubs_by_email
from tests.fixtures import club_one, clubs


def _login(client, email):
    return(client.post('/login', data={'email': email}, follow_redirects=True))


def test_root_status_ok(client):
    response = client.get('/')
    assert response.status_code == 200


def test_index_status_ok(client):
    response = client.get('/index')
    assert response.status_code == 200


def test_login_page_access_ok(client):
    response = client.get('/login')
    assert response.status_code == 200


def test_research_clubs_in_clubs_by_email(clubs, club_one):
    result = research_club_in_clubs_by_email(clubs, 'club_test1@mail.com')
    assert result == club_one


def test_login_succesful(client, club_one, mocker):
    client.get('/logout')

    mocker.patch('server.research_club_in_clubs_by_email',
                 return_value=club_one)
    _login(client, 'club_test1@mail.com')

    assert session['email'] == 'club_test1@mail.com'


def test_login_unsuccesful(client):
    client.get('/logout')

    response = _login(client, 'pas_bon@mail.com')

    assert response.status_code == 200
    assert b'Unknown club. Sorry.' in response.data
    assert session == {}


def test_logout_redirection(client):
    response = client.get('/logout')
    assert response.status_code == 302


def test_logout_session_cleared(client, mocker, club_one):
    mocker.patch('server.research_club_in_clubs_by_email',
                 return_value=club_one)
    _login(client, 'club_test1@mail.com')

    client.get('/logout')
    assert session == {}