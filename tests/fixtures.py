import pytest


@pytest.fixture
def clubs():
    clubs = [{'name': 'club_test1_name',
              'email': 'club_test1@mail.com',
              'points': '15'},
             {'name': 'club_test2_name',
              'email': 'club_test2@mail.com',
              'points': '8'}]
    return clubs


@pytest.fixture
def club_one():
    club_one = {'name': 'club_test1_name',
                'email': 'club_test1@mail.com',
                'points': '15'}
    return club_one


@pytest.fixture
def competitions():
    competitions = [{"name": "Compet du printemps",
                     "date": "2040-04-01 10:00:00",
                     "numberOfPlaces": "30"},
                    {"name": "Compet des gros costauds",
                     "date": "2035-08-15 13:30:00",
                     "numberOfPlaces": "18"}]
    return competitions

@pytest.fixture
def competition_one():
    competition_one = {"name": "Compet du printemps",
                     "date": "2040-04-01 10:00:00",
                     "numberOfPlaces": "30"}
    return competition_one
