import pytest
from flask import Flask

from server import research_club_in_clubs_by_name
from server import research_competition_in_competitions_by_name
from tests.fixtures import club_one, competition_one


def test_purchase_places_with_update_points(client, mocker,
                                            competition_one,club_one,
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
    
    response = client.get('/booking', follow_redirects=True)
    assert response.status_code == 200
    template3, context3 = captured_templates[2]
    assert template3.name == "booking.html"
    
    booked_places = 4
    response = client.post('/purchasePlaces',
                                  data={'competition': "Compet du printemps",
                                        'club': 'club_test1_name',
                                        'places': str(booked_places)},
                                  follow_redirects=True)
    template4, context4 = captured_templates[3]
    assert template4.name == "competitions.html"
    assert context4['club']['points'] == context3['club']['points'] - booked_places