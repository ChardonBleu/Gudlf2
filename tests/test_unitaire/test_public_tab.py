def test_public_tab_with_non_logged_client(client):
    """
    Tab with all club points is displayed on index page.
    It's not necesary to be logged to see it.
    """
    response = client.get('/index')
    assert response.status_code == 200
    assert b'Club name' in response.data
    assert b'Points' in response.data
