from base import mods
from base.tests import BaseTestCase

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from rest_framework.test import APIClient

from selenium import webdriver
from selenium.webdriver.common.by import By

import time

class LoginTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()
        self.client = APIClient()
        mods.mock_query(self.client)

        u123 = User(username='user123')
        u123.set_password('user123')
        u123.is_superuser = True
        u123.is_staff= True
        u123.save()

        options = webdriver.ChromeOptions()
        #Si se quieren ver en navegador, cambiar a false
        options.headless = True

        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        self.base.tearDown()

    def test_login_ok(self):
        self.driver.maximize_window()
        self.driver.get(''f'{self.live_server_url}''/authentication/accounts/login/?next=/')

        self.driver.find_element(By.NAME, "username").clear()
        self.driver.find_element(By.NAME, "username").send_keys('user123')
        time.sleep(0.5)
        self.driver.find_element(By.NAME, "password").clear()
        self.driver.find_element(By.NAME, "password").send_keys('user123')
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        time.sleep(0.5)

        self.assertTrue("Welcome!" in self.driver.page_source)

    def test_login_fail_wrong_User_Password(self):
        self.driver.maximize_window()
        self.driver.get(''f'{self.live_server_url}''/authentication/accounts/login/?next=/')

        self.driver.find_element(By.NAME, "username").clear()
        self.driver.find_element(By.NAME, "username").send_keys('userFail')
        time.sleep(0.5)
        self.driver.find_element(By.NAME, "password").clear()
        self.driver.find_element(By.NAME, "password").send_keys('passwordFail')
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        time.sleep(0.5)

        self.assertTrue("Login" in self.driver.page_source)

    def test_login_fail_blank_user(self):
        self.driver.maximize_window()
        self.driver.get(''f'{self.live_server_url}''/authentication/accounts/login/?next=/') 

        self.driver.find_element(By.NAME, "password").clear()
        self.driver.find_element(By.NAME, "password").send_keys('passwordFail')
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        time.sleep(0.5)

        self.assertTrue("Login" in self.driver.page_source)

    def test_login_fail_blank_password(self):
        self.driver.maximize_window()
        self.driver.get(''f'{self.live_server_url}''/authentication/accounts/login/?next=/') 

        self.driver.find_element(By.NAME, "username").clear()
        self.driver.find_element(By.NAME, "username").send_keys('userFail')
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        time.sleep(0.5)

        self.assertTrue("Login" in self.driver.page_source)

    def test_admin_success_access(self):
        self.driver.get(''f'{self.live_server_url}''/authentication/accounts/login/?next=/') 
        self.driver.find_element(By.NAME, "username").click()
        self.driver.find_element(By.NAME, "username").send_keys("user123")
        time.sleep(0.5)
        self.driver.find_element(By.NAME, "password").click()
        self.driver.find_element(By.NAME, "password").send_keys("user123")
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.find_element(By.CSS_SELECTOR, ".buttonWelcome").click()
        
        self.assertTrue("Site administration" in self.driver.page_source)
