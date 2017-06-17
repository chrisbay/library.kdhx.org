from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import os
import time
import unittest

# TODO - Debug page loading issue when using StaticLiveServerTestCase
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8081'


class AlbumsAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.live_server_url = 'http://localhost:8000'
        super(AlbumsAppTests, cls).setUpClass()

        try:
            cls.browser = webdriver.Firefox()
            cls.browser.implicitly_wait(10)

            # Log in
            cls.browser.get(cls.live_server_url)
            email_field = cls.browser.find_element_by_id('identifierId')
            email_field.click()
            email_field.send_keys(os.environ['KDHX_TEST_USER_EMAIL'])
            email_field.send_keys(Keys.RETURN)
            WebDriverWait(cls.browser, 5).until(
                ec.visibility_of_element_located((By.ID, 'password')))
            password_field = cls.browser.find_element_by_css_selector(
                '#password [type="password"]')
            password_field.send_keys(os.environ['KDHX_TEST_USER_PASS'])
            password_field.send_keys(Keys.RETURN)
            WebDriverWait(cls.browser, 5).until(
                ec.visibility_of_element_located((By.ID, 'kdhx-logo')))
            assert cls.live_server_url+'/albums/' == cls.browser.current_url, \
                'Login redirect failed'
        except:
            cls.browser.quit()
            assert False, 'Login failed'

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(AlbumsAppTests, cls).tearDownClass()

    def test_root_url_redirects_to_albums_index(self):
        self.browser.get(self.live_server_url)
        self.assertEqual(self.live_server_url+'/albums/',
                         self.browser.current_url)
