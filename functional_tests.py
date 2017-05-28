from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import os
import unittest
import time

class AlbumsAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        try:

            cls.browser = webdriver.Firefox()
            cls.browser.implicitly_wait(3)

            cls.browser.get('http://localhost:8000')

            # Log in
            email_field = cls.browser.find_element_by_id('identifierId')
            email_field.click()
            email_field.send_keys(os.environ['KDHX_TEST_USER_EMAIL'])
            email_field.send_keys(Keys.RETURN)
            
            WebDriverWait(cls.browser, 5).until(
                ec.visibility_of_element_located((By.ID, 'password')))
            password_field = cls.browser.find_element_by_css_selector('#password [type="password"]')
            password_field.send_keys(os.environ['KDHX_TEST_USER_PASS'])
            password_field.send_keys(Keys.RETURN)
            
            WebDriverWait(cls.browser, 5).until(
                ec.visibility_of_element_located((By.ID, 'kdhx-logo')))

            assert 'http://localhost:8000/albums/' == cls.browser.current_url, 'Login redirect failed'

        except:
            cls.browser.quit()
            assert False, 'Login failed'


    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()


    def test_root_url_redirects_to_albums_index(self):
        self.browser.get('http://localhost:8000')
        self.assertEqual('http://localhost:8000/albums/', self.browser.current_url)


    def test_can_add_new_media(self):

        # User browses to /albums/media/new/ and sees the new media type form
        self.browser.get('http://localhost:8000/albums/media/new/')
        self.assertIn('New Media Type', self.browser.title)

        header_text = self.browser.find_element_by_xpath('//h2[1]').text
        self.assertIn('New Media Type', header_text)

        label_input = self.browser.find_element_by_xpath('//form//input[@name="label"]')
        self.assertIsNotNone(label_input)

        # User enters a label for the new media type, and clicks the Save button
        label = 'LP-' + str(time.time())
        label_input.click()
        label_input.send_keys(label)
        save_btn = self.browser.find_element_by_xpath('//form//input[@type="submit"]')
        save_btn.click()

        # User sees confirmation message in response
        message_div = self.browser.find_element_by_css_selector('#messages .alert-success')
        self.assertIn(label, message_div.text)

        # TODO - delete type from database

        # TODO - User is redirected to the Albums Admin page, with a confirmation flash message
    

    def test_can_add_new_album(self):

        # User browses to /albums/new/ and sees the new album form
        self.browser.get('http://localhost:8000/albums/new/')
        self.assertIn('New Album', self.browser.title)

        header_text = self.browser.find_element_by_xpath('//h2[1]').text
        self.assertIn('New Album', header_text)

        album_name_input = self.browser.find_element_by_xpath('//form/input[@name="album-title"]')
        self.assertEqual(album_name_input.get_attribute('placeholder'), 'Album Title')

        # TODO - User enters data for a new album, and clicks the Save button

        # TODO - User sees new album form rendered again, with a confirmation flash message

        # TODO - User clicks on the flash message link to view new album details


if __name__ == '__main__':
    unittest.main()