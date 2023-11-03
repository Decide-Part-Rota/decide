from base import mods
from base.tests import BaseTestCase

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from rest_framework.test import APIClient

from selenium import webdriver
from selenium.webdriver.common.by import By

import time


class TestNavbar(StaticLiveServerTestCase):
  def setUp(self):
    self.base = BaseTestCase()
    self.base.setUp()
    self.client = APIClient()
    mods.mock_query(self.client)

    u123 = User(username='user123')
    u123.set_password('user123')
    u123.is_superuser = True
    u123.save()

    options = webdriver.ChromeOptions()
    options.headless = True
    self.driver = webdriver.Chrome(options=options)

  def tearDown(self):
    super().tearDown()
    self.driver.quit()
    self.base.tearDown()
  
  def test_navbar(self):
    self.driver.get(''f'{self.live_server_url}''/booth/boothList/')
    time.sleep(0.5)
    self.assertTrue("Log In" in self.driver.page_source)
    self.driver.find_element(By.CSS_SELECTOR, ".cta > button").click()
    self.driver.find_element(By.NAME, "username").click()
    self.driver.find_element(By.NAME, "username").send_keys("user123")
    time.sleep(0.5)
    self.driver.find_element(By.NAME, "password").click()
    self.driver.find_element(By.NAME, "password").send_keys("user123")
    time.sleep(0.5)
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    self.driver.find_element(By.CSS_SELECTOR, ".welcome").click()
    self.assertTrue("Log Out" in self.driver.page_source)