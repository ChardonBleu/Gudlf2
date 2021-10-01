import pytest

from flask import session



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
              'points': '8'}]
    return clubs


def _login(client, email):
    return(client.post('/login', data={'email': email}, follow_redirects=True))

 
def test_welcome(client, club_one, mocker):
    mocker.patch('server.research_club_in_clubs_by_email',
                 return_value=club_one)
    _login(client, 'club_test1_name')
    
    response = client.get('/welcome')
    assert response.status_code == 200