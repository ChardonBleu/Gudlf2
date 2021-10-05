from os import stat_result
import pytest
from flask import Flask

from server import research_club_in_clubs_by_name
from server import research_competition_in_competitions_by_name
from tests.fixtures import club_one, competition_past


def test_past_competition_purchase_non_authorized(logged_client, mocker,
                                                  club_one, competition_past):
    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_one)

    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_past)

    response = logged_client.get('/book/<competition_name>/<club_name>')
    assert response.status_code == 200
    assert b'This competition is passed. Choice another.' in response.data


def test_future_competition_purchase_authorized(logged_client, mocker,
                                                  club_one, competition_past):
    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_one)

    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_past)

    response = logged_client.get('/book/<competition_name>/<club_name>')
    assert response.status_code == 200
    assert b'You can book for this future competition.' in response.data
