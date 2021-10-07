import pytest

from tests.fixtures import club_one

def test_login_display_points_successful(client, mocker, club_one):
    
    response = client.get('/login')
    assert response.status_code == 200
    
    mocker.patch('server.research_club_in_clubs_by_email',
                 return_value=club_one)
    response = client.post('/login', data={'email': 'club_test1@mail.com'},
                follow_redirects=True)
    
    assert b'Welcome, club_test1@mail.com. You\'re logged in' in response.data
    
    
    response = client.get('/welcome')