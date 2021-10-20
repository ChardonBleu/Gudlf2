from tests.fixtures import club_max, competition_max, club_one, competition_one


def test_update_numberofplaces(logged_client, mocker, competition_one,
                               club_one, captured_templates):
    """The competition test list is :
    [{"name": "Compet du printemps",
                     "date": "2040-04-01 10:00:00",
                     "numberOfPlaces": "10"},
                    {"name": "Compet des gros costauds",
                     "date": "2035-08-15 13:30:00",
                     "numberOfPlaces": "18"}]
    the test book 4 places to "compet du printemps".
    It mights remain 6 places in "compet du printemps".

    Arguments:
        logged_client {test_client} -- client with logged user
        mocker {mocking fixture} -- use to mock club and competition
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
    assert context['competition']['numberOfPlaces'] == 6


def test_no_more_than_12_places_booked(logged_client, mocker,
                                       competition_max, club_max):
    """The competition test list is :
    [{'name': 'club_test_max_name',
      'email': 'club_test_max@mail.com',
      'points': '50'},
    {"name": "Compet des vieux balèzes",
     "date": "2018-08-15 13:30:00",
     "numberOfPlaces": "23"}]
    the test book 4 places to "compet du printemps".
    It mights remain 6 places in "compet du printemps".

    Arguments:
        logged_client {test_client} -- client with logged user
        mocker {mocking fixture} -- use to mock club and competition
        competition_one {dict} -- fixture for choosen competition
        club_one {dict} -- fixture for logged club
        captured_templates  -- fixture for capture of rendered templates
    """
    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_max)
    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_max)

    response = logged_client.post('/purchasePlaces',
                                  data={'competition': "Compet du printemps",
                                        'club': 'club_test1_name',
                                        'places': '13'})
    assert response.status_code == 200
    assert b'You can only book places between 0 ans 12.' in response.data
