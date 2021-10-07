import pytest
from flask import Flask

from server import research_club_in_clubs_by_name
from server import research_competition_in_competitions_by_name
from tests.fixtures import club_one, competition_one


def test_purchase_places_with_update_points(client, mocker,
                                            club_one, competition_one,
                                            captured_templates):
    """
    {'name': 'club_test1_name',
                'email': 'club_test1@mail.com',
                'points': '15'}
    The competition is:
    {"name": "Compet du printemps",
     "date": "2040-04-01 10:00:00",
     "numberOfPlaces": "10"}
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
    initial_points_club = int(context3['club']['points'])
    
    
    
    # tentative nb places achetées > points club
    booked_places = 20
    response = client.post('/purchasePlaces',
                                  data={'competition': "Compet du printemps",
                                        'club': 'club_test1_name',
                                        'places': str(booked_places)},
                                  follow_redirects=True)
    template4, context4 = captured_templates[3]
    assert template4.name == "booking.html"
    assert context4['club']['points'] == '15'
    assert context4['competition']['numberOfPlaces'] == '10'
    
    # tentative nb places achetées > places compet
    booked_places = 12
    response = client.post('/purchasePlaces',
                                  data={'competition': "Compet du printemps",
                                        'club': 'club_test1_name',
                                        'places': str(booked_places)},
                                  follow_redirects=True)
    template5, context5 = captured_templates[4]
    assert template5.name == "booking.html"
    assert context5['club']['points'] == '15'
    assert context5['competition']['numberOfPlaces'] == '10'

    # tentative nb places achetées ok
    booked_places = 8
    response = client.post('/purchasePlaces',
                                  data={'competition': "Compet du printemps",
                                        'club': 'club_test1_name',
                                        'places': str(booked_places)},
                                  follow_redirects=True)
    template6, context6 = captured_templates[5]
    assert template6.name == "competitions.html"
    assert context6['club']['points'] == '7'
    assert context6['competition']['numberOfPlaces'] == '2'
