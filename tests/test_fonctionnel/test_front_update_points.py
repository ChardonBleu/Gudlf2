import time

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from flask_testing import LiveServerTestCase

from server import create_app


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


@pytest.fixture
def competitions():
    competitions = [{"name": "Compet du printemps",
                     "date": "2040-04-01 10:00:00",
                     "numberOfPlaces": "10"},
                    {"name": "Compet des gros costauds",
                     "date": "2035-08-15 13:30:00",
                     "numberOfPlaces": "18"},
                    {"name": "Compet des vieux balèzes",
                     "date": "2018-08-15 13:30:00",
                     "numberOfPlaces": "23"}]
    return competitions


@pytest.fixture
def competition_one():
    competition_one = {"name": "Compet du printemps",
                       "date": "2040-04-01 10:00:00",
                       "numberOfPlaces": "10"}
    return competition_one


@pytest.mark.usefixtures('competitions', 'clubs', 'club_one', 'competition_one')
class TestBase(LiveServerTestCase):

    def create_app(self):
        app = create_app({"TESTING": True})
        return app

    def setUp(self):
        """Setup the test driver and create test users"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())  

    def tearDown(self):
        self.driver.quit()

    
    def test_purchase_and_update_points(self):
       
        self.driver.get(self.get_server_url() + "/login")
        email = self.driver.find_element_by_name('email')
        email.send_keys('john@simplylift.co')
        time.sleep(2)

        login = self.driver.find_element_by_id('/login')
        login.click()
        time.sleep(2)      
