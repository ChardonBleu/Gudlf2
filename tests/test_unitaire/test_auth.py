import pytest

from flask import session
from server import research_club_in_clubs
from tests.conftest import client


@pytest.fixture
def club_one():
    club_one = {'name': 'club_test1_name',
              'email': 'club_test1@mail.com',
              'points': '15'}
    return club_one

@pytest.fixture
def clubs():
    clubs = [{'name': 'club_test1_name',
              'email': 'club_test1@mail.com',
              'points': '15'},
             {'name': 'club_test2_name',
              'email': 'club_test2@mail.com',
              'points': '8'}     ]        
    return clubs

def login(client, email):
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


def test_research_clubs_in_clubs(clubs, club_one):
    result = research_club_in_clubs(clubs, 'club_test1@mail.com')
    assert result == club_one


def test_login_succesful(client, club_one, mocker):
    client.get('/logout')
    
    mocker.patch('server.research_club_in_clubs', return_value=club_one)
    login(client, 'club_test1@mail.com')
    
    assert session['email'] == 'club_test1@mail.com'


def test_login_unsuccesful(client, club_one, mocker):
    client.get('/logout')
    
    response = login(client, 'pas_bon@mail.com')
    
    assert response.status_code == 200
    assert b'Unknown club. Sorry.' in response.data
    assert session == {}
    

def test_logout_redirection(client):
    response = client.get('/logout')
    assert response.status_code == 302


def test_logout_session_cleared(client, mocker, club_one):    
    mocker.patch('server.research_club_in_clubs', return_value=club_one)
    login(client, 'club_test1@mail.com')

    response = client.get('/logout')
    assert session == {}
