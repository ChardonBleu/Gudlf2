import subprocess
import os
import time

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session", autouse=True)
def live_server():
    env = os.environ.copy()
    env["FLASK_APP"] = "server.py"
    env["FLASK_ENV"] = "development"
    server = subprocess.Popen(['flask', 'run', '--port', '5000'], env=env)
    try:
        yield server
    finally:
        server.terminate()


@pytest.mark.usefixtures('live_server')
def test_purchase_places():    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('http://127.0.0.1:5000/login')
    email = driver.find_element_by_name('email')
    email.send_keys('admin@irontemple.com')
    driver.find_element_by_tag_name('button').click()
    driver.get('http://127.0.0.1:5000/showSummary')
    points_club_before = driver.find_element_by_id('points').text
    assert points_club_before == 'Points available: 4'
    time.sleep(2)
    driver.find_elements_by_link_text('Book Places')[0].click()
    time.sleep(2)
    places = driver.find_element_by_name('places')
    places.send_keys('2')
    driver.find_element_by_tag_name('button').click()
    points_club_after = driver.find_element_by_id('points').text
    assert points_club_after == 'Points available: 2'
    time.sleep(2)
    driver.quit()