import pytest

from flask import session
import server
from tests.conftest import client


@pytest.fixture
def club_test():
    club = {
        'name': 'club_test_name',
        'email': 'club_test@mail.com',
        'points': '15'
    }
    return club


def test_root_status_ok(client):
    response = client.get('/')
    assert response.status_code == 200

def test_index_status_ok(client):
    response = client.get('/index')
    assert response.status_code == 200

def test_login_page_access_ok(client):
    response = client.get('/login')
    assert response.status_code == 200






def test_logout_redirection(client):
    response = client.get('/logout')
    assert response.status_code == 302

def test_logout_session_cleared(client):
    response = client.get('/logout')
    assert session == {}

