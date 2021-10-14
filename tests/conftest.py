import pytest


from flask import template_rendered, current_app
from server import create_app
from tests.fixtures import competitions, club_one, clubs


@pytest.fixture
def app(mocker, competitions, clubs):
    mocker.patch('server.load_competitions',
                     return_value=competitions)
    mocker.patch('server.load_clubs',
                     return_value=clubs)
    app = create_app({"TESTING": True})
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def logged_client(app, mocker, club_one):
    with app.test_client() as client:        
        mocker.patch('server.research_club_in_clubs_by_email',
                     return_value=club_one)
        
        client.post('/login',
                    data={'email': 'club_test1_name'},
                    follow_redirects=True)
        yield client

@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


