import urllib3
from flask import Flask
from flask_testing import LiveServerTestCase
from selenium.webdriver import Chrome

from server import create_app


class TestBase(LiveServerTestCase):
    def create_app(self):
        app = create_app({"TESTING": True})
        print('****createUp******') 
        return app

    
    def setUp(self):
        print('****setUp******')    
        # self.driver = Chrome(executable_path='tests/test_fonctionnel/chromedriver.exe')
        # self.driver.get(self.live_server_url())
    
    def tearDown(self):
        print('****tearDown******')
        # self.driver.quit()
        
    
    def test_open_chrome_window(self):
        print('****test******')

