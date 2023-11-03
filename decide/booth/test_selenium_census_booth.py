from base import mods
from base.tests import BaseTestCase

from django.contrib.auth.models import User
from django.conf import settings
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


from rest_framework.test import APIClient

from selenium import webdriver
from selenium.webdriver.common.by import By

import time

class TestBooth(StaticLiveServerTestCase):
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

        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='Test voting', question=q)
        v.public=True
        v.save()
        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
  
    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        self.base.tearDown()
  
    def test_booth_OpenVotings(self):
        self.driver.get(''f'{self.live_server_url}''/booth/boothList/')
        time.sleep(0.5)
        self.assertTrue("If you want to see this service you need to log in" in self.driver.page_source)
        self.driver.find_element(By.CSS_SELECTOR, "button").click()
        self.driver.find_element(By.NAME, "username").click()
        self.driver.find_element(By.NAME, "username").send_keys("user123")
        time.sleep(0.5)
        self.driver.find_element(By.NAME, "password").click()
        self.driver.find_element(By.NAME, "password").send_keys("user123")
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.find_element(By.LINK_TEXT, "Open Votings").click()
        self.assertTrue("ID" in self.driver.page_source)

    def test_booth_MyVotings(self):
        self.driver.get(''f'{self.live_server_url}''/booth/boothListPrivate/')
        time.sleep(0.5)
        self.assertTrue("If you want to see this service you need to log in" in self.driver.page_source)
        self.driver.find_element(By.CSS_SELECTOR, "button").click()
        self.driver.find_element(By.NAME, "username").click()
        self.driver.find_element(By.NAME, "username").send_keys("user123")
        time.sleep(0.5)
        self.driver.find_element(By.NAME, "password").click()
        self.driver.find_element(By.NAME, "password").send_keys("user123")
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.find_element(By.LINK_TEXT, "My Votings").click()
        self.assertTrue("ID" in self.driver.page_source)

    def test_JoinCensus_success(self):
        self.driver.get(''f'{self.live_server_url}''/booth/boothList/')
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, "button").click()
        self.driver.find_element(By.NAME, "username").click()
        self.driver.find_element(By.NAME, "username").send_keys("user123")
        time.sleep(0.5)
        self.driver.find_element(By.NAME, "password").click()
        self.driver.find_element(By.NAME, "password").send_keys("user123")
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.find_element(By.LINK_TEXT, "Open Votings").click()
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "Join census").click()
        self.driver.get(''f'{self.live_server_url}''/booth/boothListPrivate/')
        self.assertTrue("Test voting" in self.driver.page_source)

    def test_LeaveCensus_success(self):
        self.driver.get(''f'{self.live_server_url}''/booth/boothList/')
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, "button").click()
        self.driver.find_element(By.NAME, "username").click()
        self.driver.find_element(By.NAME, "username").send_keys("user123")
        time.sleep(0.5)
        self.driver.find_element(By.NAME, "password").click()
        self.driver.find_element(By.NAME, "password").send_keys("user123")
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.find_element(By.LINK_TEXT, "Open Votings").click()
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "Join census").click()
        self.driver.get(''f'{self.live_server_url}''/booth/boothListPrivate/')
        self.driver.find_element(By.LINK_TEXT, "Quit Census").click()
        self.driver.get(''f'{self.live_server_url}''/booth/boothList/')
        self.assertTrue("Test voting" in self.driver.page_source)
    