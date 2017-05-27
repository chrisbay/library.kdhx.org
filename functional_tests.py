from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import unittest
import time


class AlbumsAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        try:

            cls.browser = webdriver.Firefox()
            cls.browser.implicitly_wait(10)

            google_email_field_id = 'identifierId'
            google_email_next_btn_id = 'identifierNext'
            google_password_field_selector = '#password [type="password"]'
            google_password_next_btn_id = 'passwordNext'

            cls.browser.get('http://localhost:8000')

            # Log in
            email_field = cls.browser.find_element_by_id(google_email_field_id)
            email_field.click()
            email_field.send_keys(os.environ['KDHX_TEST_USER_EMAIL'])
            email_field.send_keys(Keys.RETURN)
            time.sleep(2)

            password_field = cls.browser.switch_to.active_element['value']
            password_field.send_keys(os.environ['KDHX_TEST_USER_PASS'])
            password_field.send_keys(Keys.RETURN)
            time.sleep(2)

        except:
            cls.browser.quit()
            assert False, 'Login failed'

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    def test_login_redirect_url_is_albums(self):
        self.assertEqual('http://localhost:8000/albums/', self.browser.current_url)

    def test_albums_page_loads(self):
        self.browser.get('http://localhost:8000/albums/')
        self.assertIn('KDHX', self.browser.title)


if __name__ == '__main__':
    unittest.main()