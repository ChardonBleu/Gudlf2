from tests.fixtures import club_one, competition_one


def test_purchase_places_with_update_points(client, mocker,
                                            competition_one, club_one,
                                            captured_templates):
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

    booked_places = 4
    response = client.post('/purchasePlaces',
                                  data={'competition': "Compet du printemps",
                                        'club': 'club_test1_name',
                                        'places': str(booked_places)},
                                  follow_redirects=True)
    template4, context4 = captured_templates[3]
    assert template4.name == "competitions.html"
    assert context4['competition']['numberOfPlaces'] == initial_competition_places - booked_places