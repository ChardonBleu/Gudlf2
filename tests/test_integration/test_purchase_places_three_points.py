from tests.fixtures import club_one, competition_one
from server import BOOKING_PLACES_MULTIPLICATOR


def test_purchase_places_with_update_points(client, mocker,
                                            club_one, competition_one,
                                            captured_templates):
    """
    when logged user is redirected to welcome page.
    Then he can choose a competition de book places on it.
    If he tries to book more places than club points allows, he stays on
    booking page and can try again.
    If he has enough club points but if he tries to book more places than
    competition free places, then he stays on booking page and he can try
    again.
    If he book allowed number of places he is redirected to competitions page
    and receive a confirmation message.

    Arguments:
        logged_client {test_client} -- client with logged user
        mocker {mocking fixture} -- use to mock club and competition
        competition_one {dict} -- fixture for choosen competition
        club_one {dict} -- fixture for logged club
    """

    response = client.get('/login')
    assert response.status_code == 200
    template1, context1 = captured_templates[0]
    assert template1.name == "login.html"

    mocker.patch('server.research_club_in_clubs_by_email',
                 return_value=club_one)
    response = client.post('/login', data={'email': 'club_test1@mail.com'},
                           follow_redirects=True)
    template2, context2 = captured_templates[1]
    assert template2.name == "welcome.html"

    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_one)
    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_one)

    response = client.get('/book/<competition_name>/<club_name>',
                          follow_redirects=True)
    template3, context3 = captured_templates[2]
    assert template3.name == "booking.html"

    # tentative nb places achetées ok
    booked_places = 2
    response = client.post('/purchasePlaces',
                           data={'competition': "Compet du printemps",
                                 'club': 'club_test1_name',
                                 'places': str(booked_places)},
                           follow_redirects=True)
    template4, context4 = captured_templates[3]
    assert template4.name == "competitions.html"
    assert context4['club']['points'] == 15 - \
        booked_places * BOOKING_PLACES_MULTIPLICATOR
