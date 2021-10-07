from tests.fixtures import club_one, clubs, competition_one, competitions


def test_book_route(client, mocker, club_one, competition_one,
                    captured_templates):
    """when logged user is redirected to welcome page.
    Then he can choose a competition to book places on it.

    Arguments:
        client {[type]} -- unlogged client
        mocker {[type]} -- used to mock logged club
        club_one {[type]} -- logged club
        competition_one {[type]} -- selected competition for booking
        captured_templates {[type]} -- used to control rendered template
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

    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_one)

    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=None)

    response = client.get('/book/<competition_name>/<club_name>',
                          follow_redirects=True)
    template3, context3 = captured_templates[2]
    assert template3.name == "competitions.html"

    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_one)

    response = client.get('/book/<competition_name>/<club_name>',
                          follow_redirects=True)
    template4, context4 = captured_templates[3]
    assert template4.name == "booking.html"
