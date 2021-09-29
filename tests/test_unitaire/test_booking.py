import pytest

from flask import session
from server import research_club_in_clubs_by_email

from tests.fixtures import club_one, clubs, competitions, competition_one
    

def _login(client, email):
    return(client.post('/login', data={'email': email}, follow_redirects=True))

 
def test_welcome_status_ok(client, mocker, club_one):
    mocker.patch('server.research_club_in_clubs_by_email', return_value=club_one)
    _login(client, 'club_test1_name')
    
    response = client.get('/showSummary')
    assert response.status_code == 200

def test_book_status_ok(client, mocker, club_one):
    mocker.patch('server.research_club_in_clubs_by_email', return_value=club_one)
    _login(client, 'club_test1_name')
    
    
    response = client.get('/book/<competition>/<club>')
    assert response.status_code == 200
