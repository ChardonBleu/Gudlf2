from flask import session
from tests.fixtures import club_one, clubs


def test_successful_login_logout_route(client, mocker, club_one,
                                       captured_templates):
    """when logged user is redirected to welcome page.

    Arguments:
        client {[type]} -- unlogged client
        mocker {[type]} -- used to mock logged club
        club_one {[type]} -- logged club
    """
    client.get('/logout')

    response = client.get('/')
    assert response.status_code == 200
    template0, context0 = captured_templates[0]
    assert template0.name == 'index.html'

    response = client.get('/login')
    assert response.status_code == 200
    template1, context1 = captured_templates[1]
    assert template1.name == 'login.html'

    mocker.patch('server.research_club_in_clubs_by_email',
                 return_value=club_one)
    response = client.post('/login', data={'email': 'club_test1@mail.com'},
                           follow_redirects=True)
    assert session['email'] == 'club_test1@mail.com'
    assert b'Welcome, club_test1@mail.com. You\'re logged in' in response.data

    template2, context2 = captured_templates[2]
    assert template2.name == 'welcome.html'

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert session == {}
    template3, context3 = captured_templates[3]
    assert template3.name == 'index.html'


def test_unsuccessful_login_route(client, captured_templates):
    """If loggin unsuccessful, user can try again on login page.

    Arguments:
        client {[type]} -- unlogged client
    """
    client.get('/logout')

    response = client.get('/')
    assert response.status_code == 200
    template0, context0 = captured_templates[0]
    assert template0.name == 'index.html'

    response = client.get('/login')
    assert response.status_code == 200
    template1, context1 = captured_templates[1]
    assert template1.name == 'login.html'

    response = client.post('/login', data={'email': 'pas_bon1@mail.com'},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Unknown club. Sorry.' in response.data
    assert session == {}
    template2, context2 = captured_templates[2]
    assert template2.name == 'login.html'
