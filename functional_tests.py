from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import os
import unittest


class AlbumsAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        try:

            cls.browser = webdriver.Firefox()
            cls.browser.implicitly_wait(10)

            google_email_field_id = 'identifierId'
            google_password_field_selector = '#password [type="password"]'

            cls.browser.get('http://localhost:8000')

            # Log in
            email_field = cls.browser.find_element_by_id(google_email_field_id)
            email_field.click()
            email_field.send_keys(os.environ['KDHX_TEST_USER_EMAIL'])
            email_field.send_keys(Keys.RETURN)
            
            WebDriverWait(cls.browser, 5).until(
                ec.visibility_of_element_located((By.ID, 'password')))
            password_field = cls.browser.find_element_by_css_selector(google_password_field_selector)
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

    
    def test_can_add_new_album(self):

        # User browses to /albums/new/ and sees the new album form
        self.browser.get('http://localhost:8000/albums/new/')
        self.assertIn('New Album', self.browser.title)

        # User enters data for a new album, and clicks the Save button

        # User sees new album form rendered again, with a confirmation flash message

        # User clicks on the flash message link to view new album details


if __name__ == '__main__':
    unittest.main()