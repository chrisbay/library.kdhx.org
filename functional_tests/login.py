from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import os
import time


def login_user(cls):
    login(cls, os.environ['KDHX_TEST_USER_EMAIL'],
          os.environ['KDHX_TEST_USER_PASS'])


# TODO - Set up admin test user
def login_admin(cls):
    login(cls, os.environ['KDHX_TEST_USER_EMAIL'],
          os.environ['KDHX_TEST_USER_PASS'])


def login(cls, user, password):
    cls.live_server_url = 'http://localhost:8000'

    try:
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(10)

        # Log in
        cls.browser.get(cls.live_server_url)
        email_field = cls.browser.find_element_by_id('identifierId')
        email_field.click()
        email_field.send_keys(user)
        email_field.send_keys(Keys.RETURN)
        WebDriverWait(cls.browser, 5).until(
            ec.visibility_of_element_located((By.ID, 'password')))
        password_field = cls.browser.find_element_by_css_selector(
            '#password [type="password"]')
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        WebDriverWait(cls.browser, 5).until(
            ec.visibility_of_element_located((By.ID, 'kdhx-logo')))
        assert cls.live_server_url+'/albums/' == cls.browser.current_url, \
            'Login redirect failed'
    except:
        cls.browser.quit()
        assert False, 'Login failed'
