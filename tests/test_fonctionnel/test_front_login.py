import subprocess
import os
import time

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(autouse=True)
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
def test_login():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('http://127.0.0.1:5000/login')
    time.sleep(2)
    email = driver.find_element_by_name('email')
    email.send_keys('john@simplylift.co')
    driver.find_element_by_id('submit').click()
    time.sleep(2)
    driver.quit() 
