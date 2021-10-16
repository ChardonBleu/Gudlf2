import unittest
import pytest
import time
from unittest.mock import patch

from flask_testing import LiveServerTestCase
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from server import load_competitions, load_clubs, research_club_in_clubs_by_email
from server import create_app


CLUBS = [{'name': 'club_test1_name',
            'email': 'club_test1@mail.com',
            'points': '15'},
            {'name': 'club_test2_name',
            'email': 'club_test2@mail.com',
            'points': '8'}]

CLUB_ONE = {'name': 'club_test1_name',
                'email': 'club_test1@mail.com',
                'points': '15'}

COMPETITIONS = [{"name": "Compet du printemps",
                    "date": "2040-04-01 10:00:00",
                    "numberOfPlaces": "10"},
                    {"name": "Compet des gros costauds",
                    "date": "2035-08-15 13:30:00",
                    "numberOfPlaces": "18"},
                    {"name": "Compet des vieux balèzes",
                    "date": "2018-08-15 13:30:00",
                    "numberOfPlaces": "23"}]


class TestAllowedPoints(LiveServerTestCase):

    @patch('server.load_competitions')
    @patch('server.load_clubs')
    def create_app(self, mock_load_clubs, mock_load_competitions):        
        mock_load_clubs.return_value = CLUBS
        mock_load_competitions.return_value = COMPETITIONS
        app = create_app({"TESTING": True})
        app.config.update(
            LIVESERVER_PORT=8943
        )
        return app

    def setUp(self):
        """Setup the test driver and create test users"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(self.get_server_url())

    def tearDown(self):
        self.driver.quit()

    @patch('server.research_club_in_clubs_by_email')
    def test_booking_places_ok(self, mock_research_club_in_clubs_by_email):
        mock_research_club_in_clubs_by_email.return_value = CLUB_ONE
        
        self.driver.get(self.get_server_url() + "/login")
        time.sleep(2)
        email = self.driver.find_element_by_name('email')
        email.send_keys("club_test1@mail.com")

        time.sleep(2) 
        self.driver.find_element_by_tag_name('button').click()
        time.sleep(2)
        self.driver.get(self.get_server_url() + "/showSummary")
        self.driver.find_element_by_id('points')
        assert 'Points available: 15' in self.driver.page_source
        time.sleep(2)
        self.driver.find_elements_by_id('book')[0].click()
        time.sleep(2)
        places = self.driver.find_element_by_name('places')
        places.send_keys("2")
        time.sleep(2)
        self.driver.find_element_by_tag_name('button').click()
        time.sleep(2)
        self.driver.find_element_by_id('points')
        assert 'Points available: 13' in self.driver.page_source
        time.sleep(2)

    @patch('server.research_club_in_clubs_by_email')
    def test_not_enough_points(self, mock_research_club_in_clubs_by_email):
        mock_research_club_in_clubs_by_email.return_value = CLUB_ONE

        self.driver.get(self.get_server_url() + "/login")
        time.sleep(2)
        email = self.driver.find_element_by_name('email')
        email.send_keys("club_test1@mail.com")

        time.sleep(2) 
        self.driver.find_element_by_tag_name('button').click()
        time.sleep(2)
        self.driver.get(self.get_server_url() + "/showSummary")
        self.driver.find_element_by_id('points')
        assert 'Points available: 15' in self.driver.page_source
        time.sleep(2)
        self.driver.find_elements_by_id('book')[1].click()
        time.sleep(2)
        places = self.driver.find_element_by_name('places')
        places.send_keys("16")
        time.sleep(2)
        self.driver.find_element_by_tag_name('button').click()
        time.sleep(2)
        assert 'Not enough points available. Sorry.' in self.driver.page_source

    @patch('server.research_club_in_clubs_by_email')
    def test_not_enough_places(self, mock_research_club_in_clubs_by_email):
        mock_research_club_in_clubs_by_email.return_value = CLUB_ONE

        self.driver.get(self.get_server_url() + "/login")
        time.sleep(2)
        email = self.driver.find_element_by_name('email')
        email.send_keys("club_test1@mail.com")

        time.sleep(2) 
        self.driver.find_element_by_tag_name('button').click()
        time.sleep(2)
        self.driver.get(self.get_server_url() + "/showSummary")
        self.driver.find_element_by_id('points')
        assert 'Points available: 15' in self.driver.page_source
        time.sleep(2)
        self.driver.find_elements_by_id('book')[0].click()
        time.sleep(2)
        places = self.driver.find_element_by_name('places')
        places.send_keys("12")
        time.sleep(2)
        self.driver.find_element_by_tag_name('button').click()
        time.sleep(2)
        assert 'Not enough places available. Sorry' in self.driver.page_source

