import pytest

from server import research_club_in_clubs_by_name
from server import research_competition_in_competitions_by_name
from tests.fixtures import club_one, clubs, competition_one, competitions

def test_succesful_book_route(client, mocker, club_one, competition_one,
                              captured_templates):
    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_one)
    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_one)

    

    response = client.get('/book/<competition_name>/<club_name>',
                          follow_redirects=True)
    print(captured_templates)