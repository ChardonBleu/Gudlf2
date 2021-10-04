import pytest
from server import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client

@pytest.fixture
def logged_client(mocker):
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        mocker.patch('server.research_club_in_clubs_by_email',
                 return_value={'name': 'club_test1_name',
                               'email': 'club_test1@mail.com',
                               'points': '15'})
        client.post('/login', data={'email': 'club_test1_name'}, follow_redirects=True)
        yield client