from os import stat_result
from re import template
import pytest
from flask import Flask


def test_public_tab_with_non_logged_client(client):
    """
    """    
    
    response = client.get('/index')
    assert response.status_code == 200
    assert b'Club name' in response.data
    assert b'Points' in response.data
