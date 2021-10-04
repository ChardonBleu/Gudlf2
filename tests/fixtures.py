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