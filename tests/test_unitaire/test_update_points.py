from os import stat_result
import pytest
from flask import Flask

from server import research_club_in_clubs_by_name
from server import research_competition_in_competitions_by_name
from server import load_competitions
from utilities.datas import load_competitions
from tests.fixtures import club_one, clubs, competition_one, competitions


def test_status_code_ok_when_logged(logged_client, mocker,
                                    club_one, competition_one):
    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_one)
    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_one)
    response = logged_client.post('/purchasePlaces',
                                  data={'competition': "Compet du printemps",
                                        'club': 'club_test1_name',
                                        'places': '4'})
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data


def test_redirect_when_unlogged(client, mocker,
                                club_one, competition_one):
    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_one)
    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_one)
    response = client.post('/purchasePlaces',
                           data={'competition': "Compet du printemps",
                                 'club': 'club_test1_name',
                                 'places': '4'})
    assert response.status_code == 302


def test_update_numberofplaces(logged_client, mocker,competition_one,
                       club_one, captured_templates):
    """The competition test list is :
    [{"name": "Compet du printemps",
                     "date": "2040-04-01 10:00:00",
                     "numberOfPlaces": "30"},
                    {"name": "Compet des gros costauds",
                     "date": "2035-08-15 13:30:00",
                     "numberOfPlaces": "18"}]
    the test book 4 places to "compet du printemps".
    It mights remain 26 places in "compet du printemps".

    Arguments:
        logged_client {test_client} -- client connecté 
        mocker {mocking fixture} -- use to mock club and competition
        competitions {list} -- fixture fot tests competitions
        competition_one {dict} -- fixture for choosen competition
        club_one {dict} -- fixture for logged club
        captured_templates  -- fixture for capture of rendered templates
    """
    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_one)
    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_one)
    
    response = logged_client.post('/purchasePlaces',
                                  data={'competition': "Compet du printemps",
                                        'club': 'club_test1_name',
                                        'places': '4'})
    assert response.status_code == 200    
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == 'competitions.html'
    assert context['competition']['numberOfPlaces'] == 26


def test_update_points_club(logged_client, mocker,competition_one,
                       club_one, captured_templates):
    """The logged club test list is :
    {'name': 'club_test1_name',
                'email': 'club_test1@mail.com',
                'points': '15'}
    the test book 4 places to "compet du printemps".
    It mights remain 11 places in poinst club.

    Arguments:
        logged_client {test_client} -- client connecté 
        mocker {mocking fixture} -- use to mock club and competition
        competitions {list} -- fixture fot tests competitions
        competition_one {dict} -- fixture for choosen competition
        club_one {dict} -- fixture for logged club
        captured_templates  -- fixture for capture of rendered templates
    """
    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_one)
    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_one)
    
    response = logged_client.post('/purchasePlaces',
                                  data={'competition': "Compet du printemps",
                                        'club': 'club_test1_name',
                                        'places': '4'})
    assert response.status_code == 200    
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == 'competitions.html'
    assert context['club']['points'] == 11
