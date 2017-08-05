from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from .login import login_user

import os
import time
import unittest

# TODO - Debug page loading issue when using StaticLiveServerTestCase
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8081'


class AlbumsAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(AlbumsAppTests, cls).setUpClass()
        login_user(cls)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(AlbumsAppTests, cls).tearDownClass()

    def test_root_url_redirects_to_albums_index(self):
        self.browser.get(self.live_server_url)
        self.assertEqual(self.live_server_url+'/albums/',
                         self.browser.current_url)
