import pytest

from flask import session

from tests.fixtures import club_one
from tests.conftest import client, logged_client


    
def test_welcome_for_display_points(logged_client, club_one, mocker):
    mocker.patch('server.research_club_in_clubs_by_email',
                 return_value=club_one)
    response = logged_client.get('/welcome')
    assert response.status_code == 200
    assert b'All clubs points:' in response.data
    assert b' <td>Iron Temple</td>\n                    <td>4</td>' in response.data


def test_redirect_if_non_logged(client):
    response = client.get('/welcome')
    assert response.status_code == 302
