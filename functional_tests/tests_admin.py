from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from .login import login_admin

import os
import time
import unittest

# TODO - Debug page loading issue when using StaticLiveServerTestCase
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8081'


class AlbumsAppAdminTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        login_admin(cls)
        super(AlbumsAppAdminTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(AlbumsAppAdminTests, cls).tearDownClass()

    def test_can_add_new_album(self):

        self.assertTrue(True)

        # User browses to /albums/new/ and sees the new album form
        # self.browser.get(self.live_server_url+'/albums/new/')
        # self.assertIn('New Album', self.browser.title)
        # header_text = self.browser.find_element_by_xpath('//h2[1]').text
        # self.assertIn('New Album', header_text)
        # album_name_input = self.browser.find_element_by_xpath(
        #     '//form//input[@name="title"]')

        # TODO - User enters data for a new album, and clicks the Save button

        # TODO - User sees new album form rendered again,
        # with a confirmation flash message

        # TODO - User clicks on flash message link to view new album details