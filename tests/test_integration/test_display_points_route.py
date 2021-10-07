from tests.fixtures import club_one


def test_login_display_points_successful(client, mocker, club_one,
                                         captured_templates):
    """when logged user is redirected to welcome page and logged user can see
    there the points tab of all clubs.

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
    assert response.status_code == 200
    assert b'Welcome, club_test1@mail.com. You\'re logged in' in response.data
    assert b'All clubs points:' in response.data

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    template3, context3 = captured_templates[2]
    assert template3.name == "index.html"
