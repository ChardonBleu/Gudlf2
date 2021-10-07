from tests.fixtures import club_one, competition_one


def test_purchase_places_with_update_points(client, mocker, competition_one,
                                            club_one, captured_templates):
    """when logged user is redirected to welcome page.
    Then he can choose a competition de book places on it.
    If he tries to book more than 12 places he receive an alert message.
    He stays on booking page and he can try again.
    If he purchase for less than 12 places he is redirected to competitions
    page with a confirmation message and competition places are updated.

    Arguments:
        client {[type]} -- unlogged client
        mocker {[type]} -- used to mock logged club
        club_one {[type]} -- logged club
        competition_one {[type]} -- selected competition for booking
        captured_templates {[type]} -- used to control rendered template
        competition_past {[type]} -- competition with date in past
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
    initial_competition_places = int(context3['competition']['numberOfPlaces'])

    booked_places = 13
    response = client.post('/purchasePlaces',
                           data={'competition': "Compet du printemps",
                                 'club': 'club_test1_name',
                                 'places': str(booked_places)},
                           follow_redirects=True)
    template4, context4 = captured_templates[3]
    assert template4.name == "booking.html"

    booked_places = 4
    response = client.post('/purchasePlaces',
                           data={'competition': "Compet du printemps",
                                 'club': 'club_test1_name',
                                 'places': str(booked_places)},
                           follow_redirects=True)
    template5, context5 = captured_templates[4]
    assert template5.name == "competitions.html"
    assert context5['competition'][
          'numberOfPlaces'] == initial_competition_places - booked_places
