import pytest

from flask import session
from server import research_club_in_clubs_by_email
from tests.fixtures import club_one, clubs


def test_successful_login_logout_route(client, mocker, club_one):
    client.get('/logout')
    
    response = client.get('/')
    assert response.status_code == 200
    
    response = client.get('/login')
    assert response.status_code == 200
    
    mocker.patch('server.research_club_in_clubs_by_email',
                 return_value=club_one)
    response = client.post('/login', data={'email': 'club_test1@mail.com'},
                follow_redirects=True)
    assert session['email'] == 'club_test1@mail.com'
    assert b'Welcome, club_test1@mail.com. You\'re logged in' in response.data
    
    response = client.get('/logout')
    assert response.status_code == 302
    assert session == {}


def test_unsuccesful_login_route(client, mocker):
    client.get('/logout')
    
    response = client.get('/')
    assert response.status_code == 200
    
    response = client.get('/login')
    assert response.status_code == 200
    
    response = client.post('/login', data={'email': 'pas_bon1@mail.com'},
                follow_redirects=True)
    assert response.status_code == 200
    assert b'Unknown club. Sorry.' in response.data
    assert session == {}
    
