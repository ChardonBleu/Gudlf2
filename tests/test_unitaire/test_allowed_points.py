from tests.fixtures import club_one, competition_one, club_max
from server import BOOKING_PLACES_MULTIPLICATOR


def test_book_more_than_points_club(logged_client, mocker,
                                    competition_one, club_one):
    """The logged club test list is :
    {'name': 'club_test1_name',
                'email': 'club_test1@mail.com',
                'points': '15'}
    
    Arguments:
        logged_client {test_client} -- client connecté
        mocker {mocking fixture} -- use to mock club and competition
        competition_one {dict} -- fixture for choosen competition
        club_one {dict} -- fixture for logged club
    """
    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_one)
    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_one)

    response = logged_client.post('/purchasePlaces',
                                  data={'competition': "Compet du printemps",
                                        'club': 'club_test1_name',
                                        'places': '16'})
    assert response.status_code == 200
    assert b'Not enough points available. Sorry.' in response.data


def test_booking_ok(logged_client, mocker, competition_one,
                    club_one, captured_templates):
    """The logged club test list is :
    {'name': 'club_test1_name',
                'email': 'club_test1@mail.com',
                'points': '15'}
    the test book 3 places to "compet du printemps".
    It mights remain 12 places in points club.

    Arguments:
        logged_client {test_client} -- client connecté
        mocker {mocking fixture} -- use to mock club and competition
        competition_one {dict} -- fixture for choosen competition
        club_one {dict} -- fixture for logged club
    """
    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_one)
    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_one)

    response = logged_client.post('/purchasePlaces',
                                  data={'competition': "Compet du printemps",
                                        'club': 'club_test1_name',
                                        'places': '3'})
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
    template, context = captured_templates[0]
    assert context['club']['points'] == 15 - 3 * BOOKING_PLACES_MULTIPLICATOR


def test_book_more_than_competition_places(logged_client, mocker,
                                           competition_one, club_max):
    """The logged club test list is :
    {'name': 'club_test1_name',
                'email': 'club_test1@mail.com',
                'points': '15'}
    The competition is:
    {"name": "Compet du printemps",
     "date": "2040-04-01 10:00:00",
     "numberOfPlaces": "10"}
    the test book 4 places to "compet du printemps".
    It mights remain 11 places in poinst club.

    Arguments:
        logged_client {test_client} -- client connecté
        mocker {mocking fixture} -- use to mock club and competition
        competition_one {dict} -- fixture for choosen competition
        club_one {dict} -- fixture for logged club
    """
    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_one)
    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_max)

    response = logged_client.post('/purchasePlaces',
                                  data={'competition': "Compet du printemps",
                                        'club': 'club_test1_name',
                                        'places': '11'})
    assert response.status_code == 200
    assert b'Not enough places available. Sorry' in response.data
