import pytest

from flask import session

from tests.fixtures import club_one, clubs


def _login(client, email):
    return(client.post('/login', data={'email': email}, follow_redirects=True))

 
def test_welcome(client, club_one, mocker):
    mocker.patch('server.research_club_in_clubs_by_email',
                 return_value=club_one)
    _login(client, 'club_test1_name')
    
    response = client.get('/welcome')
    assert response.status_code == 200

def test_redirect_if_non_logged(client):
    response = client.get('/welcome')
    assert response.status_code == 302