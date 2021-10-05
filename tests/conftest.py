import pytest
from flask import template_rendered
from server import create_app

@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def logged_client(app, mocker):
    with app.test_client() as client:
        mocker.patch('server.research_club_in_clubs_by_email',
                     return_value={'name': 'club_test1_name',
                                   'email': 'club_test1@mail.com',
                                   'points': '15'})
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
