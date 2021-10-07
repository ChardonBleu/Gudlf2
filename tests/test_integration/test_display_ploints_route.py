import pytest

from tests.fixtures import club_one

def test_login_display_points_successful(client, mocker, club_one):
    
    
    
    
    mocker.patch('server.research_club_in_clubs_by_email',
                 return_value=club_one)
    response = client.get('/welcome')